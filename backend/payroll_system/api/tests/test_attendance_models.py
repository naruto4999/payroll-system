from datetime import date

from django.test import TestCase

from api.models import EmployeeAttendance
from api.tests.base import AttendanceTestDataMixin


class AttendanceModelTests(AttendanceTestDataMixin, TestCase):
    def test_employee_attendance_save_sets_half_day_pay_multiplier(self):
        employee = self.create_employee(paycode="E004", attendance_card_no=104, overtime_type="no_overtime")

        attendance = EmployeeAttendance.objects.create(
            user=self.user,
            company=self.company,
            employee=employee,
            date=date(2024, 1, 6),
            first_half=self.leave_present,
            second_half=self.leave_absent,
        )

        self.assertEqual(float(attendance.pay_multiplier), 0.5)
