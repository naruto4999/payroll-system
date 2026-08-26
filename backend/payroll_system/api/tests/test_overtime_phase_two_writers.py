from datetime import date

from django.test import TestCase
from rest_framework.test import APIClient

from api.models import (
    EmployeeMonthlyAttendanceDetails,
    EmployeePfEsiDetail,
    EmployeeSalaryPrepared,
    OvertimePolicy,
)
from api.tests.base import AttendanceTestDataMixin


class PhaseTwoSalaryWriterTests(AttendanceTestDataMixin, TestCase):
    def setUp(self):
        self.employee = self.create_employee()
        self.create_salary_earning(self.employee)
        policy = OvertimePolicy.objects.get(company=self.company, is_default=True, is_active=True)
        policy.rounding_increment_minutes = 45
        policy.round_up_from_minutes = 25
        policy.save()

    def test_manual_salary_writer_populates_applied_rounding_snapshot(self):
        EmployeePfEsiDetail.objects.create(user=self.user, company=self.company, employee=self.employee)
        EmployeeMonthlyAttendanceDetails.objects.create(
            user=self.user,
            company=self.company,
            employee=self.employee,
            date=date(2024, 1, 1),
            paid_days_count=62,
        )
        earning = self.employee.earnings.get()
        client = APIClient()
        client.force_authenticate(self.user)
        response = client.post('/api/employee-salary-prepared', {
            'employee_salary_prepared': {
                'employee': self.employee.pk,
                'company': self.company.pk,
                'date': '2024-01-01',
            },
            'all_earned_amounts': [{
                'earnings_head': {'id': earning.earnings_head_id},
                'rate': earning.value,
                'earned_amount': earning.value,
                'arear_amount': 0,
            }],
        }, format='json')

        self.assertEqual(response.status_code, 200, response.data)
        salary = EmployeeSalaryPrepared.objects.get(employee=self.employee, date=date(2024, 1, 1))
        self.assertEqual((salary.ot_rounding_increment_minutes, salary.ot_round_up_from_minutes), (45, 25))

    def test_bulk_salary_writer_populates_applied_rounding_snapshot(self):
        EmployeePfEsiDetail.objects.create(user=self.user, company=self.company, employee=self.employee)
        EmployeeMonthlyAttendanceDetails.objects.create(
            user=self.user,
            company=self.company,
            employee=self.employee,
            date=date(2024, 1, 1),
        )

        EmployeeSalaryPrepared.objects.bulk_prepare_salaries(
            month=1,
            year=2024,
            company_id=self.company.pk,
            user=self.user,
        )

        salary = EmployeeSalaryPrepared.objects.get(employee=self.employee, date=date(2024, 1, 1))
        self.assertEqual((salary.ot_rounding_increment_minutes, salary.ot_round_up_from_minutes), (45, 25))
