from collections import defaultdict
from dataclasses import dataclass
from datetime import date, timedelta
from decimal import Decimal, ROUND_HALF_UP
from uuid import uuid4

from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models.deletion import ProtectedError
from rest_framework.exceptions import APIException


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
        'name': 'Regular days - single rate',
        'code': 'REGULAR_DAYS_SINGLE',
        'rules': (('REGULAR', Decimal('1')),),
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
        'name': 'Regular days - double rate',
        'code': 'REGULAR_DAYS_DOUBLE',
        'rules': (('REGULAR', Decimal('2')),),
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


class OvertimePolicyConfigurationError(APIException):
    """Raised when overtime cannot be resolved from persisted policy configuration."""

    status_code = 400
    default_code = 'invalid_overtime_policy_configuration'

    def __init__(self, message, *, code):
        self.code = code
        super().__init__({'code': code, 'detail': message})


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
            'rounding_increment_minutes': 30,
            'round_up_from_minutes': 16,
        }
        policy, _ = OvertimePolicy.objects.get_or_create(
            company=company,
            code=definition['code'],
            defaults=defaults,
        )
        changed = False
        for field, value in defaults.items():
            if getattr(policy, field) != value and field not in (
                'is_default', 'rounding_increment_minutes', 'round_up_from_minutes'
            ):
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


def get_company_default_overtime_policy(*, company):
    from api.models import OvertimePolicy

    policy = OvertimePolicy.objects.filter(
        company=company,
        is_default=True,
        is_active=True,
    ).first()
    if policy is None:
        raise OvertimePolicyConfigurationError(
            'The company does not have an active default overtime policy.',
            code='missing_active_default',
        )
    return policy


def resolve_employee_overtime_policy(employee_salary_detail):
    if (
        employee_salary_detail.employee.company_id != employee_salary_detail.company_id
        or employee_salary_detail.employee.user_id != employee_salary_detail.user_id
        or employee_salary_detail.company.user_id != employee_salary_detail.user_id
    ):
        raise OvertimePolicyConfigurationError(
            'The employee salary detail has inconsistent company ownership.',
            code='invalid_salary_detail_scope',
        )
    if employee_salary_detail.overtime_policy_id:
        policy = employee_salary_detail.overtime_policy
        if policy.company_id != employee_salary_detail.company_id:
            raise OvertimePolicyConfigurationError(
                'The assigned overtime policy belongs to another company.',
                code='cross_company_policy',
            )
        return policy
    return get_company_default_overtime_policy(company=employee_salary_detail.company)


def resolve_calculation_overtime_policy(*, actor, employee_salary_detail):
    from api.models import OvertimePolicy, OvertimePolicyDayRule

    company = employee_salary_detail.company
    actor_owner_id = actor.id
    if actor.role == 'REGULAR' and actor.id != company.user_id:
        actor_owner_id = getattr(getattr(actor, 'regular_to_owner', None), 'owner_id', None)
    if actor_owner_id != company.user_id:
        raise OvertimePolicyConfigurationError(
            'The employee does not belong to the authenticated account scope.',
            code='cross_company_resolution',
        )

    if actor.role != 'REGULAR':
        return resolve_employee_overtime_policy(employee_salary_detail)

    policy = OvertimePolicy.objects.filter(
        company=company,
        code='ALL_DAYS_DOUBLE',
        is_system=True,
        is_active=True,
    ).first()
    if policy is None:
        raise OvertimePolicyConfigurationError(
            'The company ALL_DAYS_DOUBLE system policy is missing or inactive.',
            code='missing_all_days_double',
        )

    rules = list(policy.day_rules.all())
    expected_priorities = {
        OvertimePolicyDayRule.DAY_TYPE_REGULAR: 1,
        OvertimePolicyDayRule.DAY_TYPE_WEEKLY_OFF: 2,
        OvertimePolicyDayRule.DAY_TYPE_HOLIDAY: 3,
    }
    if (
        policy.name != 'All days - double rate'
        or policy.earnings_basis != OvertimePolicy.EARNINGS_BASIS_ALL
        or policy.selected_earning_heads.exists()
        or {rule.day_type: rule.late_deduction_priority for rule in rules} != expected_priorities
        or any(rule.multiplier != Decimal('2') for rule in rules)
    ):
        raise OvertimePolicyConfigurationError(
            'The company ALL_DAYS_DOUBLE system policy is malformed.',
            code='malformed_all_days_double',
        )
    return policy


def _lock_owned_company(*, actor, company):
    from api.models import Company

    if actor.role != 'OWNER':
        raise ValidationError('Only owner accounts can manage overtime policies.')
    try:
        return Company.objects.select_for_update().get(pk=company.pk, user=actor)
    except Company.DoesNotExist as exc:
        raise ValidationError('Company is not owned by the authenticated account.') from exc


