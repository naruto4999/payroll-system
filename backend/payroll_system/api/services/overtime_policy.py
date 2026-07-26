from collections import defaultdict
from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP

from django.db import transaction


STANDARD_OVERTIME_POLICIES = (
    {
        'name': 'No overtime',
        'code': 'NO_OVERTIME',
        'rules': (),
        'earnings_basis': 'ALL_EARNINGS',
        'is_default': True,
    },
    {
        'name': 'All days - single rate',
        'code': 'ALL_DAYS_SINGLE',
        'rules': (('REGULAR', Decimal('1')), ('WEEKLY_OFF', Decimal('1')), ('HOLIDAY', Decimal('1'))),
        'earnings_basis': 'ALL_EARNINGS',
        'is_default': False,
    },
    {
        'name': 'WO/HD - single rate',
        'code': 'WO_HD_SINGLE',
        'rules': (('WEEKLY_OFF', Decimal('1')), ('HOLIDAY', Decimal('1'))),
        'earnings_basis': 'ALL_EARNINGS',
        'is_default': False,
    },
    {
        'name': 'All days - double rate',
        'code': 'ALL_DAYS_DOUBLE',
        'rules': (('REGULAR', Decimal('2')), ('WEEKLY_OFF', Decimal('2')), ('HOLIDAY', Decimal('2'))),
        'earnings_basis': 'ALL_EARNINGS',
        'is_default': False,
    },
    {
        'name': 'WO/HD - double rate',
        'code': 'WO_HD_DOUBLE',
        'rules': (('WEEKLY_OFF', Decimal('2')), ('HOLIDAY', Decimal('2'))),
        'earnings_basis': 'ALL_EARNINGS',
        'is_default': False,
    },
)


LEGACY_POLICY_CODE_BY_SETTINGS = {
    ('no_overtime', None): 'NO_OVERTIME',
    ('no_overtime', ''): 'NO_OVERTIME',
    ('no_overtime', 'S'): 'NO_OVERTIME',
    ('no_overtime', 'D'): 'NO_OVERTIME',
    ('all_days', None): 'ALL_DAYS_SINGLE',
    ('all_days', ''): 'ALL_DAYS_SINGLE',
    ('all_days', 'S'): 'ALL_DAYS_SINGLE',
    ('all_days', 'D'): 'ALL_DAYS_DOUBLE',
    ('holiday_weekly_off', None): 'WO_HD_SINGLE',
    ('holiday_weekly_off', ''): 'WO_HD_SINGLE',
    ('holiday_weekly_off', 'S'): 'WO_HD_SINGLE',
    ('holiday_weekly_off', 'D'): 'WO_HD_DOUBLE',
}


@transaction.atomic
def ensure_standard_overtime_policies(company):
    from api.models import OvertimePolicy, OvertimePolicyDayRule

    existing_default = OvertimePolicy.objects.filter(company=company, is_default=True, is_active=True).first()
    policies = {}
    for definition in STANDARD_OVERTIME_POLICIES:
        defaults = {
            'name': definition['name'],
            'is_active': True,
            'is_system': True,
            'earnings_basis': definition['earnings_basis'],
            'is_default': definition['is_default'] and existing_default is None,
        }
        policy, _ = OvertimePolicy.objects.get_or_create(
            company=company,
            code=definition['code'],
            defaults=defaults,
        )
        changed = False
        for field, value in defaults.items():
            if getattr(policy, field) != value and field != 'is_default':
                setattr(policy, field, value)
                changed = True
        if definition['is_default'] and existing_default is None and not policy.is_default:
            policy.is_default = True
            changed = True
        if changed:
            policy.save()

        for priority, (day_type, multiplier) in enumerate(definition['rules'], start=1):
            OvertimePolicyDayRule.objects.update_or_create(
                policy=policy,
                day_type=day_type,
                defaults={
                    'multiplier': multiplier,
                    'late_deduction_priority': priority,
                },
            )
        policy.day_rules.exclude(day_type__in=[rule[0] for rule in definition['rules']]).delete()
        policies[definition['code']] = policy
    return policies


def policy_for_legacy_settings(company, overtime_type, overtime_rate):
    code = LEGACY_POLICY_CODE_BY_SETTINGS.get((overtime_type, overtime_rate))
    if code is None:
        raise ValueError(f'Unknown overtime settings: type={overtime_type!r}, rate={overtime_rate!r}')
    return ensure_standard_overtime_policies(company)[code]


