import calendar
from dataclasses import dataclass
from datetime import date
from decimal import Decimal, ROUND_CEILING, ROUND_HALF_UP

from dateutil.relativedelta import relativedelta
from django.db import transaction
from django.db.models import Sum
from rest_framework import serializers

from api.models import (
    Company,
    Calculations,
    EarnedAmount,
    EmployeeAdvanceEmiRepayment,
    EmployeeAdvancePayment,
    EmployeeAttendance,
    EmployeeMonthlyAttendanceDetails,
    EmployeePersonalDetail,
    EmployeePfEsiDetail,
    EmployeeProfessionalDetail,
    EmployeeSalaryDetail,
    EmployeeSalaryEarning,
    EmployeeSalaryPrepared,
    EmployeeSalaryPreparedOvertimeDetail,
    PfEsiSetup,
)
from api.services.overtime_policy import calculate_employee_overtime, calculate_employee_overtime_from_loaded


MIN_PAYROLL_YEAR = 1950
MAX_PAYROLL_YEAR = 2100


@dataclass(frozen=True)
class SalaryPreparationResult:
    salary: EmployeeSalaryPrepared
    overtime_result: object


@dataclass(frozen=True)
class SalaryCalculation:
    actor: object
    company: Company
    employee: EmployeePersonalDetail
    period_start: date
    salary: object
    earned_rows: list
    earnings_heads: dict
    advances: list
    repaid: dict
    overtime_result: object
    values: dict
    net_salary: Decimal


def _error(detail, *, code='invalid_salary_preparation', field=None):
    payload = {'code': code, 'detail': detail}
    if field:
        payload['field'] = field
    raise serializers.ValidationError(payload)


def validate_period(*, year, month):
    if not isinstance(year, int) or not MIN_PAYROLL_YEAR <= year <= MAX_PAYROLL_YEAR:
        _error(
            f'Year must be between {MIN_PAYROLL_YEAR} and {MAX_PAYROLL_YEAR}.',
            code='invalid_salary_period',
            field='year',
        )
    if not isinstance(month, int) or not 1 <= month <= 12:
        _error('Month must be between 1 and 12.', code='invalid_salary_period', field='month')
    return date(year, month, 1)


def resolve_salary_scope(*, actor, company_id, employee_id=None):
    if not getattr(actor, 'is_authenticated', False):
        _error('Authentication is required.', code='authentication_required')
    if actor.role == 'OWNER':
        owner = actor
    elif actor.role == 'REGULAR':
        owner = getattr(getattr(actor, 'regular_to_owner', None), 'owner', None)
    else:
        owner = None
    if owner is None:
        _error('The authenticated account role is unsupported.', code='unsupported_account_role')

    try:
        company = Company.objects.get(pk=company_id, user=owner)
    except Company.DoesNotExist:
        _error('The company was not found.', code='company_not_found', field='company')
    if actor.role == 'REGULAR' and not company.visible:
        _error('The company is not visible to this account.', code='company_not_visible')

    if employee_id is None:
        return owner, company, None
    try:
        employee = EmployeePersonalDetail.objects.get(pk=employee_id, company=company, user=owner)
    except EmployeePersonalDetail.DoesNotExist:
        _error('The employee was not found in this company.', code='employee_not_found', field='employee')
    if actor.role == 'REGULAR' and not employee.visible:
        _error('The employee is not visible to this account.', code='employee_not_visible')
    return owner, company, employee


def serialize_overtime_result(result, *, include_diagnostics=False):
    def serialize_row(row):
        return {
            key: str(value) if isinstance(value, Decimal) else value
            for key, value in row.items()
        }

    payload = {
        'effective_policy': result.effective_policy,
        'period_start': result.period_start,
        'period_end': result.period_end,
        'totals': {
            'raw_eligible_minutes': result.raw_eligible_minutes,
            'rounded_gross_minutes': result.rounded_gross_minutes,
            'deducted_late_minutes': result.deducted_late_minutes,
            'net_minutes': result.net_minutes,
            'amount': str(result.amount),
        },
        'breakdown': [serialize_row(row) for row in result.breakdown],
    }
    if include_diagnostics:
        payload['group_diagnostics'] = [serialize_row(row) for row in result.group_diagnostics]
    return payload


