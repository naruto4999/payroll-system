from collections import defaultdict
from dataclasses import dataclass, field, fields

from ..models import (
    EarnedAmount,
    EmployeeMonthlyAttendanceDetails,
    EmployeeSalaryEarning,
    EmployeeSalaryPreparedOvertimeDetail,
    PfEsiSetup,
)
from ..report_options import resolve_report_options


@dataclass
class PaymentSheetTotals:
    salary_rate: float = 0
    salary_rate_breakdown: dict = field(default_factory=dict)
    paid_days: float = 0
    earned_salary: float = 0
    earned_salary_breakdown: dict = field(default_factory=dict)
    incentive: float = 0
    ot_hours: float = 0
    ot_amount: float = 0
    total_earned: float = 0
    advance: float = 0
    epf: float = 0
    esi: float = 0
    lwf: float = 0
    others: float = 0
    tds: float = 0
    total_deductions: float = 0
    net_payable: float = 0

    def add(self, row):
        for field in fields(self):
            value = getattr(row, field.name)
            if isinstance(value, dict):
                target = getattr(self, field.name)
                for head_id, amount in value.items():
                    target[head_id] = target.get(head_id, 0) + amount
                continue
            if value is not None:
                setattr(self, field.name, getattr(self, field.name) + value)


@dataclass(frozen=True)
class PaymentSheetRow:
    serial: int
    attendance_card_no: object
    employee_name: str
    father_or_husband_name: str
    designation: str
    department_id: int | None
    department_name: str | None
    salary_rate: float
    salary_rate_breakdown: dict
    paid_days: float | None
    earned_salary: float | None
    earned_salary_breakdown: dict
    incentive: float
    ot_hours: float | None
    ot_amount: float | None
    total_earned: float | None
    advance: float
    epf: float
    esi: float
    lwf: float
    others: float
    tds: float
    total_deductions: float
    net_payable: float | None


@dataclass
class PaymentSheetSection:
    department_id: int | None
    department_name: str | None
    rows: list
    totals: PaymentSheetTotals


@dataclass(frozen=True)
class PaymentSheetReport:
    company_name: str
    company_address: str
    show_lwf: bool
    grouped: bool
    salary_rate_columns: str
    earned_salary_columns: str
    salary_rate_heads: tuple
    earned_salary_heads: tuple
    ot_hours_label: str
    sections: list
    totals: PaymentSheetTotals

    @property
    def rows(self):
        return [row for section in self.sections for row in section.rows]


