from datetime import date
from unittest.mock import patch

from django.test import TestCase
from rest_framework.test import APIClient

from api.models import OvertimePolicy
from api.tests.base import AttendanceTestDataMixin


class OvertimeReportPolicyTests(AttendanceTestDataMixin, TestCase):
    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def daily_payload(self, employee_ids):
        return {
            'report_type': 'overtime_sheet_daily',
            'employee_ids': employee_ids,
            'company': self.company.pk,
            'month': 1,
            'year': 2024,
            'filters': {
                'group_by': 'none',
                'month_from_date': None,
                'month_to_date': None,
                'resignation_filter': 'all',
                'sort_by': 'attendance_card_no',
                'date': 2,
            },
        }

    def monthly_payload(self, employee_ids):
        return {
            'report_type': 'overtime_sheet',
            'employee_ids': employee_ids,
            'company': self.company.pk,
            'month': 1,
            'year': 2024,
            'filters': {
                'group_by': 'none',
                'resignation_filter': 'all',
                'sort_by': 'attendance_card_no',
                'language': 'english',
                'format': 'pdf',
                'overtime': 'with_ot',
            },
        }

    def create_employee_overtime(self, *, paycode, card, policy, late_min=None, late_deduction=False):
        employee = self.create_employee(
            paycode=paycode,
            attendance_card_no=card,
            overtime_policy=policy,
        )
        if late_deduction:
            salary_detail = employee.employee_salary_detail
            salary_detail.late_deduction = True
            salary_detail.save(update_fields=['late_deduction'])
        self.create_salary_earning(employee)
        attendance = self.create_attendance(
            employee,
            work_date=date(2024, 1, 2),
            ot_min=60,
            late_min=late_min,
        )
        self.create_overtime_detail(attendance, minutes=60)
        return employee, attendance

    @patch('api.views.generate_overtime_sheet_daily', return_value=[b'%PDF'])
    def test_daily_report_excludes_raw_overtime_under_no_overtime_policy(self, generator):
        no_overtime = OvertimePolicy.objects.get(company=self.company, code='NO_OVERTIME')
        payable_policy = OvertimePolicy.objects.get(company=self.company, code='ALL_DAYS_SINGLE')
        no_ot_employee, _ = self.create_employee_overtime(
            paycode='NO_OT', card=201, policy=no_overtime,
        )
        payable_employee, payable_attendance = self.create_employee_overtime(
            paycode='HAS_OT', card=202, policy=payable_policy,
        )

        response = self.client.post(
            '/api/generate-attendance-reports',
            self.daily_payload([no_ot_employee.pk, payable_employee.pk]),
            format='json',
        )

        self.assertEqual(response.status_code, 200)
        rows = generator.call_args.args[1]
        self.assertEqual([row['attendance'].pk for row in rows], [payable_attendance.pk])
        self.assertEqual(rows[0]['overtime_result'].policy_eligible_gross_minutes, 60)
        self.assertEqual(rows[0]['overtime_result'].net_minutes, 60)

    @patch('api.views.generate_overtime_sheet_daily', return_value=[b'%PDF'])
    def test_daily_report_keeps_fully_late_deducted_policy_eligible_overtime(self, generator):
        payable_policy = OvertimePolicy.objects.get(company=self.company, code='ALL_DAYS_SINGLE')
        employee, attendance = self.create_employee_overtime(
            paycode='FULL_DEDUCTION',
            card=205,
            policy=payable_policy,
            late_min=60,
            late_deduction=True,
        )

        response = self.client.post(
            '/api/generate-attendance-reports',
            self.daily_payload([employee.pk]),
            format='json',
        )

        self.assertEqual(response.status_code, 200)
        rows = generator.call_args.args[1]
        self.assertEqual([row['attendance'].pk for row in rows], [attendance.pk])
        result = rows[0]['overtime_result']
        self.assertEqual(result.policy_eligible_gross_minutes, 60)
        self.assertEqual(result.deducted_late_minutes, 60)
        self.assertEqual(result.net_minutes, 0)
        self.assertEqual(result.amount, 0)

    @patch('api.views.generate_overtime_sheet_daily')
    def test_daily_report_returns_not_found_when_only_raw_no_overtime_exists(self, generator):
        no_overtime = OvertimePolicy.objects.get(company=self.company, code='NO_OVERTIME')
        employee, _ = self.create_employee_overtime(
            paycode='NO_OT_ONLY', card=203, policy=no_overtime,
        )

        response = self.client.post(
            '/api/generate-attendance-reports',
            self.daily_payload([employee.pk]),
            format='json',
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data['detail'], 'No OT Employees on this date')
        generator.assert_not_called()

    @patch('api.views.generate_overtime_sheet')
    def test_monthly_report_excludes_zero_policy_calculated_snapshot(self, generator):
        no_overtime = OvertimePolicy.objects.get(company=self.company, code='NO_OVERTIME')
        employee = self.create_employee(
            paycode='NO_OT_MONTHLY',
            attendance_card_no=204,
            overtime_policy=no_overtime,
        )
        self.create_prepared_salary(employee, net_minutes=0, amount=0)

        response = self.client.post(
            '/api/generate-salary-overtime-sheet',
            self.monthly_payload([employee.pk]),
            format='json',
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data['detail'], 'No Overtime for any Employee in the given month')
        generator.assert_not_called()
