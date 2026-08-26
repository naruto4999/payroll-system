from datetime import date

from django.core.exceptions import ValidationError
from django.test import TestCase
from rest_framework.test import APIClient

from api.models import (
    Company,
    EarningsHead,
    EmployeeAttendance,
    EmployeeMonthlyAttendanceDetails,
    EmployeePfEsiDetail,
    LeaveGrade,
    OvertimePolicy,
)
from api.reports.generate_salary_sheet import (
    displayed_absent_half_count,
    format_day_count,
    get_selective_pay_unpaid_leave_counts,
)
from api.tests.base import AttendanceTestDataMixin


class SelectiveLeavePayTests(AttendanceTestDataMixin, TestCase):
    def setUp(self):
        self.employee = self.create_employee()
        self.basic = self.create_salary_earning(self.employee, value=20800)
        EmployeePfEsiDetail.objects.create(
            user=self.user,
            company=self.company,
            employee=self.employee,
        )
        self.monthly = EmployeeMonthlyAttendanceDetails.objects.create(
            user=self.user,
            company=self.company,
            employee=self.employee,
            date=date(2024, 1, 1),
            paid_days_count=40,
        )
        policy = OvertimePolicy.objects.get(
            company=self.company,
            code='ALL_DAYS_DOUBLE',
        )
        self.assign_overtime_policy(self.employee, policy)
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def _preview(self):
        return self.client.post(
            '/api/salary-preparation/preview',
            {
                'company': self.company.pk,
                'employee': self.employee.pk,
                'year': 2024,
                'month': 1,
                'incentive_amount': 0,
                'advance_deducted': 0,
                'others_deducted': 0,
                'arrears': [],
            },
            format='json',
        )

    def _custom_leave(self, payable_head):
        leave = LeaveGrade.objects.create(
            user=self.user,
            company=self.company,
            name='SPECIAL',
            paid=False,
        )
        leave.payable_earnings_heads.add(payable_head)
        return leave

    def test_monthly_preview_pays_only_selected_head_for_custom_leave(self):
        allowance = self.create_salary_earning(
            self.employee,
            name='Allowance',
            value=3100,
        )
        custom_leave = self._custom_leave(allowance.earnings_head)
        EmployeeAttendance.objects.create(
            user=self.user,
            company=self.company,
            employee=self.employee,
            date=date(2024, 1, 2),
            first_half=custom_leave,
            second_half=custom_leave,
            manual_mode=True,
        )

        response = self._preview()

        self.assertEqual(response.status_code, 200, response.data)
        amounts = {
            row['earnings_head']['name']: row['earned_amount']
            for row in response.data['salary']['earned_amounts']
        }
        self.assertEqual(amounts['Basic'], 13419)
        self.assertEqual(amounts['Allowance'], 2100)

        bulk = self.client.post(
            '/api/employee-bulk-salary-prepared',
            {
                'company': self.company.pk,
                'year': 2024,
                'month': 1,
                'employeeIds': [self.employee.pk],
            },
            format='json',
        )
        self.assertEqual(bulk.status_code, 200, bulk.data)
        prepared_amounts = {
            row.earnings_head.name: row.earned_amount
            for row in self.employee.salaries_prepared.get(
                date=date(2024, 1, 1)
            ).current_salary_earned_amounts.select_related('earnings_head')
        }
        self.assertEqual(prepared_amounts, amounts)

    def test_salary_sheet_splits_selective_pay_leave_from_displayed_absence(self):
        allowance = self.create_salary_earning(
            self.employee,
            name='Allowance',
            value=3100,
        )
        custom_leave = self._custom_leave(allowance.earnings_head)
        EmployeeAttendance.objects.create(
            user=self.user,
            company=self.company,
            employee=self.employee,
            date=date(2024, 1, 2),
            first_half=custom_leave,
            second_half=custom_leave,
            manual_mode=True,
        )
        EmployeeAttendance.objects.create(
            user=self.user,
            company=self.company,
            employee=self.employee,
            date=date(2024, 1, 3),
            first_half=custom_leave,
            manual_mode=True,
        )

        leave_counts = get_selective_pay_unpaid_leave_counts(
            user=self.user,
            company_id=self.company.pk,
            employee_id=self.employee.pk,
            salary_date=date(2024, 1, 1),
            selective_pay_unpaid_leaves=[custom_leave],
        )

        self.assertEqual(leave_counts, [('SPECIAL', 3)])
        self.assertEqual(format_day_count(leave_counts[0][1]), '1.5')
        self.assertEqual(displayed_absent_half_count(3, leave_counts), 0)
        self.assertEqual(displayed_absent_half_count(5, leave_counts), 2)

    def test_daily_preview_pays_selected_head_rate_for_half_leave(self):
        salary_detail = self.basic.employee.employee_salary_detail
        salary_detail.salary_mode = 'daily'
        salary_detail.save(update_fields=['salary_mode'])
        self.basic.value = 100
        self.basic.save(update_fields=['value'])
        allowance = self.create_salary_earning(
            self.employee,
            name='Allowance',
            value=100,
        )
        custom_leave = self._custom_leave(allowance.earnings_head)
        EmployeeAttendance.objects.create(
            user=self.user,
            company=self.company,
            employee=self.employee,
            date=date(2024, 1, 2),
            first_half=custom_leave,
            second_half=self.leave_absent,
            manual_mode=True,
        )

        response = self._preview()

        self.assertEqual(response.status_code, 200, response.data)
        amounts = {
            row['earnings_head']['name']: row['earned_amount']
            for row in response.data['salary']['earned_amounts']
        }
        self.assertEqual(amounts['Basic'], 2000)
        self.assertEqual(amounts['Allowance'], 2050)