def _load_payment_sheet_data(user, prepared_salaries, include_weighted_ot=False):
    employee_ids = {salary.employee_id for salary in prepared_salaries}
    salary_ids = [salary.id for salary in prepared_salaries]
    salary_dates = {salary.date for salary in prepared_salaries}

    attendance_by_key = {}
    user_attendance_by_key = {}
    attendances = EmployeeMonthlyAttendanceDetails.objects.filter(
        employee_id__in=employee_ids,
        date__in=salary_dates,
    ).order_by('pk')
    for attendance in attendances:
        key = (attendance.employee_id, attendance.date)
        attendance_by_key.setdefault(key, attendance)
        if attendance.user_id == user.id:
            user_attendance_by_key.setdefault(key, attendance)

    salary_rates_by_employee = defaultdict(list)
    if salary_dates:
        salary_rates = EmployeeSalaryEarning.objects.filter(
            employee_id__in=employee_ids,
            from_date__lte=max(salary_dates),
            to_date__gte=min(salary_dates),
        ).select_related('earnings_head').order_by('pk')
        for salary_rate in salary_rates:
            salary_rates_by_employee[salary_rate.employee_id].append(salary_rate)

    earned_salary_by_salary = defaultdict(int)
    earned_salary_breakdown_by_salary = defaultdict(dict)
    earned_head_names = {}
    earned_salary_ids = set()
    earned_amounts = EarnedAmount.objects.filter(
        salary_prepared_id__in=salary_ids,
    ).select_related('earnings_head').only(
        'salary_prepared_id',
        'earnings_head_id',
        'earnings_head__name',
        'earned_amount',
    )
    for earned_amount in earned_amounts:
        earned_salary_ids.add(earned_amount.salary_prepared_id)
        earned_salary_by_salary[earned_amount.salary_prepared_id] += earned_amount.earned_amount
        earned_salary_breakdown_by_salary[earned_amount.salary_prepared_id][
            earned_amount.earnings_head_id
        ] = earned_amount.earned_amount
        earned_head_names[earned_amount.earnings_head_id] = earned_amount.earnings_head.name

    weighted_ot_minutes_by_salary = defaultdict(int)
    salaries_with_ot_breakdown = set()
    if include_weighted_ot:
        overtime_details = EmployeeSalaryPreparedOvertimeDetail.objects.filter(
            salary_prepared_id__in=salary_ids,
        ).only('salary_prepared_id', 'net_minutes', 'multiplier')
        for detail in overtime_details:
            salaries_with_ot_breakdown.add(detail.salary_prepared_id)
            weighted_ot_minutes_by_salary[detail.salary_prepared_id] += (
                detail.net_minutes * detail.multiplier
            )

    return {
        'attendance_by_key': attendance_by_key,
        'user_attendance_by_key': user_attendance_by_key,
        'salary_rates_by_employee': salary_rates_by_employee,
        'earned_salary_by_salary': earned_salary_by_salary,
        'earned_salary_breakdown_by_salary': earned_salary_breakdown_by_salary,
        'earned_head_names': earned_head_names,
        'earned_salary_ids': earned_salary_ids,
        'weighted_ot_minutes_by_salary': weighted_ot_minutes_by_salary,
        'salaries_with_ot_breakdown': salaries_with_ot_breakdown,
    }


def _salary_rate_for(salary, salary_rates):
    owner_id = (
        salary.user_id
        if salary.user.role == 'OWNER'
        else salary.user.regular_to_owner.owner_id
    )
    seen_head_ids = set()
    total = 0
    breakdown = {}
    head_names = {}
    for salary_rate in salary_rates:
        head = salary_rate.earnings_head
        if (
            salary_rate.from_date <= salary.date <= salary_rate.to_date
            and head.company_id == salary.company_id
            and head.user_id == owner_id
            and head.id not in seen_head_ids
        ):
            # The old implementation used first() for each head. Ordering the
            # bulk query by PK preserves that choice if effective ranges overlap.
            seen_head_ids.add(head.id)
            total += salary_rate.value
            breakdown[head.id] = salary_rate.value
            head_names[head.id] = head.name
    return total, breakdown, head_names


