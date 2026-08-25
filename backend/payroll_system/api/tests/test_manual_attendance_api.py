from datetime import date, time
from unittest.mock import patch

from django.test import TestCase
from rest_framework.test import APIClient

from api.models import EmployeeAttendance, EmployeeAttendanceOvertimeDetail
from api.tests.base import AttendanceTestDataMixin


class ManualAttendanceApiTests(AttendanceTestDataMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.employee = cls.create_employee(cls)

    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(self.user)
        self.create_url = f'/api/employee-attendance/{self.company.id}/{self.employee.id}'
        self.update_url = f'/api/employee-attendance-update/{self.company.id}/{self.employee.id}'

    def row(self, work_date='2024-01-02', **overrides):
        values = {
            'employee': self.employee.id,
            'company': self.company.id,
            'date': work_date,
            'firstHalf': self.leave_present.id,
            'secondHalf': self.leave_present.id,
            'manualMode': True,
            'overtimeIntervals': [],
            'overtimeDurationEntries': [{
                'workDate': work_date,
                'grossMinutes': 50,
                'excludedMinutes': 10,
                'exclusionReason': 'MEAL_BREAK',
                'exclusionNote': '',
            }],
        }
        values.update(overrides)
        return values

    @patch('api.views.EmployeeGenerativeLeaveRecord.objects.generate_update_monthly_record')
    def test_create_binds_scope_ignores_ot_min_and_returns_nested_facts(self, regenerate):
        row = self.row(otMin=999)
        response = self.client.post(self.create_url, {'employeeAttendance': [row]}, format='json')

        self.assertEqual(response.status_code, 200, response.data)
        attendance = EmployeeAttendance.objects.get(employee=self.employee, date=date(2024, 1, 2))
        self.assertEqual(attendance.ot_min, 40)
        self.assertEqual(response.data[0]['ot_min'], 40)
        detail = response.data[0]['overtime_details'][0]
        self.assertEqual(detail['source'], 'MANUAL')
        self.assertEqual(detail['gross_minutes'], 50)
        self.assertEqual(detail['excluded_minutes'], 10)
        self.assertEqual(detail['eligible_minutes'], 40)
        self.assertEqual(detail['exclusion_reason'], 'MEAL_BREAK')
        self.assertEqual(detail['exclusion_reason_display'], 'Meal Break')
        self.assertIn('exclusion_note', detail)
        regenerate.assert_called_once()

    @patch('api.views.EmployeeGenerativeLeaveRecord.objects.generate_update_monthly_record')
    def test_update_replaces_and_clears_details_atomically(self, regenerate):
        first = self.create_attendance(self.employee, work_date=date(2024, 1, 2))
        second = self.create_attendance(self.employee, work_date=date(2024, 1, 3))
        self.create_overtime_detail(first, minutes=30)
        EmployeeAttendance.objects.filter(pk=first.pk).update(ot_min=30)

        rows = [
            self.row(id=first.id, overtimeDurationEntries=[]),
            self.row(
                work_date='2024-01-03',
                id=second.id,
                overtimeDurationEntries=[{'workDate': '2024-01-03', 'grossMinutes': 25}],
            ),
        ]
        response = self.client.put(self.update_url, {'employeeAttendance': rows}, format='json')

        self.assertEqual(response.status_code, 200, response.data)
        first.refresh_from_db()
        second.refresh_from_db()
        self.assertIsNone(first.ot_min)
        self.assertFalse(first.overtime_details.exists())
        self.assertEqual(second.ot_min, 25)
        self.assertEqual(second.overtime_details.get().source, 'MANUAL')
        regenerate.assert_called_once()

    @patch('api.views.EmployeeGenerativeLeaveRecord.objects.generate_update_monthly_record')
    def test_exact_interval_uses_manual_source_and_regenerates_each_affected_month(self, regenerate):
        row = self.row(work_date='2024-01-31')
        row['manualIn'] = '09:30'
        row['manualOut'] = '01:30'
        row['overtimeDurationEntries'] = []
        row['overtimeIntervals'] = [{
            'startDatetime': '2024-01-31T18:00:00+05:30',
            'endDatetime': '2024-02-01T01:30:00+05:30',
        }]

        response = self.client.post(self.create_url, {'employeeAttendance': [row]}, format='json')

        self.assertEqual(response.status_code, 200, response.data)
        details = EmployeeAttendanceOvertimeDetail.objects.order_by('work_date')
        self.assertEqual(list(details.values_list('work_date', flat=True)), [date(2024, 1, 31), date(2024, 2, 1)])
        attendance = EmployeeAttendance.objects.get(date=date(2024, 1, 31))
        self.assertEqual(attendance.manual_out, time(1, 30))
        self.assertEqual({detail.attendance.pk for detail in details}, {attendance.pk})
        self.assertEqual(list(details.values_list('gross_minutes', flat=True)), [360, 90])
        self.assertEqual(attendance.ot_min, 450)
        self.assertEqual(set(details.values_list('source', flat=True)), {'MANUAL'})
        self.assertEqual(regenerate.call_count, 2)

    @patch('api.views.EmployeeGenerativeLeaveRecord.objects.generate_update_monthly_record')
    def test_invalid_later_row_rolls_back_attendance_and_details(self, regenerate):
        first = self.create_attendance(self.employee, work_date=date(2024, 1, 2))
        second = self.create_attendance(self.employee, work_date=date(2024, 1, 3))
        rows = [
            self.row(id=first.id, manualIn='08:00'),
            self.row(
                work_date='2024-01-03',
                id=second.id,
                overtimeDurationEntries=[{
                    'workDate': '2024-01-03',
                    'grossMinutes': 10,
                    'excludedMinutes': 10,
                    'exclusionReason': 'MEAL_BREAK',
                }],
            ),
        ]

        response = self.client.put(self.update_url, {'employeeAttendance': rows}, format='json')

        self.assertEqual(response.status_code, 400, response.data)
        first.refresh_from_db()
        self.assertIsNone(first.manual_in)
        self.assertFalse(first.overtime_details.exists())
        regenerate.assert_not_called()

    def test_legacy_positive_update_without_replacement_is_controlled(self):
        attendance = self.create_attendance(self.employee, ot_min=30)
        row = self.row(id=attendance.id)
        row.pop('overtimeIntervals')
        row.pop('overtimeDurationEntries')

        response = self.client.put(self.update_url, {'employeeAttendance': [row]}, format='json')

        self.assertEqual(response.status_code, 409, response.data)
        self.assertEqual(response.data['unbackfilled_overtime']['attendance_id'], attendance.id)
        attendance.refresh_from_db()
        self.assertEqual(attendance.ot_min, 30)

    def test_scope_month_validation_and_nested_list_serializer(self):
        attendance = self.create_attendance(self.employee)
        self.create_overtime_detail(
            attendance,
            minutes=30,
            excluded_minutes=5,
            exclusion_reason='OTHER',
            exclusion_note='approved',
        )
        EmployeeAttendance.objects.filter(pk=attendance.pk).update(ot_min=25)

        list_url = f'/api/all-employee-attendance/{self.company.id}/2024/1'
        response = self.client.get(list_url)
        self.assertEqual(response.status_code, 200, response.data)
        attendance_data = response.data[0]
        self.assertEqual(attendance_data['employee'], self.employee.id)
        self.assertEqual(attendance_data['company'], self.company.id)
        self.assertEqual(attendance_data['first_half'], self.leave_present.id)
        self.assertEqual(attendance_data['second_half'], self.leave_present.id)
        self.assertNotIn('employee_id', attendance_data)
        self.assertNotIn('first_half_id', attendance_data)
        overtime_detail = attendance_data['overtime_details'][0]
        self.assertEqual(overtime_detail['attendance'], attendance.date)
        self.assertEqual(overtime_detail['exclusion_reason_display'], 'Other')
        self.assertEqual(overtime_detail['exclusion_note'], 'approved')

        mixed_scope = self.row(company=self.company.id + 999)
        response = self.client.post(self.create_url, {'employeeAttendance': [mixed_scope]}, format='json')
        self.assertEqual(response.status_code, 400)

        mixed_month = [self.row(), self.row(work_date='2024-02-01')]
        response = self.client.post(self.create_url, {'employeeAttendance': mixed_month}, format='json')
        self.assertEqual(response.status_code, 400)