def _lock_overtime_attendance(*, actor, company, employee, period_start):
    period_end = period_start + relativedelta(months=1) - relativedelta(days=1)
    return list(EmployeeAttendance.objects.select_for_update().filter(
        user=actor,
        company=company,
        employee=employee,
        date__range=(period_start, period_end),
    ).order_by('id', 'date'))


@transaction.atomic
def preview_employee_overtime(*, actor, company_id, employee_id, year, month):
    period_start = validate_period(year=year, month=month)
    owner, company, employee = resolve_salary_scope(
        actor=actor, company_id=company_id, employee_id=employee_id,
    )
    Company.objects.select_for_update().get(pk=company.pk)
    _lock_overtime_attendance(
        actor=actor, company=company, employee=employee, period_start=period_start,
    )
    list(EmployeeSalaryEarning.objects.select_for_update().filter(
        user=owner,
        company=company,
        employee=employee,
        from_date__lte=period_start,
        to_date__gte=period_start,
    ).order_by('pk'))
    list(EmployeeSalaryDetail.objects.select_for_update().filter(
        user=owner, company=company, employee=employee,
    ))
    list(Calculations.objects.select_for_update().filter(user=owner, company=company))
    return calculate_employee_overtime(
        actor=actor,
        company=company,
        employee=employee,
        period_start=period_start,
    )


def _load_prerequisites(*, actor, owner, company, employee, period_start):
    try:
        salary_detail = EmployeeSalaryDetail.objects.select_for_update(of=('self',)).select_related(
            'employee', 'company', 'overtime_policy',
        ).get(
            user=owner, company=company, employee=employee,
        )
    except EmployeeSalaryDetail.DoesNotExist:
        _error('The employee salary detail is missing.', code='missing_employee_salary_detail')
    try:
        pf_esi_detail = EmployeePfEsiDetail.objects.select_for_update().get(
            company=company, employee=employee,
        )
    except EmployeePfEsiDetail.DoesNotExist:
        _error('The employee PF/ESI detail is missing.', code='missing_employee_pf_esi_detail')
    try:
        pf_esi_setup = PfEsiSetup.objects.select_for_update().get(user=owner, company=company)
    except PfEsiSetup.DoesNotExist:
        _error('The company PF/ESI setup is missing.', code='missing_company_pf_esi_setup')
    try:
        company_calculations = Calculations.objects.get(user=owner, company=company)
    except Calculations.DoesNotExist:
        _error('The company overtime calculation configuration is missing.', code='missing_company_calculations')

    attendance_rows = list(EmployeeMonthlyAttendanceDetails.objects.select_for_update().filter(
        user=actor, company=company, employee=employee, date=period_start,
    ).order_by('pk')[:2])
    if not attendance_rows:
        _error('The monthly attendance summary is missing.', code='missing_monthly_attendance')
    if len(attendance_rows) > 1:
        _error('Multiple monthly attendance summaries exist.', code='duplicate_monthly_attendance')

    salary_earnings = list(EmployeeSalaryEarning.objects.select_for_update().select_related('earnings_head').filter(
        user=owner,
        company=company,
        employee=employee,
        from_date__lte=period_start,
        to_date__gte=period_start,
    ).order_by('earnings_head_id'))
    if not salary_earnings:
        _error('The employee has no active salary earnings.', code='missing_salary_earnings')
    head_ids = [earning.earnings_head_id for earning in salary_earnings]
    if len(head_ids) != len(set(head_ids)):
        _error(
            'Multiple active salary rates exist for an earnings head.',
            code='duplicate_active_salary_earning',
        )
    return salary_detail, pf_esi_detail, pf_esi_setup, company_calculations, attendance_rows[0], salary_earnings


