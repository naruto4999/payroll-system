from datetime import date
from unittest.mock import patch

from django.test import TestCase
from rest_framework.test import APIClient

from api.models import EmployeeAttendance, EmployeeProfessionalDetail, OwnerToRegular, Regular
from api.tests.base import AttendanceTestDataMixin


class EmployeeDojAttendanceTests(AttendanceTestDataMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.employee = cls.create_employee(cls, date_of_joining=date(2024, 1, 10))
        cls.regular = Regular.objects.create_user(
            username='doj-regular',
            email='doj-regular@example.com',
            password='password',
            phone_no=9999999998,
        )
        OwnerToRegular.objects.create(owner=cls.user, user=cls.regular)

    def update_doj(self, new_doj):
        client = APIClient()
        client.force_authenticate(user=self.user)
        return client.patch(
            f'/api/employee-professional-detail/{self.company.id}/{self.employee.id}',
            {'company': self.company.id, 'employee': self.employee.id, 'dateOfJoining': new_doj.isoformat()},
            format='json',
        )

    @patch('api.models.EmployeeGenerativeLeaveRecord.objects.generate_update_monthly_record')
    def test_earlier_doj_skips_regular_attendance_for_hidden_company(self, _generate):
        response = self.update_doj(date(2024, 1, 5))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(EmployeeProfessionalDetail.objects.get(employee=self.employee).date_of_joining, date(2024, 1, 5))
        self.assertTrue(EmployeeAttendance.objects.filter(
            user=self.user, employee=self.employee, date=date(2024, 1, 5),
        ).exists())
        self.assertFalse(EmployeeAttendance.objects.filter(user=self.regular, employee=self.employee).exists())

    @patch('api.models.EmployeeGenerativeLeaveRecord.objects.generate_update_monthly_record')
    def test_earlier_doj_generates_regular_attendance_for_visible_company(self, _generate):
        self.company.visible = True
        self.company.save(update_fields=['visible'])

        response = self.update_doj(date(2024, 1, 5))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(EmployeeAttendance.objects.filter(
            user=self.user, employee=self.employee, date=date(2024, 1, 5),
        ).exists())
        self.assertTrue(EmployeeAttendance.objects.filter(
            user=self.regular, employee=self.employee, date=date(2024, 1, 5),
        ).exists())

    def test_later_doj_deletes_hidden_regular_attendance_before_new_doj(self):
        for actor in (self.user, self.regular):
            for work_date in (date(2024, 1, 10), date(2024, 1, 15)):
                EmployeeAttendance.objects.create(
                    user=actor,
                    company=self.company,
                    employee=self.employee,
                    date=work_date,
                    first_half=self.leave_absent,
                    second_half=self.leave_absent,
                )

        response = self.update_doj(date(2024, 1, 15))

        self.assertEqual(response.status_code, 200)
        for actor in (self.user, self.regular):
            self.assertFalse(EmployeeAttendance.objects.filter(
                user=actor, employee=self.employee, date=date(2024, 1, 10),
            ).exists())
            self.assertTrue(EmployeeAttendance.objects.filter(
                user=actor, employee=self.employee, date=date(2024, 1, 15),
            ).exists())