def _assert_one_active_default(*, company):
    from api.models import OvertimePolicy

    if OvertimePolicy.objects.filter(company=company, is_default=True, is_active=True).count() != 1:
        raise ValidationError({'is_default': 'The company must have exactly one active default overtime policy.'})


def _validate_mutation_state(*, company, policy, validated_data, day_rules, selected_heads, creating=False):
    from api.models import OvertimePolicy

    forbidden_fields = {'company', 'code', 'is_system'} & set(validated_data)
    if forbidden_fields:
        raise ValidationError({field: 'This field is managed by the system.' for field in forbidden_fields})

    resulting_default = validated_data.get('is_default', False if creating else policy.is_default)
    resulting_active = validated_data.get('is_active', True if creating else policy.is_active)
    if resulting_default and not resulting_active:
        raise ValidationError({'is_default': 'An inactive policy cannot be the company default.'})
    if not creating and policy.is_default and not resulting_default:
        raise ValidationError({'is_default': 'Select another default instead of clearing the active default.'})

    resulting_increment = validated_data.get(
        'rounding_increment_minutes', 30 if creating else policy.rounding_increment_minutes
    )
    resulting_threshold = validated_data.get(
        'round_up_from_minutes', 16 if creating else policy.round_up_from_minutes
    )
    if resulting_increment <= 0:
        raise ValidationError({'rounding_increment_minutes': 'Rounding increment must be greater than zero.'})
    if resulting_threshold < 1:
        raise ValidationError({'round_up_from_minutes': 'Round-up threshold must be at least 1.'})
    if resulting_threshold > resulting_increment:
        raise ValidationError({'round_up_from_minutes': 'Round-up threshold cannot exceed the rounding increment.'})

    if day_rules is not None:
        day_types = [rule['day_type'] for rule in day_rules]
        priorities = [rule['late_deduction_priority'] for rule in day_rules]
        if len(day_types) != len(set(day_types)):
            raise ValidationError({'day_rules': 'Day types must be unique.'})
        if len(priorities) != len(set(priorities)):
            raise ValidationError({'day_rules': 'Late-deduction priorities must be unique.'})
        if any(priority < 1 for priority in priorities):
            raise ValidationError({'day_rules': 'Late-deduction priorities must be at least 1.'})

    if selected_heads is not None:
        if len(selected_heads) != len({head.pk for head in selected_heads}):
            raise ValidationError({'selected_earning_head_ids': 'Selected earning heads must be unique.'})
        if any(head.company_id != company.pk for head in selected_heads):
            raise ValidationError({'selected_earning_head_ids': 'All selected earning heads must belong to the policy company.'})

    previous_basis = None if creating else policy.earnings_basis
    resulting_basis = validated_data.get('earnings_basis', previous_basis or OvertimePolicy.EARNINGS_BASIS_ALL)
    resulting_heads = selected_heads
    if resulting_heads is None and not creating:
        resulting_heads = [link.earnings_head for link in policy.selected_earning_heads.select_related('earnings_head')]
    resulting_heads = resulting_heads or []
    if resulting_basis == OvertimePolicy.EARNINGS_BASIS_SELECTED:
        if previous_basis != OvertimePolicy.EARNINGS_BASIS_SELECTED and selected_heads is None:
            raise ValidationError({'selected_earning_head_ids': 'A non-empty list is required when selecting SELECTED_HEADS.'})
        if not resulting_heads:
            raise ValidationError({'selected_earning_head_ids': 'At least one earning head is required for SELECTED_HEADS.'})
    else:
        selected_heads = []

    if not creating and policy.is_system:
        protected = ('name', 'is_active', 'earnings_basis')
        changed = [field for field in protected if field in validated_data and validated_data[field] != getattr(policy, field)]
        if day_rules is not None:
            changed.append('day_rules')
        current_head_ids = list(policy.selected_earning_heads.values_list('earnings_head_id', flat=True))
        if selected_heads is not None and [head.pk for head in selected_heads] != current_head_ids:
            changed.append('selected_earning_head_ids')
        if changed:
            raise ValidationError({field: 'System policy definitions cannot be changed.' for field in changed})
    return selected_heads


def _replace_policy_relations(*, policy, day_rules, selected_heads):
    from api.models import OvertimePolicyDayRule, OvertimePolicyEarningsHead

    if day_rules is not None:
        policy.day_rules.all().delete()
        OvertimePolicyDayRule.objects.bulk_create(
            [OvertimePolicyDayRule(policy=policy, **rule) for rule in day_rules]
        )
    if selected_heads is not None:
        policy.selected_earning_heads.all().delete()
        OvertimePolicyEarningsHead.objects.bulk_create(
            [OvertimePolicyEarningsHead(policy=policy, earnings_head=head) for head in selected_heads]
        )