def _default_earned_inputs(*, salary_detail, monthly_attendance, salary_earnings, period_start):
    paid_days = Decimal(monthly_attendance.paid_days_count) / Decimal(2)
    days_in_month = Decimal(calendar.monthrange(period_start.year, period_start.month)[1])
    rows = []
    for earning in salary_earnings:
        amount = Decimal(earning.value) * paid_days
        if salary_detail.salary_mode == 'monthly':
            amount /= days_in_month
        amount = amount.quantize(Decimal('1'), rounding=ROUND_HALF_UP)
        rows.append({
            'earnings_head_id': earning.earnings_head_id,
            'rate': earning.value,
            'earned_amount': int(amount),
            'arear_amount': 0,
        })
    return rows


def _normalize_manual_earned_inputs(
    *, earned_inputs, salary_detail, monthly_attendance, salary_earnings, period_start,
):
    if not isinstance(earned_inputs, list):
        _error('Earned amounts must be an array.', code='invalid_earned_amounts', field='all_earned_amounts')
    earning_by_head = {earning.earnings_head_id: earning for earning in salary_earnings}
    expected = _default_earned_inputs(
        salary_detail=salary_detail,
        monthly_attendance=monthly_attendance,
        salary_earnings=salary_earnings,
        period_start=period_start,
    )
    base_by_head = {row['earnings_head_id']: row['earned_amount'] for row in expected}
    normalized = []
    seen = set()
    for index, raw_row in enumerate(earned_inputs):
        if not isinstance(raw_row, dict):
            _error(f'Earned amount row {index + 1} must be an object.', code='invalid_earned_amounts')
        raw_head = raw_row.get('earnings_head')
        head_id = raw_head.get('id') if isinstance(raw_head, dict) else raw_head
        try:
            head_id = int(head_id)
        except (TypeError, ValueError):
            _error(f'Earned amount row {index + 1} has an invalid earnings head.', code='invalid_earned_head')
        if head_id in seen:
            _error('Each earnings head may appear only once.', code='duplicate_earned_head')
        seen.add(head_id)
        earning = earning_by_head.get(head_id)
        if earning is None:
            _error('An earned amount head is not active for this employee and period.', code='invalid_earned_head')
        try:
            rate = int(raw_row.get('rate'))
            earned_amount = int(raw_row.get('earned_amount'))
            arear_amount = int(raw_row.get('arear_amount', 0))
        except (TypeError, ValueError):
            _error('Earned amount values must be whole numbers.', code='invalid_earned_amounts')
        if min(rate, earned_amount, arear_amount) < 0:
            _error('Earned amount values cannot be negative.', code='invalid_earned_amounts')
        if rate != earning.value:
            _error('The submitted salary rate is stale.', code='stale_salary_rate')
        if earned_amount != base_by_head[head_id] + arear_amount:
            _error('Earned amount must equal the server-calculated amount plus arrears.', code='invalid_earned_amount')
        normalized.append({
            'earnings_head_id': head_id,
            'rate': rate,
            'earned_amount': earned_amount,
            'arear_amount': arear_amount,
        })
    missing = sorted(set(earning_by_head) - seen)
    if missing:
        _error('Every active salary earning head is required.', code='missing_earned_heads')
    return normalized


def _earned_inputs_from_arrears(
    *, arrear_inputs, salary_detail, monthly_attendance, salary_earnings, period_start,
):
    rows = _default_earned_inputs(
        salary_detail=salary_detail,
        monthly_attendance=monthly_attendance,
        salary_earnings=salary_earnings,
        period_start=period_start,
    )
    rows_by_head = {row['earnings_head_id']: row for row in rows}
    seen = set()
    for raw_row in arrear_inputs or []:
        head_id = raw_row['earnings_head']
        if head_id in seen:
            _error('Each earnings head may appear only once.', code='duplicate_earned_head')
        seen.add(head_id)
        row = rows_by_head.get(head_id)
        if row is None:
            _error('An arrear earnings head is not active for this employee and period.', code='invalid_earned_head')
        row['arear_amount'] = raw_row.get('arear_amount', 0)
        row['earned_amount'] += row['arear_amount']
    return rows