def build_payment_sheet_report(user, request_data, prepared_salaries, output_format):
    prepared_salaries = list(prepared_salaries)
    if not prepared_salaries:
        raise ValueError('Payment sheet requires at least one prepared salary.')
    if output_format not in {'pdf', 'xlsx'}:
        raise ValueError(f'Unsupported payment sheet format: {output_format}')

    company = prepared_salaries[0].company
    report_options = (
        resolve_report_options(company, 'payment_sheet', 'xlsx')
        if output_format == 'xlsx'
        else {'ot_hours_display': 'actual'}
    )
    loaded = _load_payment_sheet_data(
        user,
        prepared_salaries,
        include_weighted_ot=report_options['ot_hours_display'] == 'weighted',
    )
    company_setup = PfEsiSetup.objects.get(company=request_data['company'])
    company_details = getattr(company, 'company_details', None)
    grouped = request_data['filters']['group_by'] != 'none'
    totals = PaymentSheetTotals()
    sections = []
    salary_rate_head_names = {}
    earned_head_names = loaded['earned_head_names']

    for serial, salary in enumerate(prepared_salaries, start=1):
        professional_detail = getattr(salary.employee, 'employee_professional_detail', None)
        department = professional_detail.department if professional_detail else None
        designation = professional_detail.designation if professional_detail else None
        key = (salary.employee_id, salary.date)
        attendance = (
            loaded['user_attendance_by_key'].get(key)
            if output_format == 'pdf'
            else loaded['attendance_by_key'].get(key)
        )
        paid_days = attendance.paid_days_count / 2 if attendance else None
        earned_salary = (
            loaded['earned_salary_by_salary'][salary.id]
            if salary.id in loaded['earned_salary_ids']
            else None
        )
        incentive = salary.incentive_amount
        has_pdf_ot = output_format != 'pdf' or attendance is not None
        actual_ot_hours = salary.net_ot_minutes_monthly / 60 if has_pdf_ot else None
        if (
            has_pdf_ot
            and report_options['ot_hours_display'] == 'weighted'
            and salary.id in loaded['salaries_with_ot_breakdown']
        ):
            ot_hours = float(loaded['weighted_ot_minutes_by_salary'][salary.id] / 60)
        else:
            ot_hours = actual_ot_hours
        ot_amount = salary.net_ot_amount_monthly if has_pdf_ot else None
        salary_rate, salary_rate_breakdown, row_head_names = _salary_rate_for(
            salary,
            loaded['salary_rates_by_employee'][salary.employee_id],
        )
        salary_rate_head_names.update(row_head_names)

        if output_format == 'pdf' and not earned_salary:
            total_earned = None
        else:
            total_earned = (earned_salary or 0) + incentive + (ot_amount or 0)

        advance = salary.advance_deducted
        epf = salary.pf_deducted + salary.vpf_deducted
        esi = salary.esi_deducted
        lwf = salary.labour_welfare_fund_deducted if company_setup.enable_labour_welfare_fund else 0
        others = salary.others_deducted
        tds = salary.tds_deducted
        total_deductions = advance + epf + esi + lwf + others + tds
        net_payable = total_earned - total_deductions if total_earned is not None else None

        row = PaymentSheetRow(
            serial=serial,
            attendance_card_no=salary.employee.attendance_card_no,
            employee_name=salary.employee.name,
            father_or_husband_name=salary.employee.father_or_husband_name or '',
            designation=designation.name if designation else '',
            department_id=department.id if department else None,
            department_name=department.name if department else None,
            salary_rate=salary_rate,
            salary_rate_breakdown=salary_rate_breakdown,
            paid_days=paid_days,
            earned_salary=earned_salary,
            earned_salary_breakdown=loaded['earned_salary_breakdown_by_salary'][salary.id],
            incentive=incentive,
            ot_hours=ot_hours,
            ot_amount=ot_amount,
            total_earned=total_earned,
            advance=advance,
            epf=epf,
            esi=esi,
            lwf=lwf,
            others=others,
            tds=tds,
            total_deductions=total_deductions,
            net_payable=net_payable,
        )
        totals.add(row)

        section_key = row.department_id if grouped else 'all'
        if not sections or sections[-1].department_id != section_key:
            sections.append(PaymentSheetSection(
                department_id=section_key,
                department_name=row.department_name if grouped else None,
                rows=[],
                totals=PaymentSheetTotals(),
            ))
        sections[-1].rows.append(row)
        sections[-1].totals.add(row)

    return PaymentSheetReport(
        company_name=company.name,
        company_address=company_details.address if company_details else '',
        show_lwf=company_setup.enable_labour_welfare_fund,
        grouped=grouped,
        salary_rate_columns=request_data['filters'].get('salary_rate_columns', 'total_only'),
        earned_salary_columns=request_data['filters'].get('earned_salary_columns', 'total_only'),
        salary_rate_heads=tuple(sorted(salary_rate_head_names.items())),
        earned_salary_heads=tuple(sorted(earned_head_names.items())),
        ot_hours_label='OT Hrs',
        sections=sections,
        totals=totals,
    )
