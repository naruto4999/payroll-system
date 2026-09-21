from datetime import date, time
from unittest.mock import patch

from django.db import connection
from django.test import TestCase
from django.test.utils import CaptureQueriesContext
from rest_framework.test import APIClient

from api.models import (
    EmployeeGenerativeLeaveRecord,
    EmployeeMonthlyAttendanceDetails,
    LeaveGrade,
)
from api.tests.base import AttendanceTestDataMixin


class AttendanceRegisterReportTests(AttendanceTestDataMixin, TestCase):
    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(self.user)
        self.generated_leave = LeaveGrade.objects.get(
            user=self.user,
            company=self.company,
            name='CL',
        )

    def payload(self, employee_ids, *, sort_by='attendance_card_no'):
        return {
            'report_type': 'attendance_register',
            'employee_ids': employee_ids,
            'company': self.company.pk,
            'month': 1,
            'year': 2024,
            'filters': {
                'group_by': 'none',
                'month_from_date': None,
                'month_to_date': None,
                'resignation_filter': 'all',
                'sort_by': sort_by,
                'date': None,
            },
        }

    def create_report_employee(self, index):
        employee = self.create_employee(
            paycode=f'E{index}',
            attendance_card_no=100 + index,
        )
        attendance = self.create_attendance(
            employee,
            work_date=date(2024, 1, 2),
            ot_min=60,
            late_min=15,
        )
        attendance.manual_in = time(9, 0)
        attendance.manual_out = time(18, 0)
        attendance.save()
        EmployeeMonthlyAttendanceDetails.objects.create(
            user=self.user,
            company=self.company,
            employee=employee,
            date=date(2024, 1, 1),
            present_count=61,
            paid_days_count=62,
            weekly_off_days_count=8,
            holiday_days_count=2,
            net_ot_minutes_monthly=60,
        )
        EmployeeGenerativeLeaveRecord.objects.create(
            user=self.user,
            company=self.company,
            employee=employee,
            leave=self.generated_leave,
            date=date(2024, 1, 1),
            leave_count=3,
        )
        return employee

    def render_report(self, employees, *, sort_by='attendance_card_no'):
        with CaptureQueriesContext(connection) as queries:
            response = self.client.post(
                '/api/generate-attendance-reports',
                self.payload([employee.pk for employee in employees], sort_by=sort_by),
                format='json',
            )
            content = b''.join(response.streaming_content)
        return response, content, queries.captured_queries

    def test_query_count_does_not_scale_per_employee(self):
        employees = [self.create_report_employee(1)]
        response, content, one_employee_queries = self.render_report(employees)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(content.startswith(b'%PDF-'))

        employees.extend(self.create_report_employee(index) for index in range(2, 6))
        response, content, five_employee_queries = self.render_report(employees)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(content.startswith(b'%PDF-'))
        self.assertLessEqual(
            len(five_employee_queries),
            10,
            [query['sql'] for query in five_employee_queries],
        )
        self.assertLessEqual(
            len(five_employee_queries),
            len(one_employee_queries) + 1,
            [query['sql'] for query in five_employee_queries],
        )

    def test_paycode_sort_query_count_does_not_scale_per_employee(self):
        employees = [self.create_report_employee(index) for index in range(1, 6)]

        response, content, queries = self.render_report(employees, sort_by='paycode')

        self.assertEqual(response.status_code, 200)
        self.assertTrue(content.startswith(b'%PDF-'))
        self.assertLessEqual(len(queries), 12, [query['sql'] for query in queries])

    @patch('api.views.generate_attendance_register', return_value=[b'%PDF'])
    def test_paycode_sort_preserves_numeric_order(self, generator):
        employee_10 = self.create_report_employee(10)
        employee_2 = self.create_report_employee(2)

        response = self.client.post(
            '/api/generate-attendance-reports',
            self.payload([employee_10.pk, employee_2.pk], sort_by='paycode'),
            format='json',
        )
        content = b''.join(response.streaming_content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(content, b'%PDF')
        loaded_employees = generator.call_args.args[2]
        self.assertEqual([employee.paycode for employee in loaded_employees], ['E2', 'E10'])