def _calculate_deductions(
    *, actor, salary_detail, pf_esi_detail, pf_esi_setup, earned_rows, earnings_heads, overtime_result,
):
    total_earned = sum(row['earned_amount'] for row in earned_rows)
    basic_rows = [
        row for row in earned_rows
        if earnings_heads[row['earnings_head_id']].name == 'Basic'
    ]
    pf_deducted = Decimal(0)
    if pf_esi_detail.pf_allow:
        if len(basic_rows) != 1:
            _error('A single active Basic earning is required for PF.', code='missing_basic_earning')
        basic_earned = basic_rows[0]['earned_amount']
        if pf_esi_detail.pf_limit_ignore_employee:
            pfable = basic_earned
            if pf_esi_detail.pf_limit_ignore_employee_value is not None:
                pfable = min(pfable, pf_esi_detail.pf_limit_ignore_employee_value)
        else:
            pfable = min(pf_esi_setup.ac_1_epf_employee_limit, basic_earned)
        pf_deducted = (
            Decimal(pfable) * pf_esi_setup.ac_1_epf_employee_percentage / Decimal(100)
        ).quantize(Decimal('1'), rounding=ROUND_HALF_UP)

    esi_deducted = Decimal(0)
    if pf_esi_detail.esi_allow:
        esi_basis = Decimal(total_earned)
        if actor.role == 'REGULAR' or pf_esi_detail.esi_on_ot:
            esi_basis += overtime_result.amount
        esiable = min(Decimal(pf_esi_setup.esi_employee_limit), esi_basis)
        esi_deducted = (
            esiable * pf_esi_setup.esi_employee_percentage / Decimal(100)
        ).quantize(Decimal('1'), rounding=ROUND_CEILING)

    lwf_deducted = Decimal(0)
    if pf_esi_setup.enable_labour_welfare_fund and salary_detail.labour_wellfare_fund:
        lwf_deducted = min(
            Decimal(pf_esi_setup.labour_welfare_fund_limit),
            Decimal(total_earned) * pf_esi_setup.labour_welfare_fund_percentage / Decimal(100),
        ).quantize(Decimal('1'), rounding=ROUND_HALF_UP)
    return {
        'pf_deducted': int(pf_deducted),
        'esi_deducted': int(esi_deducted),
        'vpf_deducted': pf_esi_detail.vpf_amount,
        'tds_deducted': pf_esi_detail.tds_amount,
        'labour_welfare_fund_deducted': int(lwf_deducted),
        'payment_mode': salary_detail.payment_mode,
    }


def _lock_advances(*, owner, actor, company, employee, period_start, salary):
    advances = list(EmployeeAdvancePayment.objects.select_for_update().filter(
        user=owner,
        employee=employee,
        company=company,
        date__lt=period_start + relativedelta(months=1),
    ).order_by('date', 'pk'))
    advance_ids = [advance.pk for advance in advances]
    repayments = EmployeeAdvanceEmiRepayment.objects.select_for_update().filter(
        employee_advance_payment_id__in=advance_ids,
        user__role=actor.role,
    )
    if salary is not None:
        repayments = repayments.exclude(salary_prepared=salary)
    repaid = {}
    for repayment in repayments.only('employee_advance_payment_id', 'amount'):
        advance_id = repayment.employee_advance_payment_id
        repaid[advance_id] = repaid.get(advance_id, 0) + repayment.amount
    return advances, repaid


def _default_advance_deduction(*, advances, repaid):
    return sum(
        min(advance.emi, max(advance.principal - repaid.get(advance.pk, 0), 0))
        for advance in advances
    )


def _validate_advance_deduction(*, advances, repaid, amount):
    capacity = sum(max(advance.principal - repaid.get(advance.pk, 0), 0) for advance in advances)
    if amount > capacity:
        _error('Advance deduction exceeds the remaining repayment capacity.', code='excessive_advance_repayment')


