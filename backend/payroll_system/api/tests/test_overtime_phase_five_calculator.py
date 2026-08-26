from datetime import date
from decimal import Decimal
from unittest.mock import patch

from django.test import TestCase

from api.models import (
    Calculations,
    Company,
    EarningsHead,
    EmployeeAttendance,
    EmployeeSalaryDetail,
    OvertimePolicy,
    OvertimePolicyEarningsHead,
    OwnerToRegular,
    Regular,
    User,
)
from api.services.overtime_policy import (
    OvertimePolicyConfigurationError,
    calculate_employee_overtime,
    calculate_policy_overtime,
    rounded_ot_minutes,
)
from api.tests.base import AttendanceTestDataMixin


class OvertimePhaseFiveCalculatorTests(AttendanceTestDataMixin, TestCase):
    def calculate(self, employee, *, actor=None, period_start=date(2024, 1, 1)):
        return calculate_employee_overtime(
            actor=actor or self.user,
            company=self.company,
            employee=employee,
            period_start=period_start,
        )

    def create_calculation_employee(
        self,
        *,
        paycode,
        card,
        policy=None,
        salary_mode='monthly',
        earning=20800,
    ):
        employee = self.create_employee(
            paycode=paycode,
            attendance_card_no=card,
            salary_mode=salary_mode,
            overtime_policy=policy,
        )
        if earning is not None:
            self.create_salary_earning(employee, value=earning)
        return employee

    def row(self, result, day_type):
        return next(row for row in result.breakdown if row['day_type'] == day_type)

    def test_rounding_helper_supports_default_custom_and_non_thirty_increments(self):
        default = {0: 0, 15: 0, 16: 30, 29: 30, 30: 30, 45: 30, 46: 60, 59: 60}
        custom = {0: 0, 19: 0, 20: 30, 29: 30, 30: 30, 49: 30, 50: 60, 59: 60}

        self.assertEqual({value: rounded_ot_minutes(value) for value in default}, default)
        self.assertEqual({value: rounded_ot_minutes(value, 30, 20) for value in custom}, custom)
        self.assertEqual(rounded_ot_minutes(23, 15, 8), 30)
        for args in ((10, 0, 1), (10, -1, 1), (10, 30, 0), (10, 30, 31)):
            with self.assertRaises(ValueError):
                rounded_ot_minutes(*args)

    def test_details_override_aggregate_and_round_once_per_group(self):
        policy = OvertimePolicy.objects.get(company=self.company, code='ALL_DAYS_SINGLE')
        employee = self.create_calculation_employee(paycode='GROUP', card=201, policy=policy)
        first = self.create_attendance(employee, ot_min=999)
        self.create_overtime_detail(first, minutes=10, source='MANUAL')
        self.create_overtime_detail(first, minutes=10, source='IMPORTED')
        second = self.create_attendance(employee, work_date=date(2024, 1, 3), ot_min=10)
        self.create_overtime_detail(second, minutes=10)

        result = self.calculate(employee)

        self.assertEqual(result.raw_eligible_minutes, 30)
        self.assertEqual(result.rounded_gross_minutes, 30)
        self.assertEqual(result.net_minutes, 30)
        self.assertEqual(len(result.group_diagnostics), 2)
        self.assertEqual([group['rounded_gross_minutes'] for group in result.group_diagnostics], [30, 0])

    def test_day_type_is_part_of_grouping_and_ineligible_facts_remain_diagnostic(self):
        policy = self.create_overtime_policy(code='REGULAR_ONLY', rules=(('REGULAR', '1'),))
        employee = self.create_calculation_employee(paycode='CATEGORY', card=202, policy=policy)
        attendance = self.create_attendance(employee, ot_min=30)
        self.create_overtime_detail(attendance, minutes=15, day_type='REGULAR')
        self.create_overtime_detail(attendance, minutes=15, day_type='WEEKLY_OFF', source='IMPORTED')

        result = self.calculate(employee)

        self.assertEqual(result.raw_eligible_minutes, 30)
        self.assertEqual(result.rounded_gross_minutes, 0)
        self.assertEqual(result.net_minutes, 0)
        self.assertEqual([row['day_type'] for row in result.breakdown], ['REGULAR', 'WEEKLY_OFF', 'HOLIDAY'])
        self.assertFalse(self.row(result, 'WEEKLY_OFF')['eligible'])
        self.assertEqual(self.row(result, 'WEEKLY_OFF')['raw_eligible_minutes'], 15)

    def test_custom_policy_rounding_is_applied_to_each_group(self):
        policy = self.create_overtime_policy(code='ROUND_16', round_up_from_minutes=16)
        employee = self.create_calculation_employee(paycode='ROUND16', card=203, policy=policy)
        attendance = self.create_attendance(employee, ot_min=46)
        self.create_overtime_detail(attendance, minutes=46)

        result = self.calculate(employee)

        self.assertEqual(result.net_minutes, 60)
        self.assertEqual((result.rounding_increment_minutes, result.round_up_from_minutes), (30, 16))

    def test_late_rounding_remains_30_20_when_policy_uses_custom_ot_rounding(self):
        policy = self.create_overtime_policy(code='ROUND_16_LATE', round_up_from_minutes=16)
        employee = self.create_calculation_employee(paycode='ROUND16LATE', card=204, policy=policy)
        salary_detail = EmployeeSalaryDetail.objects.get(employee=employee)
        salary_detail.late_deduction = True
        salary_detail.save(update_fields=['late_deduction'])
        attendance = self.create_attendance(employee, ot_min=90, late_min=76)
        self.create_overtime_detail(attendance, minutes=90)

        result = self.calculate(employee)

        self.assertEqual(result.rounded_gross_minutes, 90)
        self.assertEqual(result.deducted_late_minutes, 60)
        self.assertEqual(result.net_minutes, 30)

    def test_same_multiplier_components_round_once_per_attendance_before_late_deduction(self):
        policy = self.create_overtime_policy(
            code='SHARED_MULTIPLIER',
            rules=(('REGULAR', '1'), ('WEEKLY_OFF', '1')),
        )
        employee = self.create_calculation_employee(paycode='SHARED', card=219, policy=policy)
        salary_detail = EmployeeSalaryDetail.objects.get(employee=employee)
        salary_detail.late_deduction = True
        salary_detail.save(update_fields=['late_deduction'])
        attendance = self.create_attendance(employee, ot_min=846, late_min=30)
        self.create_overtime_detail(
            attendance,
            minutes=828,
            excluded_minutes=30,
            exclusion_reason='MEAL_BREAK',
            day_type='WEEKLY_OFF',
        )
        self.create_overtime_detail(
            attendance,
            minutes=48,
            work_date=date(2024, 1, 3),
            day_type='REGULAR',
        )

        result = self.calculate(employee)

        self.assertEqual(result.raw_eligible_minutes, 846)
        self.assertEqual(result.policy_eligible_gross_minutes, 840)
        self.assertEqual(result.deducted_late_minutes, 30)
        self.assertEqual(result.net_minutes, 810)
        self.assertEqual(self.row(result, 'WEEKLY_OFF')['gross_minutes'], 792)
        self.assertEqual(self.row(result, 'WEEKLY_OFF')['net_minutes'], 792)
        self.assertEqual(self.row(result, 'REGULAR')['gross_minutes'], 48)
        self.assertEqual(self.row(result, 'REGULAR')['net_minutes'], 18)
        self.assertEqual(
            [group['rounding_bucket_rounded_minutes'] for group in result.group_diagnostics],
            [840, 840],
        )

    def test_different_multipliers_round_separately_before_priority_late_deduction(self):
        policy = self.create_overtime_policy(
            code='SPLIT_MULTIPLIER',
            rules=(('REGULAR', '1'), ('WEEKLY_OFF', '2')),
        )
        employee = self.create_calculation_employee(paycode='SPLIT', card=220, policy=policy)
        salary_detail = EmployeeSalaryDetail.objects.get(employee=employee)
        salary_detail.late_deduction = True
        salary_detail.save(update_fields=['late_deduction'])
        attendance = self.create_attendance(employee, ot_min=846, late_min=30)
        self.create_overtime_detail(attendance, minutes=798, day_type='WEEKLY_OFF')
        self.create_overtime_detail(
            attendance,
            minutes=48,
            work_date=date(2024, 1, 3),
            day_type='REGULAR',
        )

        result = self.calculate(employee)

        self.assertEqual(result.policy_eligible_gross_minutes, 870)
        self.assertEqual(result.net_minutes, 840)
        self.assertEqual(self.row(result, 'REGULAR')['gross_minutes'], 60)
        self.assertEqual(self.row(result, 'REGULAR')['deducted_late_minutes'], 30)
        self.assertEqual(self.row(result, 'WEEKLY_OFF')['gross_minutes'], 810)
        self.assertEqual(self.row(result, 'WEEKLY_OFF')['deducted_late_minutes'], 0)

    def test_different_multiplier_late_priority_changes_the_payable_amount(self):
        regular_first = self.create_overtime_policy(
            code='REGULAR_FIRST',
            rules=(('REGULAR', '1'), ('WEEKLY_OFF', '2')),
        )
        weekly_first = self.create_overtime_policy(
            code='WEEKLY_FIRST',
            rules=(('WEEKLY_OFF', '2'), ('REGULAR', '1')),
        )
        results = []
        for index, policy in enumerate((regular_first, weekly_first), start=1):
            employee = self.create_calculation_employee(
                paycode=f'PRIORITY{index}', card=220 + index, policy=policy,
            )
            salary_detail = EmployeeSalaryDetail.objects.get(employee=employee)
            salary_detail.late_deduction = True
            salary_detail.save(update_fields=['late_deduction'])
            attendance = self.create_attendance(employee, ot_min=846, late_min=30)
            self.create_overtime_detail(attendance, minutes=798, day_type='WEEKLY_OFF')
            self.create_overtime_detail(
                attendance,
                minutes=48,
                work_date=date(2024, 1, 3),
                day_type='REGULAR',
            )
            results.append(self.calculate(employee))

        self.assertEqual(results[0].net_minutes, results[1].net_minutes)
        self.assertEqual(self.row(results[0], 'REGULAR')['deducted_late_minutes'], 30)
        self.assertEqual(self.row(results[1], 'WEEKLY_OFF')['deducted_late_minutes'], 30)
        self.assertGreater(results[0].amount, results[1].amount)

    def test_shared_multiplier_round_down_allocation_never_becomes_negative(self):
        policy = self.create_overtime_policy(
            code='ROUND_TO_ZERO',
            rules=(('REGULAR', '1'), ('WEEKLY_OFF', '1')),
        )
        employee = self.create_calculation_employee(paycode='ZERO', card=223, policy=policy)
        attendance = self.create_attendance(employee, ot_min=15)
        self.create_overtime_detail(attendance, minutes=10)
        self.create_overtime_detail(
            attendance,
            minutes=5,
            work_date=date(2024, 1, 3),
            day_type='WEEKLY_OFF',
        )

        result = self.calculate(employee)

        self.assertEqual(result.policy_eligible_gross_minutes, 0)
        self.assertEqual(result.net_minutes, 0)
        self.assertTrue(all(group['rounded_gross_minutes'] >= 0 for group in result.group_diagnostics))

    def test_same_multiplier_does_not_combine_separate_attendance_rows(self):
        policy = OvertimePolicy.objects.get(company=self.company, code='ALL_DAYS_SINGLE')
        employee = self.create_calculation_employee(paycode='SEPARATE', card=224, policy=policy)
        first = self.create_attendance(employee, ot_min=20)
        second = self.create_attendance(employee, work_date=date(2024, 1, 3), ot_min=20)
        self.create_overtime_detail(first, minutes=20)
        self.create_overtime_detail(second, minutes=20)

        result = self.calculate(employee)

        self.assertEqual(result.raw_eligible_minutes, 40)
        self.assertEqual(result.policy_eligible_gross_minutes, 60)
        self.assertEqual(
            [group['rounding_bucket_rounded_minutes'] for group in result.group_diagnostics],
            [30, 30],
        )

    def test_late_minutes_follow_policy_priority_and_spill_without_negative_values(self):
        policy = self.create_overtime_policy(
            code='LATE_PRIORITY',
            rules=(('WEEKLY_OFF', '2'), ('REGULAR', '1')),
        )
        employee = self.create_calculation_employee(paycode='LATE', card=204, policy=policy)
        salary_detail = EmployeeSalaryDetail.objects.get(employee=employee)
        salary_detail.late_deduction = True
        salary_detail.save(update_fields=['late_deduction'])
        weekly = self.create_attendance(employee, ot_min=60, late_min=80)
        self.create_overtime_detail(weekly, minutes=60, day_type='WEEKLY_OFF')
        regular = self.create_attendance(employee, work_date=date(2024, 1, 3), ot_min=60)
        self.create_overtime_detail(regular, minutes=60)

        result = self.calculate(employee)

        self.assertEqual(self.row(result, 'WEEKLY_OFF')['deducted_late_minutes'], 60)
        self.assertEqual(self.row(result, 'REGULAR')['deducted_late_minutes'], 30)
        self.assertEqual(result.policy_eligible_gross_minutes, 120)
        self.assertEqual(result.deducted_late_minutes, 90)
        self.assertEqual(result.net_minutes, 30)
        self.assertTrue(all(row['net_minutes'] >= 0 for row in result.breakdown))

    def test_selected_heads_control_rate_and_metadata(self):
        employee = self.create_calculation_employee(paycode='HEADS', card=205, earning=None)
        selected_earning = self.create_salary_earning(employee, name='OT Basic', value=10400)
        self.create_salary_earning(employee, name='Allowance', value=5000)
        policy = self.create_overtime_policy(
            code='SELECTED',
            earnings_basis=OvertimePolicy.EARNINGS_BASIS_SELECTED,
            selected_heads=(selected_earning.earnings_head,),
        )
        self.assign_overtime_policy(employee, policy)
        attendance = self.create_attendance(employee, ot_min=60)
        self.create_overtime_detail(attendance, minutes=60)

        result = self.calculate(employee)

        self.assertEqual(result.amount, Decimal('50'))
        self.assertEqual(result.selected_earning_head_ids, (selected_earning.earnings_head_id,))
        self.assertEqual(result.effective_policy['earnings_basis'], 'SELECTED_HEADS')

    def test_payable_selected_head_without_employee_rate_is_controlled_error(self):
        employee = self.create_calculation_employee(paycode='NO_RATE', card=206, earning=None)
        head = EarningsHead.objects.create(user=self.user, company=self.company, name='Unused')
        policy = self.create_overtime_policy(
            code='NO_RATE_POLICY',
            earnings_basis=OvertimePolicy.EARNINGS_BASIS_SELECTED,
            selected_heads=(head,),
        )
        self.assign_overtime_policy(employee, policy)
        attendance = self.create_attendance(employee, ot_min=60)
        self.create_overtime_detail(attendance, minutes=60)

        with self.assertRaises(OvertimePolicyConfigurationError) as caught:
            self.calculate(employee)

        self.assertEqual(caught.exception.code, 'missing_selected_earning_rate')

    def test_malformed_selected_head_configuration_has_structured_errors(self):
        employee = self.create_calculation_employee(paycode='BAD_HEADS', card=217)
        empty_policy = self.create_overtime_policy(code='EMPTY_HEADS')
        OvertimePolicy.objects.filter(pk=empty_policy.pk).update(earnings_basis='SELECTED_HEADS')
        self.assign_overtime_policy(employee, empty_policy)

        with self.assertRaises(OvertimePolicyConfigurationError) as empty:
            self.calculate(employee)
        self.assertEqual(empty.exception.code, 'empty_selected_heads')

        other_owner = User.objects.create_user(
            username='head-owner',
            email='head-owner@example.com',
            password='password',
            phone_no=9999999203,
        )
        other_company = Company.objects.create(user=other_owner, name='Head Company')
        other_head = EarningsHead.objects.create(user=other_owner, company=other_company, name='Other Head')
        selected_earning = employee.earnings.select_related('earnings_head').get()
        cross_policy = self.create_overtime_policy(
            code='CROSS_HEAD',
            earnings_basis=OvertimePolicy.EARNINGS_BASIS_SELECTED,
            selected_heads=(selected_earning.earnings_head,),
        )
        self.assign_overtime_policy(employee, cross_policy)
        OvertimePolicyEarningsHead.objects.filter(policy=cross_policy).update(earnings_head=other_head)

        with self.assertRaises(OvertimePolicyConfigurationError) as cross_company:
            self.calculate(employee)
        self.assertEqual(cross_company.exception.code, 'cross_company_selected_head')

    def test_daily_and_monthly_formulas_round_categories_to_cents_and_total_to_whole(self):
        double = OvertimePolicy.objects.get(company=self.company, code='ALL_DAYS_DOUBLE')
        daily = self.create_calculation_employee(
            paycode='DAILY', card=207, policy=double, salary_mode='daily', earning=20800
        )
        daily_attendance = self.create_attendance(daily, ot_min=60)
        self.create_overtime_detail(daily_attendance, minutes=60)

        daily_result = self.calculate(daily)

        self.assertEqual(daily_result.amount, Decimal('5200'))
        self.assertEqual(self.row(daily_result, 'REGULAR')['divisor'], Decimal('1.00'))

        single = OvertimePolicy.objects.get(company=self.company, code='ALL_DAYS_SINGLE')
        monthly = self.create_calculation_employee(paycode='MONTHLY', card=208, policy=single, earning=20800)
        monthly_attendance = self.create_attendance(monthly, work_date=date(2024, 1, 4), ot_min=120)
        self.create_overtime_detail(monthly_attendance, minutes=60)
        self.create_overtime_detail(monthly_attendance, minutes=60, day_type='HOLIDAY', source='IMPORTED')
        Calculations.objects.filter(company=self.company).update(ot_calculation='30')

        monthly_result = self.calculate(monthly)

        self.assertEqual(self.row(monthly_result, 'REGULAR')['amount'], Decimal('86.67'))
        self.assertEqual(self.row(monthly_result, 'HOLIDAY')['amount'], Decimal('86.67'))
        self.assertEqual(sum(row['amount'] for row in monthly_result.breakdown), Decimal('173.34'))
        self.assertEqual(monthly_result.amount, Decimal('173'))
        self.assertTrue(all(isinstance(row['amount'], Decimal) for row in monthly_result.breakdown))

    def test_owner_month_days_divisors_cover_calendar_lengths(self):
        policy = OvertimePolicy.objects.get(company=self.company, code='ALL_DAYS_SINGLE')
        employee = self.create_calculation_employee(paycode='DIVISOR', card=209, policy=policy)
        employee.earnings.update(from_date=date(2023, 1, 1))
        Calculations.objects.filter(company=self.company).update(ot_calculation='month_days')
        expected = {
            date(2023, 2, 1): Decimal('28.00'),
            date(2024, 2, 1): Decimal('29.00'),
            date(2024, 4, 1): Decimal('30.00'),
            date(2024, 1, 1): Decimal('31.00'),
        }
        for index, (period_start, divisor) in enumerate(expected.items(), start=1):
            attendance = self.create_attendance(
                employee,
                work_date=period_start.replace(day=2),
                ot_min=60,
            )
            self.create_overtime_detail(attendance, minutes=60)
            result = self.calculate(employee, period_start=period_start)
            self.assertEqual(self.row(result, 'REGULAR')['divisor'], divisor, index)

    def test_regular_uses_forced_double_policy_divisor_26_and_ignores_legacy_rate(self):
        single = OvertimePolicy.objects.get(company=self.company, code='ALL_DAYS_SINGLE')
        employee = self.create_calculation_employee(paycode='REGULAR', card=210, policy=single)
        employee.visible = True
        employee.save(update_fields=['visible'])
        self.company.visible = True
        self.company.save(update_fields=['visible'])
        salary_detail = EmployeeSalaryDetail.objects.get(employee=employee)
        salary_detail.overtime_rate = 'S'
        salary_detail.save(update_fields=['overtime_rate'])
        regular = Regular.objects.create_user(
            username='phase-five-regular',
            email='phase-five-regular@example.com',
            password='password',
            phone_no=9999999201,
        )
        OwnerToRegular.objects.create(user=regular, owner=self.user)
        attendance = EmployeeAttendance.objects.create(
            user=regular,
            company=self.company,
            employee=employee,
            date=date(2024, 1, 2),
            first_half=self.leave_present,
            second_half=self.leave_present,
            ot_min=60,
        )
        self.create_overtime_detail(attendance, minutes=60)

        result = self.calculate(employee, actor=regular)

        self.assertEqual(result.policy_code, 'ALL_DAYS_DOUBLE')
        self.assertEqual(result.policy_resolution, 'FORCED_REGULAR')
        self.assertEqual(self.row(result, 'REGULAR')['multiplier'], Decimal('2'))
        self.assertEqual(self.row(result, 'REGULAR')['divisor'], Decimal('26.00'))
        self.assertEqual(result.amount, Decimal('200'))

    def test_attendance_date_assigns_cross_month_detail_to_the_supported_period(self):
        policy = OvertimePolicy.objects.get(company=self.company, code='ALL_DAYS_SINGLE')
        employee = self.create_calculation_employee(paycode='CROSS_MONTH', card=211, policy=policy)
        attendance = self.create_attendance(employee, work_date=date(2024, 1, 31), ot_min=60)
        self.create_overtime_detail(attendance, minutes=60, work_date=date(2024, 2, 1))

        january = self.calculate(employee, period_start=date(2024, 1, 1))
        february = self.calculate(employee, period_start=date(2024, 2, 1))

        self.assertEqual(january.net_minutes, 60)
        self.assertEqual(january.group_diagnostics[0]['work_date'], date(2024, 2, 1))
        self.assertEqual(february.net_minutes, 0)

    def test_unbackfilled_positive_aggregate_is_a_controlled_error(self):
        policy = OvertimePolicy.objects.get(company=self.company, code='ALL_DAYS_SINGLE')
        employee = self.create_calculation_employee(paycode='LEGACY', card=212, policy=policy)
        self.create_attendance(employee, ot_min=60)

        with self.assertRaises(OvertimePolicyConfigurationError) as caught:
            self.calculate(employee)

        self.assertEqual(caught.exception.code, 'unbackfilled_overtime')

    def test_no_details_and_policy_ineligible_details_return_stable_zero_rows(self):
        no_overtime = OvertimePolicy.objects.get(company=self.company, code='NO_OVERTIME')
        employee = self.create_calculation_employee(paycode='NO_OT', card=213, policy=no_overtime, earning=None)
        empty_result = self.calculate(employee)
        attendance = self.create_attendance(employee, ot_min=60)
        self.create_overtime_detail(attendance, minutes=60)
        ineligible_result = self.calculate(employee)

        self.assertEqual(empty_result.net_minutes, 0)
        self.assertEqual(len(empty_result.breakdown), 3)
        self.assertEqual(ineligible_result.raw_eligible_minutes, 60)
        self.assertEqual(ineligible_result.rounded_gross_minutes, 60)
        self.assertEqual(ineligible_result.net_minutes, 0)
        self.assertEqual(ineligible_result.snapshot_breakdown, [])

    def test_inherited_policy_metadata_is_explicit_in_result(self):
        employee = self.create_calculation_employee(paycode='INHERITED', card=218)

        result = self.calculate(employee)

        self.assertEqual(result.policy_resolution, 'INHERITED_DEFAULT')
        self.assertEqual(result.effective_policy['id'], result.policy_id)
        self.assertEqual(result.period_start, date(2024, 1, 1))
        self.assertEqual(result.period_end, date(2024, 1, 31))

    def test_unsupported_salary_mode_and_missing_calculations_are_controlled_errors(self):
        policy = OvertimePolicy.objects.get(company=self.company, code='ALL_DAYS_SINGLE')
        employee = self.create_calculation_employee(
            paycode='PIECE', card=214, policy=policy, salary_mode='piece_rate'
        )
        with self.assertRaises(OvertimePolicyConfigurationError) as unsupported:
            self.calculate(employee)
        self.assertEqual(unsupported.exception.code, 'unsupported_salary_mode')

        EmployeeSalaryDetail.objects.filter(employee=employee).update(salary_mode='monthly')
        Calculations.objects.filter(company=self.company).delete()
        with self.assertRaises(OvertimePolicyConfigurationError) as missing:
            self.calculate(employee)
        self.assertEqual(missing.exception.code, 'missing_company_calculations')

    def test_invalid_runtime_rounding_configuration_has_structured_error(self):
        policy = OvertimePolicy.objects.get(company=self.company, code='ALL_DAYS_SINGLE')
        employee = self.create_calculation_employee(paycode='BAD_ROUND', card=215, policy=policy)
        salary_detail = EmployeeSalaryDetail.objects.get(employee=employee)
        earning = employee.earnings.select_related('earnings_head').get()
        policy.rounding_increment_minutes = 0

        with patch('api.services.overtime_policy.resolve_calculation_overtime_policy', return_value=policy):
            with self.assertRaises(OvertimePolicyConfigurationError) as caught:
                calculate_policy_overtime(
                    employee_salary_detail=salary_detail,
                    attendance_records=[],
                    salary_earnings=[earning],
                    company_calculations=Calculations.objects.get(company=self.company),
                    user=self.user,
                    days_in_month=31,
                    period_start=date(2024, 1, 1),
                )

        self.assertEqual(caught.exception.code, 'invalid_rounding_configuration')

    def test_cross_company_actor_is_rejected_before_loading_inputs(self):
        employee = self.create_calculation_employee(paycode='SCOPE', card=216)
        other_owner = User.objects.create_user(
            username='phase-five-other',
            email='phase-five-other@example.com',
            password='password',
            phone_no=9999999202,
        )
        Company.objects.create(user=other_owner, name='Other')

        with self.assertRaises(OvertimePolicyConfigurationError) as caught:
            self.calculate(employee, actor=other_owner)

        self.assertEqual(caught.exception.code, 'cross_company_resolution')