@transaction.atomic
def create_overtime_policy(*, actor, company, validated_data, day_rules, selected_heads):
    from api.models import OvertimePolicy

    company = _lock_owned_company(actor=actor, company=company)
    selected_heads = _validate_mutation_state(
        company=company,
        policy=None,
        validated_data=validated_data,
        day_rules=day_rules,
        selected_heads=selected_heads,
        creating=True,
    )
    if validated_data.get('is_default'):
        OvertimePolicy.objects.filter(company=company, is_default=True).update(is_default=False)
    policy = OvertimePolicy.objects.create(
        company=company,
        code=f'CUSTOM_{uuid4()}',
        **validated_data,
    )
    _replace_policy_relations(policy=policy, day_rules=day_rules, selected_heads=selected_heads)
    _assert_one_active_default(company=company)
    return policy


@transaction.atomic
def update_overtime_policy(*, actor, company, policy, validated_data, day_rules, selected_heads):
    from api.models import OvertimePolicy

    company = _lock_owned_company(actor=actor, company=company)
    try:
        policy = OvertimePolicy.objects.select_for_update().get(pk=policy.pk, company=company)
    except OvertimePolicy.DoesNotExist as exc:
        raise ValidationError('The overtime policy no longer exists.') from exc
    selected_heads = _validate_mutation_state(
        company=company,
        policy=policy,
        validated_data=validated_data,
        day_rules=day_rules,
        selected_heads=selected_heads,
    )
    if validated_data.get('is_default'):
        OvertimePolicy.objects.filter(company=company, is_default=True).exclude(pk=policy.pk).update(is_default=False)
    for field, value in validated_data.items():
        setattr(policy, field, value)
    policy.save()
    _replace_policy_relations(policy=policy, day_rules=day_rules, selected_heads=selected_heads)
    _assert_one_active_default(company=company)
    return policy


@transaction.atomic
def delete_overtime_policy(*, actor, company, policy):
    company = _lock_owned_company(actor=actor, company=company)
    try:
        policy = type(policy).objects.select_for_update().get(pk=policy.pk, company=company)
    except type(policy).DoesNotExist as exc:
        raise ValidationError('The overtime policy no longer exists.') from exc
    if policy.is_system:
        raise ValidationError('System overtime policies cannot be deleted.')
    if policy.is_default:
        raise ValidationError('Select another default before deleting this overtime policy.')
    try:
        policy.delete()
    except ProtectedError as exc:
        raise ValidationError('An assigned overtime policy cannot be deleted.') from exc
    _assert_one_active_default(company=company)