def _replace_repayments(*, actor, salary, advances, repaid, amount):
    EmployeeAdvanceEmiRepayment.objects.filter(salary_prepared=salary).delete()
    _validate_advance_deduction(advances=advances, repaid=repaid, amount=amount)
    remaining = amount
    minimum_due = _default_advance_deduction(advances=advances, repaid=repaid)
    surplus = max(amount - minimum_due, 0)
    rows = []
    for advance in advances:
        available = max(advance.principal - repaid.get(advance.pk, 0), 0)
        allocation = min(available, advance.emi)
        if surplus:
            extra = min(max(available - allocation, 0), surplus)
            allocation += extra
            surplus -= extra
        allocation = min(allocation, remaining)
        if allocation > 0:
            rows.append(EmployeeAdvanceEmiRepayment(
                user=actor,
                amount=allocation,
                employee_advance_payment=advance,
                salary_prepared=salary,
            ))
            remaining -= allocation
        if remaining == 0:
            break
    if remaining:
        _error('Advance repayment could not be allocated.', code='advance_reconciliation_failed')
    EmployeeAdvanceEmiRepayment.objects.bulk_create(rows)


def _reconcile_salary(salary):
    child_totals = salary.overtime_breakdown.aggregate(
        minutes=Sum('net_minutes'), amount=Sum('amount'),
    )
    if salary.net_ot_minutes_monthly != (child_totals['minutes'] or 0):
        _error('Saved overtime minutes do not reconcile.', code='overtime_reconciliation_failed')
    child_amount_total = Decimal(child_totals['amount'] or 0).quantize(
        Decimal('1'), rounding=ROUND_HALF_UP
    )
    if salary.net_ot_amount_monthly != child_amount_total:
        _error('Saved overtime amount does not reconcile.', code='overtime_reconciliation_failed')
    repayment_total = salary.emis_with_salary_prepared.aggregate(total=Sum('amount'))['total'] or 0
    if salary.advance_deducted != repayment_total:
        _error('Saved advance repayments do not reconcile.', code='advance_reconciliation_failed')


def _calculate_employee_salary(
    *, actor, company_id, employee_id, year, month, parent_inputs=None, earned_inputs=None,
    arrear_inputs=None, bulk=False,
):
    period_start = validate_period(year=year, month=month)
    owner, company, employee = resolve_salary_scope(
        actor=actor, company_id=company_id, employee_id=employee_id,
    )
    Company.objects.select_for_update().get(pk=company.pk)
    salary = EmployeeSalaryPrepared.objects.select_for_update().filter(
        user=actor, employee=employee, date=period_start,
    ).first()
    attendance_records = _lock_overtime_attendance(
        actor=actor, company=company, employee=employee, period_start=period_start,
    )
    salary_detail, pf_esi_detail, pf_esi_setup, company_calculations, monthly_attendance, salary_earnings = _load_prerequisites(
        actor=actor,
        owner=owner,
        company=company,
        employee=employee,
        period_start=period_start,
    )
    if bulk:
        earned_rows = _default_earned_inputs(
            salary_detail=salary_detail,
            monthly_attendance=monthly_attendance,
            salary_earnings=salary_earnings,
            period_start=period_start,
        )
    elif arrear_inputs is not None:
        earned_rows = _earned_inputs_from_arrears(
            arrear_inputs=arrear_inputs,
            salary_detail=salary_detail,
            monthly_attendance=monthly_attendance,
            salary_earnings=salary_earnings,
            period_start=period_start,
        )
    else:
        earned_rows = _normalize_manual_earned_inputs(
            earned_inputs=earned_inputs,
            salary_detail=salary_detail,
            monthly_attendance=monthly_attendance,
            salary_earnings=salary_earnings,
            period_start=period_start,
        )
    advances, repaid = _lock_advances(
        owner=owner,
        actor=actor,
        company=company,
        employee=employee,
        period_start=period_start,
        salary=salary,
    )
    earnings_heads = {earning.earnings_head_id: earning.earnings_head for earning in salary_earnings}
    overtime_result = calculate_employee_overtime_from_loaded(
        actor=actor,
        employee_salary_detail=salary_detail,
        attendance_records=attendance_records,
        salary_earnings=salary_earnings,
        company_calculations=company_calculations,
        period_start=period_start,
    )
    deductions = _calculate_deductions(
        actor=actor,
        salary_detail=salary_detail,
        pf_esi_detail=pf_esi_detail,
        pf_esi_setup=pf_esi_setup,
        earned_rows=earned_rows,
        earnings_heads=earnings_heads,
        overtime_result=overtime_result,
    )
    parent_inputs = dict(parent_inputs or {})
    if bulk:
        advance_deducted = _default_advance_deduction(advances=advances, repaid=repaid)
        incentive_amount = 0
        others_deducted = 0
    else:
        advance_deducted = parent_inputs.get('advance_deducted')
        if advance_deducted is None:
            advance_deducted = _default_advance_deduction(advances=advances, repaid=repaid)
        incentive_amount = parent_inputs.get('incentive_amount', 0)
        others_deducted = parent_inputs.get('others_deducted', 0)
        for field in ('vpf_deducted', 'tds_deducted'):
            if parent_inputs.get(field) is not None:
                deductions[field] = parent_inputs[field]
    _validate_advance_deduction(
        advances=advances,
        repaid=repaid,
        amount=advance_deducted,
    )
    values = {
        'company': company,
        'incentive_amount': incentive_amount,
        'advance_deducted': advance_deducted,
        'others_deducted': others_deducted,
        'net_ot_minutes_monthly': sum(row['net_minutes'] for row in overtime_result.snapshot_breakdown),
        'net_ot_amount_monthly': overtime_result.amount,
        'ot_rounding_increment_minutes': overtime_result.rounding_increment_minutes,
        'ot_round_up_from_minutes': overtime_result.round_up_from_minutes,
        **deductions,
    }
    total_earned = sum(row['earned_amount'] for row in earned_rows)
    total_deductions = sum(values[field] for field in (
        'pf_deducted',
        'esi_deducted',
        'vpf_deducted',
        'advance_deducted',
        'tds_deducted',
        'labour_welfare_fund_deducted',
        'others_deducted',
    ))
    net_salary = (
        Decimal(total_earned)
        + Decimal(values['net_ot_amount_monthly'])
        + Decimal(incentive_amount)
        - Decimal(total_deductions)
    )
    return SalaryCalculation(
        actor=actor,
        company=company,
        employee=employee,
        period_start=period_start,
        salary=salary,
        earned_rows=earned_rows,
        earnings_heads=earnings_heads,
        advances=advances,
        repaid=repaid,
        overtime_result=overtime_result,
        values=values,
        net_salary=net_salary,
    )