def resolve_employee_overtime_policy(employee_salary_detail):
    if employee_salary_detail.overtime_policy_id:
        return employee_salary_detail.overtime_policy
    return policy_for_legacy_settings(
        employee_salary_detail.company,
        employee_salary_detail.overtime_type,
        employee_salary_detail.overtime_rate,
    )


def classify_attendance_day(attendance):
    first = attendance.first_half.name
    second = attendance.second_half.name
    names = {first, second}
    if any(name in ('HD', 'HD*') for name in names):
        return 'HOLIDAY'
    if any(name in ('WO', 'WO*') for name in names):
        return 'WEEKLY_OFF'
    return 'REGULAR'


def rounded_ot_minutes(minutes):
    return (minutes // 30) * 30 + (30 if minutes % 30 >= 20 else 0)


def resolve_overtime_divisor(user, company_calculations, days_in_month):
    if user.role == 'REGULAR':
        return Decimal(26)
    if company_calculations.ot_calculation == 'month_days':
        return Decimal(days_in_month)
    return Decimal(company_calculations.ot_calculation)


@dataclass
class OvertimeCalculationResult:
    net_minutes: int
    amount: Decimal
    breakdown: list


def calculate_policy_overtime(
    *,
    employee_salary_detail,
    attendance_records,
    salary_earnings,
    company_calculations,
    user,
    days_in_month,
):
    policy = resolve_employee_overtime_policy(employee_salary_detail)
    rules = {rule.day_type: rule for rule in policy.day_rules.all()}
    if not rules:
        return OvertimeCalculationResult(net_minutes=0, amount=Decimal('0'), breakdown=[])

    selected_head_ids = None
    if policy.earnings_basis == 'SELECTED_HEADS':
        selected_head_ids = set(policy.selected_earning_heads.values_list('earnings_head_id', flat=True))
    eligible_salary_rate = sum(
        Decimal(earning.value)
        for earning in salary_earnings
        if selected_head_ids is None or earning.earnings_head_id in selected_head_ids
    )
    if eligible_salary_rate <= 0:
        return OvertimeCalculationResult(net_minutes=0, amount=Decimal('0'), breakdown=[])

    minutes_by_day_type = defaultdict(int)
    late_minutes = 0
    for attendance in attendance_records:
        if attendance.ot_min:
            day_type = classify_attendance_day(attendance)
            if day_type in rules:
                minutes_by_day_type[day_type] += attendance.ot_min
        if attendance.late_min:
            late_minutes += attendance.late_min

    rounded_late_minutes = 0
    if employee_salary_detail.late_deduction and user.role == 'OWNER':
        rounded_late_minutes = rounded_ot_minutes(late_minutes)

    divisor = resolve_overtime_divisor(user, company_calculations, days_in_month)
    breakdown = []
    total_net_minutes = 0
    total_amount = Decimal('0')

    for rule in sorted(rules.values(), key=lambda current_rule: current_rule.late_deduction_priority):
        gross_minutes = rounded_ot_minutes(minutes_by_day_type.get(rule.day_type, 0))
        deducted_late_minutes = min(gross_minutes, rounded_late_minutes)
        rounded_late_minutes -= deducted_late_minutes
        net_minutes = gross_minutes - deducted_late_minutes
        if net_minutes == 0 and gross_minutes == 0:
            continue

        hours = Decimal(net_minutes) / Decimal(60)
        multiplier = Decimal('2') if user.role == 'REGULAR' else rule.multiplier
        if employee_salary_detail.salary_mode.lower() == 'daily':
            amount = eligible_salary_rate / Decimal(8) * hours * multiplier
            amount_divisor = Decimal(1)
        else:
            amount = eligible_salary_rate / divisor / Decimal(8) * hours * multiplier
            amount_divisor = divisor
        amount = amount.quantize(Decimal('1.'), rounding=ROUND_HALF_UP)

        total_net_minutes += net_minutes
        total_amount += amount
        breakdown.append({
            'day_type': rule.day_type,
            'gross_minutes': gross_minutes,
            'deducted_late_minutes': deducted_late_minutes,
            'net_minutes': net_minutes,
            'multiplier': multiplier,
            'eligible_salary_rate': eligible_salary_rate.quantize(Decimal('0.01')),
            'divisor': amount_divisor.quantize(Decimal('0.01')),
            'amount': int(amount),
        })

    return OvertimeCalculationResult(net_minutes=total_net_minutes, amount=total_amount, breakdown=breakdown)