def rounded_ot_minutes(minutes, increment=30, round_up_from=16):
    if increment <= 0:
        raise ValueError('Rounding increment must be greater than zero.')
    if round_up_from < 1 or round_up_from > increment:
        raise ValueError('Round-up threshold must be between 1 and the rounding increment.')
    if minutes < 0:
        raise ValueError('Overtime minutes cannot be negative.')
    return (minutes // increment) * increment + (increment if minutes % increment >= round_up_from else 0)


def resolve_overtime_divisor(user, company_calculations, days_in_month):
    if user.role == 'REGULAR':
        return Decimal(26)
    if company_calculations is None:
        raise OvertimePolicyConfigurationError(
            'The company overtime calculation configuration is missing.',
            code='missing_company_calculations',
        )
    if company_calculations.ot_calculation == 'month_days':
        divisor = Decimal(days_in_month)
    else:
        try:
            divisor = Decimal(company_calculations.ot_calculation)
        except (TypeError, ValueError, ArithmeticError) as exc:
            raise OvertimePolicyConfigurationError(
                'The company overtime divisor is invalid.',
                code='invalid_overtime_divisor',
            ) from exc
    if not divisor.is_finite() or divisor <= 0:
        raise OvertimePolicyConfigurationError(
            'The company overtime divisor must be greater than zero.',
            code='invalid_overtime_divisor',
        )
    return divisor


@dataclass
class OvertimeCalculationResult:
    policy_id: int
    policy_code: str
    policy_name: str
    policy_resolution: str
    earnings_basis: str
    selected_earning_head_ids: tuple
    net_minutes: int
    amount: Decimal
    breakdown: list
    rounding_increment_minutes: int
    round_up_from_minutes: int
    period_start: date
    period_end: date
    raw_eligible_minutes: int
    rounded_gross_minutes: int
    deducted_late_minutes: int
    group_diagnostics: list

    @property
    def total_raw_eligible_minutes(self):
        return self.raw_eligible_minutes

    @property
    def total_rounded_gross_minutes(self):
        return self.rounded_gross_minutes

    @property
    def policy_eligible_gross_minutes(self):
        return sum(row['gross_minutes'] for row in self.breakdown if row['eligible'])

    @property
    def total_deducted_late_minutes(self):
        return self.deducted_late_minutes

    @property
    def total_net_minutes(self):
        return self.net_minutes

    @property
    def total_amount(self):
        return self.amount

    @property
    def effective_policy(self):
        return {
            'id': self.policy_id,
            'code': self.policy_code,
            'name': self.policy_name,
            'resolution': self.policy_resolution,
            'earnings_basis': self.earnings_basis,
            'selected_earning_head_ids': list(self.selected_earning_head_ids),
            'rounding_increment_minutes': self.rounding_increment_minutes,
            'round_up_from_minutes': self.round_up_from_minutes,
        }

    @property
    def snapshot_breakdown(self):
        fields = (
            'day_type',
            'gross_minutes',
            'deducted_late_minutes',
            'net_minutes',
            'multiplier',
            'eligible_salary_rate',
            'divisor',
            'amount',
        )
        return [
            {field: row[field] for field in fields}
            for row in self.breakdown
            if row['eligible'] and (row['gross_minutes'] or row['deducted_late_minutes'])
        ]


OVERTIME_DAY_TYPES = ('REGULAR', 'WEEKLY_OFF', 'HOLIDAY')
OVERTIME_DAY_TYPE_ORDER = {day_type: index for index, day_type in enumerate(OVERTIME_DAY_TYPES)}


def _configuration_error(message, code):
    raise OvertimePolicyConfigurationError(message, code=code)


def _validate_policy_calculation_state(policy):
    increment = policy.rounding_increment_minutes
    threshold = policy.round_up_from_minutes
    if increment is None or increment <= 0 or threshold is None or threshold < 1 or threshold > increment:
        _configuration_error('The overtime policy rounding configuration is invalid.', 'invalid_rounding_configuration')

    rules = list(policy.day_rules.all())
    day_types = [rule.day_type for rule in rules]
    priorities = [rule.late_deduction_priority for rule in rules]
    if (
        len(day_types) != len(set(day_types))
        or len(priorities) != len(set(priorities))
        or any(day_type not in OVERTIME_DAY_TYPES for day_type in day_types)
        or any(priority < 1 or rule.multiplier <= 0 for priority, rule in zip(priorities, rules))
    ):
        _configuration_error('The overtime policy category rules are invalid.', 'invalid_policy_rules')
    return tuple({
        'day_type': rule.day_type,
        'multiplier': rule.multiplier,
        'late_deduction_priority': rule.late_deduction_priority,
    } for rule in rules)


def _selected_head_ids(policy):
    from api.models import OvertimePolicy

    links = list(policy.selected_earning_heads.select_related('earnings_head'))
    if any(link.earnings_head.company_id != policy.company_id for link in links):
        _configuration_error('A selected overtime earnings head belongs to another company.', 'cross_company_selected_head')
    if policy.earnings_basis == OvertimePolicy.EARNINGS_BASIS_SELECTED:
        if not links:
            _configuration_error('SELECTED_HEADS overtime policies require at least one earnings head.', 'empty_selected_heads')
        return tuple(link.earnings_head_id for link in links)
    if policy.earnings_basis != OvertimePolicy.EARNINGS_BASIS_ALL:
        _configuration_error('The overtime policy earnings basis is invalid.', 'invalid_earnings_basis')
    return ()


def _eligible_salary_rate(*, salary_earnings, selected_head_ids, employee_salary_detail):
    selected_head_ids = set(selected_head_ids)
    rate = Decimal('0')
    matched_selected_heads = set()
    for earning in salary_earnings:
        if (
            earning.employee_id != employee_salary_detail.employee_id
            or earning.company_id != employee_salary_detail.company_id
            or earning.user_id != employee_salary_detail.user_id
            or earning.earnings_head.company_id != employee_salary_detail.company_id
        ):
            _configuration_error('An overtime salary earning is outside the employee account scope.', 'invalid_earning_scope')
        if not selected_head_ids or earning.earnings_head_id in selected_head_ids:
            rate += Decimal(earning.value)
            matched_selected_heads.add(earning.earnings_head_id)
    return rate, matched_selected_heads


def _calculate_overtime_core(
    *,
    policy_id,
    policy_code,
    policy_name,
    policy_resolution,
    earnings_basis,
    rounding_increment_minutes,
    round_up_from_minutes,
    rules,
    selected_head_ids,
    eligible_salary_rate,
    detail_facts,
    late_minutes,
    deduct_late,
    salary_mode,
    divisor,
    period_start,
    period_end,
):
    grouped_minutes = defaultdict(int)
    for fact in detail_facts:
        grouped_minutes[(fact['attendance_id'], fact['work_date'], fact['day_type'])] += fact['eligible_minutes']

    rules_by_day_type = {rule['day_type']: rule for rule in rules}
    group_diagnostics = []
    rounded_by_day_type = defaultdict(int)
    raw_by_day_type = defaultdict(int)
    multiplier_buckets = defaultdict(list)
    for (attendance_id, work_date, day_type), raw_minutes in sorted(grouped_minutes.items()):
        raw_by_day_type[day_type] += raw_minutes
        component = {
            'attendance_id': attendance_id,
            'work_date': work_date,
            'day_type': day_type,
            'raw_eligible_minutes': raw_minutes,
        }
        rule = rules_by_day_type.get(day_type)
        if rule is None:
            rounded_minutes = rounded_ot_minutes(
                raw_minutes,
                rounding_increment_minutes,
                round_up_from_minutes,
            )
            rounded_by_day_type[day_type] += rounded_minutes
            group_diagnostics.append({
                **component,
                'multiplier': None,
                'rounding_bucket_raw_minutes': raw_minutes,
                'rounding_bucket_rounded_minutes': rounded_minutes,
                'rounded_gross_minutes': rounded_minutes,
            })
            continue
        multiplier_buckets[(attendance_id, rule['multiplier'])].append(component)

    for (attendance_id, multiplier), components in sorted(multiplier_buckets.items()):
        bucket_raw_minutes = sum(component['raw_eligible_minutes'] for component in components)
        bucket_rounded_minutes = rounded_ot_minutes(
            bucket_raw_minutes,
            rounding_increment_minutes,
            round_up_from_minutes,
        )
        allocated_minutes = [component['raw_eligible_minutes'] for component in components]
        allocation_order = sorted(
            range(len(components)),
            key=lambda index: (
                -components[index]['raw_eligible_minutes'],
                components[index]['work_date'],
                OVERTIME_DAY_TYPE_ORDER[components[index]['day_type']],
            ),
        )
        rounding_delta = bucket_rounded_minutes - bucket_raw_minutes
        if rounding_delta > 0:
            allocated_minutes[allocation_order[0]] += rounding_delta
        elif rounding_delta < 0:
            remaining_reduction = -rounding_delta
            for index in allocation_order:
                reduction = min(allocated_minutes[index], remaining_reduction)
                allocated_minutes[index] -= reduction
                remaining_reduction -= reduction
                if remaining_reduction == 0:
                    break

        for component, rounded_minutes in zip(components, allocated_minutes):
            rounded_by_day_type[component['day_type']] += rounded_minutes
            group_diagnostics.append({
                **component,
                'multiplier': multiplier,
                'rounding_bucket_raw_minutes': bucket_raw_minutes,
                'rounding_bucket_rounded_minutes': bucket_rounded_minutes,
                'rounded_gross_minutes': rounded_minutes,
            })

    group_diagnostics.sort(key=lambda item: (
        item['attendance_id'],
        item['work_date'],
        OVERTIME_DAY_TYPE_ORDER[item['day_type']],
    ))

    # Late deductions use the approved fixed 30/20 rule, independently of
    # the overtime policy's configurable gross-minute rounding.
    remaining_late_minutes = rounded_ot_minutes(late_minutes, 30, 20) if deduct_late else 0
    deducted_by_day_type = defaultdict(int)
    for rule in sorted(rules, key=lambda item: item['late_deduction_priority']):
        deduction = min(rounded_by_day_type[rule['day_type']], remaining_late_minutes)
        deducted_by_day_type[rule['day_type']] = deduction
        remaining_late_minutes -= deduction

    amount_divisor = Decimal('1') if salary_mode == 'daily' else divisor
    breakdown = []
    total_net_minutes = 0
    total_deducted_late_minutes = 0
    total_amount = Decimal('0')
    for day_type in OVERTIME_DAY_TYPES:
        rule = rules_by_day_type.get(day_type)
        eligible = rule is not None
        gross_minutes = rounded_by_day_type[day_type]
        deducted_late_minutes = deducted_by_day_type[day_type] if eligible else 0
        net_minutes = max(gross_minutes - deducted_late_minutes, 0) if eligible else 0
        multiplier = rule['multiplier'] if eligible else Decimal('0')
        amount = Decimal('0')
        if net_minutes:
            hours = Decimal(net_minutes) / Decimal(60)
            amount = (eligible_salary_rate * hours * multiplier) / amount_divisor / Decimal(8)
            amount = amount.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        total_net_minutes += net_minutes
        total_deducted_late_minutes += deducted_late_minutes
        total_amount += amount
        breakdown.append({
            'day_type': day_type,
            'eligible': eligible,
            'raw_eligible_minutes': raw_by_day_type[day_type],
            'rounded_gross_minutes': gross_minutes,
            'gross_minutes': gross_minutes,
            'deducted_late_minutes': deducted_late_minutes,
            'net_minutes': net_minutes,
            'multiplier': multiplier,
            'eligible_salary_rate': eligible_salary_rate.quantize(Decimal('0.01')),
            'divisor': amount_divisor.quantize(Decimal('0.01')),
            'amount': amount,
        })

    total_amount = total_amount.quantize(Decimal('1'), rounding=ROUND_HALF_UP)

    return OvertimeCalculationResult(
        policy_id=policy_id,
        policy_code=policy_code,
        policy_name=policy_name,
        policy_resolution=policy_resolution,
        earnings_basis=earnings_basis,
        selected_earning_head_ids=tuple(selected_head_ids),
        net_minutes=total_net_minutes,
        amount=total_amount,
        breakdown=breakdown,
        rounding_increment_minutes=rounding_increment_minutes,
        round_up_from_minutes=round_up_from_minutes,
        period_start=period_start,
        period_end=period_end,
        raw_eligible_minutes=sum(raw_by_day_type.values()),
        rounded_gross_minutes=sum(rounded_by_day_type.values()),
        deducted_late_minutes=total_deducted_late_minutes,
        group_diagnostics=group_diagnostics,
    )


def _calculate_loaded_overtime(
    *,
    employee_salary_detail,
    detail_records,
    attendance_records,
    salary_earnings,
    company_calculations,
    user,
    period_start,
    period_end,
):
    if (
        employee_salary_detail.employee.company_id != employee_salary_detail.company_id
        or employee_salary_detail.employee.user_id != employee_salary_detail.user_id
        or employee_salary_detail.company.user_id != employee_salary_detail.user_id
    ):
        _configuration_error('The employee salary detail has inconsistent company ownership.', 'invalid_salary_detail_scope')
    if company_calculations is not None and (
        company_calculations.company_id != employee_salary_detail.company_id
        or company_calculations.user_id != employee_salary_detail.user_id
    ):
        _configuration_error('The company calculation settings are outside the employee scope.', 'invalid_calculation_scope')
    policy = resolve_calculation_overtime_policy(actor=user, employee_salary_detail=employee_salary_detail)
    rules = _validate_policy_calculation_state(policy)
    selected_head_ids = _selected_head_ids(policy)
    salary_mode = employee_salary_detail.salary_mode.lower()
    if salary_mode not in ('daily', 'monthly'):
        _configuration_error('The employee salary mode does not support overtime calculation.', 'unsupported_salary_mode')

    attendance_records = list(attendance_records)
    detail_records = list(detail_records)
    from api.models import EmployeeAttendanceOvertimeDetail

    attendance_by_scope = {
        (attendance.employee_id, attendance.date, attendance.user_id): attendance
        for attendance in attendance_records
    }
    attendance_relation = EmployeeAttendanceOvertimeDetail._meta.get_field('attendance')
    for detail in detail_records:
        attendance = attendance_by_scope.get((detail.employee_id, detail.attendance_date, detail.user_id))
        if attendance is not None:
            attendance_relation.set_cached_value(detail, attendance)
    attendance_keys_with_details = {(detail.attendance.id, detail.attendance.date) for detail in detail_records}
    for attendance in attendance_records:
        if (
            attendance.user_id != user.pk
            or attendance.company_id != employee_salary_detail.company_id
            or attendance.employee_id != employee_salary_detail.employee_id
        ):
            _configuration_error('An attendance row is outside the employee calculation scope.', 'invalid_attendance_scope')
        attendance_key = (attendance.id, attendance.date)
        has_any_details = attendance.overtime_details.exists() if attendance_key not in attendance_keys_with_details else True
        if attendance.ot_min and not has_any_details:
            _configuration_error(
                f'Attendance {attendance.id} on {attendance.date} has positive overtime but no categorized details.',
                'unbackfilled_overtime',
            )

    detail_facts = []
    for detail in detail_records:
        attendance = detail.attendance
        if (
            attendance.user_id != user.pk
            or attendance.company_id != employee_salary_detail.company_id
            or attendance.employee_id != employee_salary_detail.employee_id
        ):
            _configuration_error('An overtime detail is outside the employee calculation scope.', 'invalid_overtime_detail_scope')
        if not period_start <= attendance.date <= period_end:
            _configuration_error(
                'An overtime detail belongs to an attendance row outside the calculation period.',
                'unsupported_overtime_attendance_date',
            )
        if detail.day_type not in OVERTIME_DAY_TYPES or detail.eligible_minutes <= 0:
            _configuration_error('An overtime detail has invalid calculation facts.', 'invalid_overtime_detail')
        detail_facts.append({
            'attendance_id': detail.attendance.id,
            'work_date': detail.work_date,
            'day_type': detail.day_type,
            'eligible_minutes': detail.eligible_minutes,
        })

    eligible_salary_rate, matched_selected_heads = _eligible_salary_rate(
        salary_earnings=salary_earnings,
        selected_head_ids=selected_head_ids,
        employee_salary_detail=employee_salary_detail,
    )
    payable_day_types = {rule['day_type'] for rule in rules}
    payable_groups = defaultdict(int)
    for fact in detail_facts:
        if fact['day_type'] in payable_day_types:
            payable_groups[(fact['attendance_id'], fact['work_date'], fact['day_type'])] += fact['eligible_minutes']
    rounded_payable_minutes = sum(
        rounded_ot_minutes(
            minutes,
            policy.rounding_increment_minutes,
            policy.round_up_from_minutes,
        )
        for minutes in payable_groups.values()
    )
    if rounded_payable_minutes and selected_head_ids and not matched_selected_heads:
        _configuration_error('No applicable employee rate exists for the selected overtime earnings heads.', 'missing_selected_earning_rate')
    if rounded_payable_minutes and eligible_salary_rate <= 0:
        _configuration_error('The eligible overtime salary rate must be greater than zero.', 'non_positive_eligible_salary_rate')

    divisor = resolve_overtime_divisor(user, company_calculations, (period_end - period_start).days + 1)
    policy_resolution = 'FORCED_REGULAR' if user.role == 'REGULAR' else (
        'EXPLICIT' if employee_salary_detail.overtime_policy_id else 'INHERITED_DEFAULT'
    )
    return _calculate_overtime_core(
        policy_id=policy.pk,
        policy_code=policy.code,
        policy_name=policy.name,
        policy_resolution=policy_resolution,
        earnings_basis=policy.earnings_basis,
        rounding_increment_minutes=policy.rounding_increment_minutes,
        round_up_from_minutes=policy.round_up_from_minutes,
        rules=rules,
        selected_head_ids=selected_head_ids,
        eligible_salary_rate=eligible_salary_rate,
        detail_facts=detail_facts,
        late_minutes=sum(attendance.late_min or 0 for attendance in attendance_records),
        deduct_late=employee_salary_detail.late_deduction and user.role == 'OWNER',
        salary_mode=salary_mode,
        divisor=divisor,
        period_start=period_start,
        period_end=period_end,
    )


def calculate_employee_overtime(*, actor, company, employee, period_start):
    from api.models import (
        Calculations,
        EmployeeAttendance,
        EmployeeAttendanceOvertimeDetail,
        EmployeeSalaryDetail,
        EmployeeSalaryEarning,
    )

    if not getattr(actor, 'is_authenticated', False):
        _configuration_error('Authentication is required for overtime calculation.', 'authentication_required')
    if not isinstance(period_start, date) or period_start.day != 1:
        _configuration_error('The overtime period must start on the first day of a month.', 'invalid_overtime_period')
    owner = actor if actor.role == 'OWNER' else getattr(getattr(actor, 'regular_to_owner', None), 'owner', None)
    if owner is None or company.user_id != owner.pk:
        _configuration_error('The company is outside the authenticated account scope.', 'cross_company_resolution')
    if employee.company_id != company.pk or employee.user_id != owner.pk:
        _configuration_error('The employee is outside the company account scope.', 'invalid_employee_scope')
    if actor.role == 'REGULAR' and (not company.visible or not employee.visible):
        _configuration_error('The employee is not visible to the authenticated regular account.', 'employee_not_visible')
    if actor.role not in ('OWNER', 'REGULAR'):
        _configuration_error('The authenticated account role is unsupported.', 'unsupported_account_role')

    period_end = period_start.replace(day=28) + timedelta(days=4)
    period_end = period_end.replace(day=1) - timedelta(days=1)
    try:
        employee_salary_detail = EmployeeSalaryDetail.objects.select_related(
            'employee', 'company', 'overtime_policy'
        ).get(user=owner, company=company, employee=employee)
    except EmployeeSalaryDetail.DoesNotExist as exc:
        raise OvertimePolicyConfigurationError(
            'The employee salary detail is missing.', code='missing_employee_salary_detail'
        ) from exc
    try:
        company_calculations = Calculations.objects.get(user=owner, company=company)
    except Calculations.DoesNotExist as exc:
        raise OvertimePolicyConfigurationError(
            'The company overtime calculation configuration is missing.', code='missing_company_calculations'
        ) from exc

    attendance_records = list(EmployeeAttendance.objects.filter(
        user=actor,
        company=company,
        employee=employee,
        date__range=(period_start, period_end),
    ))
    detail_records = EmployeeAttendanceOvertimeDetail.objects.filter(
        attendance__user=actor,
        attendance__company=company,
        attendance__employee=employee,
        attendance__date__range=(period_start, period_end),
    )
    salary_earnings = EmployeeSalaryEarning.objects.select_related('earnings_head').filter(
        user=owner,
        company=company,
        employee=employee,
        from_date__lte=period_start,
        to_date__gte=period_start,
    )
    return _calculate_loaded_overtime(
        employee_salary_detail=employee_salary_detail,
        detail_records=detail_records,
        attendance_records=attendance_records,
        salary_earnings=salary_earnings,
        company_calculations=company_calculations,
        user=actor,
        period_start=period_start,
        period_end=period_end,
    )


def calculate_employee_overtime_from_loaded(
    *, actor, employee_salary_detail, attendance_records, salary_earnings, company_calculations, period_start,
):
    if not isinstance(period_start, date) or period_start.day != 1:
        _configuration_error('The overtime period must start on the first day of a month.', 'invalid_overtime_period')
    period_end = period_start.replace(day=28) + timedelta(days=4)
    period_end = period_end.replace(day=1) - timedelta(days=1)
    from api.models import EmployeeAttendanceOvertimeDetail

    detail_records = EmployeeAttendanceOvertimeDetail.objects.filter(
        attendance__user=actor,
        attendance__company=employee_salary_detail.company,
        attendance__employee=employee_salary_detail.employee,
        attendance__date__range=(period_start, period_end),
    )
    return _calculate_loaded_overtime(
        employee_salary_detail=employee_salary_detail,
        detail_records=detail_records,
        attendance_records=attendance_records,
        salary_earnings=salary_earnings,
        company_calculations=company_calculations,
        user=actor,
        period_start=period_start,
        period_end=period_end,
    )


def calculate_attendance_overtime(*, actor, attendance):
    """Calculate the policy-payable overtime attached to one attendance row."""
    from api.models import Calculations, EmployeeSalaryDetail, EmployeeSalaryEarning

    if not getattr(actor, 'is_authenticated', False):
        _configuration_error('Authentication is required for overtime calculation.', 'authentication_required')
    owner = actor if actor.role == 'OWNER' else getattr(getattr(actor, 'regular_to_owner', None), 'owner', None)
    if owner is None or attendance.company.user_id != owner.pk:
        _configuration_error('The attendance is outside the authenticated account scope.', 'cross_company_resolution')

    period_start = attendance.date.replace(day=1)
    period_end = period_start.replace(day=28) + timedelta(days=4)
    period_end = period_end.replace(day=1) - timedelta(days=1)
    try:
        employee_salary_detail = EmployeeSalaryDetail.objects.select_related(
            'employee', 'company', 'overtime_policy'
        ).get(user=owner, company=attendance.company, employee=attendance.employee)
    except EmployeeSalaryDetail.DoesNotExist as exc:
        raise OvertimePolicyConfigurationError(
            'The employee salary detail is missing.', code='missing_employee_salary_detail'
        ) from exc
    try:
        company_calculations = Calculations.objects.get(user=owner, company=attendance.company)
    except Calculations.DoesNotExist as exc:
        raise OvertimePolicyConfigurationError(
            'The company overtime calculation configuration is missing.', code='missing_company_calculations'
        ) from exc

    detail_records = list(attendance.overtime_details.all())
    salary_earnings = EmployeeSalaryEarning.objects.select_related('earnings_head').filter(
        user=owner,
        company=attendance.company,
        employee=attendance.employee,
        from_date__lte=period_start,
        to_date__gte=period_start,
    )
    return _calculate_loaded_overtime(
        employee_salary_detail=employee_salary_detail,
        detail_records=detail_records,
        attendance_records=[attendance],
        salary_earnings=salary_earnings,
        company_calculations=company_calculations,
        user=actor,
        period_start=period_start,
        period_end=period_end,
    )


def calculate_policy_overtime(
    *,
    employee_salary_detail,
    attendance_records,
    salary_earnings,
    company_calculations,
    user,
    days_in_month,
    period_start=None,
):
    attendance_records = list(attendance_records)
    if period_start is None:
        dates = [attendance.date for attendance in attendance_records]
        period_start = min(dates).replace(day=1) if dates else date.today().replace(day=1)
    period_end = period_start + timedelta(days=days_in_month - 1)
    detail_records = [
        detail
        for attendance in attendance_records
        for detail in attendance.overtime_details.all()
    ]
    return _calculate_loaded_overtime(
        employee_salary_detail=employee_salary_detail,
        detail_records=detail_records,
        attendance_records=attendance_records,
        salary_earnings=salary_earnings,
        company_calculations=company_calculations,
        user=user,
        period_start=period_start,
        period_end=period_end,
    )