def serialize_salary_calculation(calculation):
    def serialize_value(value):
        return str(value) if isinstance(value, Decimal) else value

    salary = {
        'employee': calculation.employee.pk,
        'company': calculation.company.pk,
        'date': calculation.period_start,
        **{
            key: serialize_value(value)
            for key, value in calculation.values.items()
            if key != 'company'
        },
        'net_salary': serialize_value(calculation.net_salary),
        'earned_amounts': [
            {
                'earnings_head': {
                    'id': row['earnings_head_id'],
                    'name': calculation.earnings_heads[row['earnings_head_id']].name,
                },
                'rate': row['rate'],
                'earned_amount': row['earned_amount'],
                'arear_amount': row['arear_amount'],
            }
            for row in calculation.earned_rows
        ],
        'overtime_breakdown': [
            {key: serialize_value(value) for key, value in row.items()}
            for row in calculation.overtime_result.snapshot_breakdown
        ],
    }
    return {
        'salary': salary,
        'overtime': serialize_overtime_result(calculation.overtime_result, include_diagnostics=True),
    }


@transaction.atomic
def preview_employee_salary(
    *, actor, company_id, employee_id, year, month, parent_inputs=None, arrear_inputs=None,
):
    calculation = _calculate_employee_salary(
        actor=actor,
        company_id=company_id,
        employee_id=employee_id,
        year=year,
        month=month,
        parent_inputs=parent_inputs,
        arrear_inputs=arrear_inputs,
    )
    return serialize_salary_calculation(calculation)


