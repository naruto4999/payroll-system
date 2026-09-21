from datetime import date
from unittest.mock import patch

from django.db import connection
from django.test import TestCase
from django.test.utils import CaptureQueriesContext
from rest_framework.test import APIClient

from api.models import (
    EarnedAmount,
    EmployeeAttendance,
    EmployeeGenerativeLeaveRecord,
    EmployeeMonthlyAttendanceDetails,
    EmployeePfEsiDetail,
    LeaveGrade,
)
from api.tests.base import AttendanceTestDataMixin


class PayslipReportTests(AttendanceTestDataMixin, TestCase):
    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(self.user)
        company_details = self.company.company_details
        company_details.address = 'Test address'
        company_details.save(update_fields=['address'])

        basic = self.user.earnings_heads.get(company=self.company, name='Basic')
        self.selective_leave = LeaveGrade.objects.create(
            user=self.user,
            company=self.company,
            name='SPECIAL',
            paid=False,
        )
        self.selective_leave.payable_earnings_heads.add(basic)
        self.generative_leave = LeaveGrade.objects.get(
            user=self.user,
            company=self.company,
            name='CL',
        )
        self.generative_leave.limit = 12
        self.generative_leave.generate_frequency = 1
        self.generative_leave.save(update_fields=['limit', 'generate_frequency'])

    def create_report_employee(self, index):
        employee = self.create_employee(
            paycode=f'E{index}',
            attendance_card_no=100 + index,
        )
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
            present_count=52,
            weekly_off_days_count=8,
            holiday_days_count=2,
            not_paid_days_count=1,
            paid_days_count=61,
        )
        EmployeeAttendance.objects.create(
            user=self.user,
            company=self.company,
            employee=employee,
            date=date(2024, 1, 2),
            first_half=self.selective_leave,
            manual_mode=True,
        )
        EmployeeGenerativeLeaveRecord.objects.create(
            user=self.user,
            company=self.company,
            employee=employee,
            leave=self.generative_leave,
            date=date(2024, 1, 1),
            leave_count=1,
        )
        prepared_salary = self.create_prepared_salary(
            employee,
            net_minutes=60,
            amount=200,
        )
        prepared_salary.incentive_amount = 100
        prepared_salary.save(update_fields=['incentive_amount'])
        EarnedAmount.objects.create(
            user=self.user,
            earnings_head=salary_rate.earnings_head,
            salary_prepared=prepared_salary,
            rate=salary_rate.value,
            earned_amount=salary_rate.value,
            arear_amount=50,
        )
        return employee

    def payload(self, employee_ids, sort_by='attendance_card_no'):
        return {
            'report_type': 'payslip',
            'employee_ids': employee_ids,
            'company': self.company.pk,
            'month': 1,
            'year': 2024,
            'filters': {
                'group_by': 'none',
                'resignation_filter': 'all',
                'sort_by': sort_by,
                'language': 'english',
                'format': 'pdf',
                'overtime': 'with_ot',
            },
        }

    def render_payslip(self, employees, sort_by='attendance_card_no'):
        with CaptureQueriesContext(connection) as queries:
            response = self.client.post(
                '/api/generate-salary-overtime-sheet',
                self.payload([employee.pk for employee in employees], sort_by),
                format='json',
            )
            content = b''.join(response.streaming_content)
        return response, content, queries.captured_queries

    def test_payslip_query_count_does_not_scale_per_employee(self):
        employees = [self.create_report_employee(1)]
        response, content, one_employee_queries = self.render_payslip(employees)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')
        self.assertTrue(content.startswith(b'%PDF-'))

        employees.extend(self.create_report_employee(index) for index in range(2, 6))
        response, content, five_employee_queries = self.render_payslip(employees)

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

    def test_paycode_sort_query_count_does_not_scale_per_employee(self):
        employees = [self.create_report_employee(index) for index in range(1, 6)]

        response, content, queries = self.render_payslip(employees, sort_by='paycode')

        self.assertEqual(response.status_code, 200)
        self.assertTrue(content.startswith(b'%PDF-'))
        self.assertLessEqual(len(queries), 15, [query['sql'] for query in queries])

    @patch('api.views.generate_payslip', return_value=[b'%PDF'])
    def test_paycode_sort_preserves_numeric_order(self, generator):
        employee_10 = self.create_report_employee(10)
        employee_2 = self.create_report_employee(2)

        response = self.client.post(
            '/api/generate-salary-overtime-sheet',
            self.payload([employee_10.pk, employee_2.pk], sort_by='paycode'),
            format='json',
        )
        content = b''.join(response.streaming_content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(content, b'%PDF')
        loaded_salaries = generator.call_args.args[2]
        self.assertEqual(
            [salary.employee.paycode for salary in loaded_salaries],
            ['E2', 'E10'],
        )