class SelectiveLeaveGradeApiTests(AttendanceTestDataMixin, TestCase):
    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(self.user)
        self.allowance = EarningsHead.objects.create(
            user=self.user,
            company=self.company,
            name='Allowance',
        )

    def test_create_and_update_selective_leave_grade(self):
        response = self.client.post(
            f'/api/leave-grade/{self.company.pk}',
            {
                'company': self.company.pk,
                'name': 'SPECIAL',
                'paid': False,
                'limit': None,
                'generateFrequency': None,
                'payableEarningsHeads': [self.allowance.pk],
            },
            format='json',
        )

        self.assertEqual(response.status_code, 201, response.data)
        leave = LeaveGrade.objects.get(pk=response.data['id'])
        self.assertEqual(
            list(leave.payable_earnings_heads.values_list('pk', flat=True)),
            [self.allowance.pk],
        )

        response = self.client.put(
            f'/api/leave-grade/{self.company.pk}/{leave.pk}',
            {
                'company': self.company.pk,
                'name': leave.name,
                'paid': True,
                'limit': None,
                'generateFrequency': None,
                'payableEarningsHeads': [],
            },
            format='json',
        )

        self.assertEqual(response.status_code, 201, response.data)
        self.assertFalse(leave.payable_earnings_heads.exists())

    def test_rejects_cross_company_payable_head(self):
        other_company = Company.objects.create(user=self.user, name='Other')
        other_head = EarningsHead.objects.create(
            user=self.user,
            company=other_company,
            name='Other allowance',
        )

        response = self.client.post(
            f'/api/leave-grade/{self.company.pk}',
            {
                'company': self.company.pk,
                'name': 'SPECIAL',
                'paid': False,
                'payableEarningsHeads': [other_head.pk],
            },
            format='json',
        )

        self.assertEqual(response.status_code, 400, response.data)
        self.assertIn('payable_earnings_heads', response.data)

        leave = LeaveGrade.objects.create(
            user=self.user,
            company=self.company,
            name='DIRECT',
            paid=False,
        )
        with self.assertRaises(ValidationError):
            leave.payable_earnings_heads.add(other_head)

    def test_rejects_selected_heads_for_fully_paid_leave(self):
        response = self.client.post(
            f'/api/leave-grade/{self.company.pk}',
            {
                'company': self.company.pk,
                'name': 'SPECIAL',
                'paid': True,
                'payableEarningsHeads': [self.allowance.pk],
            },
            format='json',
        )

        self.assertEqual(response.status_code, 400, response.data)
        self.assertIn('payable_earnings_heads', response.data)

    def test_rejects_paid_state_change_after_attendance_use(self):
        employee = self.create_employee()
        paid_leave = LeaveGrade.objects.create(
            user=self.user,
            company=self.company,
            name='SPECIAL',
            paid=True,
        )
        EmployeeAttendance.objects.create(
            user=self.user,
            company=self.company,
            employee=employee,
            date=date(2024, 1, 2),
            first_half=paid_leave,
            second_half=paid_leave,
            manual_mode=True,
        )
        monthly = EmployeeMonthlyAttendanceDetails.objects.create(
            user=self.user,
            company=self.company,
            employee=employee,
            date=date(2024, 1, 1),
            paid_days_count=2,
        )

        response = self.client.put(
            f'/api/leave-grade/{self.company.pk}/{paid_leave.pk}',
            {
                'company': self.company.pk,
                'name': paid_leave.name,
                'paid': False,
                'limit': None,
                'generateFrequency': None,
                'payableEarningsHeads': [self.allowance.pk],
            },
            format='json',
        )

        self.assertEqual(response.status_code, 400, response.data)
        self.assertIn('paid', response.data)
        monthly.refresh_from_db()
        self.assertEqual(monthly.paid_days_count, 2)
        self.assertEqual(monthly.not_paid_days_count, 0)