@transaction.atomic
def prepare_employee_salary(
    *, actor, company_id, employee_id, year, month, parent_inputs=None, earned_inputs=None,
    bulk=False,
):
    calculation = _calculate_employee_salary(
        actor=actor,
        company_id=company_id,
        employee_id=employee_id,
        year=year,
        month=month,
        parent_inputs=parent_inputs,
        earned_inputs=earned_inputs,
        bulk=bulk,
    )
    salary = calculation.salary
    defaults = calculation.values
    if salary is None:
        salary = EmployeeSalaryPrepared.objects.create(
            user=actor, employee=calculation.employee, date=calculation.period_start, **defaults,
        )
    else:
        for field, value in defaults.items():
            setattr(salary, field, value)
        salary.save(update_fields=list(defaults))

    salary.overtime_breakdown.all().delete()
    EmployeeSalaryPreparedOvertimeDetail.objects.bulk_create([
        EmployeeSalaryPreparedOvertimeDetail(salary_prepared=salary, **row)
        for row in calculation.overtime_result.snapshot_breakdown
    ])
    salary.current_salary_earned_amounts.all().delete()
    EarnedAmount.objects.bulk_create([
        EarnedAmount(user=actor, salary_prepared=salary, **row) for row in calculation.earned_rows
    ])
    _replace_repayments(
        actor=actor,
        salary=salary,
        advances=calculation.advances,
        repaid=calculation.repaid,
        amount=defaults['advance_deducted'],
    )
    _reconcile_salary(salary)
    return SalaryPreparationResult(salary=salary, overtime_result=calculation.overtime_result)


def _preflight_employee(*, actor, owner, company, employee, period_start):
    salary_detail, pf_esi_detail, pf_esi_setup, _company_calculations, monthly_attendance, salary_earnings = _load_prerequisites(
        actor=actor,
        owner=owner,
        company=company,
        employee=employee,
        period_start=period_start,
    )
    earned_rows = _default_earned_inputs(
        salary_detail=salary_detail,
        monthly_attendance=monthly_attendance,
        salary_earnings=salary_earnings,
        period_start=period_start,
    )
    overtime_result = calculate_employee_overtime(
        actor=actor, company=company, employee=employee, period_start=period_start,
    )
    _calculate_deductions(
        actor=actor,
        salary_detail=salary_detail,
        pf_esi_detail=pf_esi_detail,
        pf_esi_setup=pf_esi_setup,
        earned_rows=earned_rows,
        earnings_heads={earning.earnings_head_id: earning.earnings_head for earning in salary_earnings},
        overtime_result=overtime_result,
    )


@transaction.atomic
def bulk_prepare_salaries(*, actor, company_id, year, month, employee_ids=None):
    period_start = validate_period(year=year, month=month)
    owner, company, _ = resolve_salary_scope(actor=actor, company_id=company_id)
    Company.objects.select_for_update().get(pk=company.pk)
    period_end = period_start + relativedelta(months=1) - relativedelta(days=1)
    professionals = EmployeeProfessionalDetail.objects.active_employees_between_dates(
        user=owner, company_id=company.pk, from_date=period_start, to_date=period_end,
    ).select_related('employee').order_by('employee_id')
    if employee_ids is not None:
        requested_ids = list(dict.fromkeys(employee_ids))
        professionals = professionals.filter(employee_id__in=requested_ids)
    else:
        requested_ids = None
    if actor.role == 'REGULAR':
        professionals = professionals.filter(employee__visible=True)
    employees = [row.employee for row in professionals]
    errors = []
    if requested_ids is not None:
        missing = sorted(set(requested_ids) - {employee.pk for employee in employees})
        errors.extend({
            'employee': employee_id,
            'code': 'employee_not_found',
            'detail': 'The employee is unavailable in this company scope.',
        } for employee_id in missing)
    for employee in employees:
        try:
            _preflight_employee(
                actor=actor,
                owner=owner,
                company=company,
                employee=employee,
                period_start=period_start,
            )
        except Exception as exc:
            detail = getattr(exc, 'detail', str(exc))
            errors.append({'employee': employee.pk, 'error': detail})
    if errors:
        raise serializers.ValidationError({'code': 'bulk_preflight_failed', 'errors': errors})

    results = []
    for employee in employees:
        results.append(prepare_employee_salary(
            actor=actor,
            company_id=company.pk,
            employee_id=employee.pk,
            year=year,
            month=month,
            bulk=True,
        ))
    return results
