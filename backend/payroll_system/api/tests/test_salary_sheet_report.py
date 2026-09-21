from datetime import date

from django.db import connection
from django.test import TestCase
from django.test.utils import CaptureQueriesContext
from rest_framework.test import APIClient

from api.models import (
    Deparment,
    EarnedAmount,
    EarningsHead,
    EmployeeAttendance,
    EmployeeMonthlyAttendanceDetails,
    EmployeePfEsiDetail,
    LeaveGrade,
)
from api.tests.base import AttendanceTestDataMixin


class SalarySheetReportTests(AttendanceTestDataMixin, TestCase):
    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(self.user)
        self.department = Deparment.objects.create(
            user=self.user,
            company=self.company,
            name='Operations',
        )
        company_details = self.company.company_details
        company_details.address = 'Test address'
        company_details.save(update_fields=['address'])
        basic = EarningsHead.objects.get(
            user=self.user,
            company=self.company,
            name='Basic',
        )
        self.selective_leave = LeaveGrade.objects.create(
            user=self.user,
            company=self.company,
            name='SPECIAL',
            paid=False,
        )
        self.selective_leave.payable_earnings_heads.add(basic)

    def create_report_employee(self, index):
        employee = self.create_employee(
            paycode=f'E{index:03d}',
            attendance_card_no=100 + index,
        )
        professional_detail = employee.employee_professional_detail
        professional_detail.department = self.department
        professional_detail.save(update_fields=['department'])
        salary_rate = self.create_salary_earning(employee, value=20800 + index)
        EmployeePfEsiDetail.objects.create(
            user=self.user,
            company=self.company,
            employee=employee,
        )
        EmployeeMonthlyAttendanceDetails.objects.create(
            user=self.user,
            company=self.company,
            employee=employee,
            date=date(2024, 1, 1),
            present_count=62,
            paid_days_count=62,
        )
        EmployeeAttendance.objects.create(
            user=self.user,
            company=self.company,
            employee=employee,
            date=date(2024, 1, 2),
            first_half=self.selective_leave,
            manual_mode=True,
        )
        prepared_salary = self.create_prepared_salary(employee)
        EarnedAmount.objects.create(
            user=self.user,
            earnings_head=salary_rate.earnings_head,
            salary_prepared=prepared_salary,
            rate=salary_rate.value,
            earned_amount=salary_rate.value,
        )
        return employee

    def salary_sheet_payload(self, employee_ids):
        return {
            'report_type': 'salary_sheet',
            'employee_ids': employee_ids,
            'company': self.company.pk,
            'month': 1,
            'year': 2024,
            'filters': {
                'group_by': 'department',
                'resignation_filter': 'all',
                'sort_by': 'attendance_card_no',
                'language': 'english',
                'format': 'pdf',
                'overtime': 'with_ot',
            },
        }

    def render_salary_sheet(self, employee_ids):
        with CaptureQueriesContext(connection) as queries:
            response = self.client.post(
                '/api/generate-salary-overtime-sheet',
                self.salary_sheet_payload(employee_ids),
                format='json',
            )
            content = b''.join(response.streaming_content)
        return response, content, queries.captured_queries

    def test_salary_sheet_query_count_does_not_scale_per_employee(self):
        employees = [self.create_report_employee(1)]
        response, content, one_employee_queries = self.render_salary_sheet(
            [employee.pk for employee in employees]
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(content.startswith(b'%PDF-'))

        employees.extend(self.create_report_employee(index) for index in range(2, 6))
        response, content, five_employee_queries = self.render_salary_sheet(
            [employee.pk for employee in employees]
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(content.startswith(b'%PDF-'))
        self.assertLessEqual(
            len(five_employee_queries),
            15,
            [query['sql'] for query in five_employee_queries],
        )
        self.assertLessEqual(
            len(five_employee_queries),
            len(one_employee_queries) + 1,
            [query['sql'] for query in five_employee_queries],
        )
