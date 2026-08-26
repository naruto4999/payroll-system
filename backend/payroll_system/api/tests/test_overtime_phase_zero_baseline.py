from datetime import date
from decimal import Decimal

from django.test import TestCase

from api.models import Calculations, EmployeeSalaryDetail, OvertimePolicy
from api.services.overtime_policy import calculate_policy_overtime, rounded_ot_minutes
from api.tests.base import AttendanceTestDataMixin


class OvertimePhaseZeroBaselineTests(AttendanceTestDataMixin, TestCase):
    def calculate(self, employee, attendance, *, role="OWNER"):
        self.user.role = role
        salary_detail = EmployeeSalaryDetail.objects.get(employee=employee)
        earning = self.create_salary_earning(employee)
        return calculate_policy_overtime(
            employee_salary_detail=salary_detail,
            attendance_records=[attendance],
            salary_earnings=[earning],
            company_calculations=Calculations.objects.get(company=self.company),
            user=self.user,
            days_in_month=31,
        )

    def test_default_rounding_30_16_characterization(self):
        expected = {0: 0, 15: 0, 16: 30, 29: 30, 30: 30, 45: 30, 46: 60, 59: 60}
        self.assertEqual({minutes: rounded_ot_minutes(minutes) for minutes in expected}, expected)

    def test_owner_monthly_uses_assigned_policy(self):
        policy = OvertimePolicy.objects.get(company=self.company, code="ALL_DAYS_SINGLE")
        employee = self.create_employee(overtime_policy=policy)
        attendance = self.create_attendance(employee, ot_min=60)
        self.create_overtime_detail(attendance, minutes=60)

        result = self.calculate(employee, attendance)

        self.assertEqual(result.net_minutes, 60)
        self.assertEqual(result.amount, Decimal("100"))
        self.assertEqual(result.breakdown[0]["multiplier"], Decimal("1"))

    def test_owner_daily_assigned_double_policy_current_formula(self):
        policy = OvertimePolicy.objects.get(company=self.company, code="ALL_DAYS_DOUBLE")
        employee = self.create_employee(
            paycode="E002",
            attendance_card_no=102,
            salary_mode="daily",
            overtime_rate="D",
            overtime_policy=policy,
        )
        attendance = self.create_attendance(employee, work_date=date(2024, 1, 3), ot_min=60)
        self.create_overtime_detail(attendance, minutes=60)

        result = self.calculate(employee, attendance)

        self.assertEqual(result.amount, Decimal("5200"))
        self.assertEqual(result.breakdown[0]["multiplier"], Decimal("2"))
        self.assertEqual(result.breakdown[0]["divisor"], Decimal("1.00"))

    def test_regular_uses_all_days_double_policy_and_divisor_26(self):
        employee = self.create_employee(paycode="E003", attendance_card_no=103)
        attendance = self.create_attendance(employee, work_date=date(2024, 1, 4), ot_min=60)
        self.create_overtime_detail(attendance, minutes=60)

        result = self.calculate(employee, attendance, role="REGULAR")

        self.assertEqual(result.net_minutes, 60)
        self.assertEqual(result.amount, Decimal("200"))
        self.assertEqual(result.breakdown[0]["multiplier"], Decimal("2"))

    def test_explicit_policy_and_selected_head_fixture(self):
        employee = self.create_employee(paycode="E004", attendance_card_no=104)
        earning = self.create_salary_earning(employee, name="Overtime Basic", value=10000)
        policy = self.create_overtime_policy(
            earnings_basis=OvertimePolicy.EARNINGS_BASIS_SELECTED,
            selected_heads=(earning.earnings_head,),
        )

        salary_detail = self.assign_overtime_policy(employee, policy)

        self.assertEqual(salary_detail.overtime_policy, policy)
        self.assertEqual(list(policy.selected_earning_heads.values_list("earnings_head_id", flat=True)), [earning.earnings_head_id])

    def test_attendance_details_override_conflicting_legacy_aggregate(self):
        policy = OvertimePolicy.objects.get(company=self.company, code="ALL_DAYS_SINGLE")
        employee = self.create_employee(paycode="E005", attendance_card_no=105, overtime_policy=policy)
        attendance = self.create_attendance(employee, work_date=date(2024, 1, 5), ot_min=60)
        self.create_overtime_detail(attendance, minutes=120)

        result = self.calculate(employee, attendance)

        self.assertEqual(result.net_minutes, 120)

    def test_prepared_salary_fixtures_support_legacy_and_categorized_rows(self):
        employee = self.create_employee(paycode="E006", attendance_card_no=106)
        legacy = self.create_prepared_salary(employee, net_minutes=30, amount=50)
        categorized = self.create_prepared_salary(
            employee,
            period=date(2024, 2, 1),
            net_minutes=30,
            amount=50,
        )
        self.create_prepared_overtime_detail(categorized)

        self.assertFalse(legacy.overtime_breakdown.exists())
        self.assertEqual(categorized.overtime_breakdown.get().net_minutes, 30)
