from datetime import date

from django.core.exceptions import ValidationError
from django.test import TestCase

from api.models import EmployeePersonalDetail, EmployeeProfessionalDetail
from api.tests.base import AttendanceTestDataMixin


class EmployeeModelTests(AttendanceTestDataMixin, TestCase):
    def test_employee_professional_detail_requires_resignation_date_for_resigned_employee(self):
        employee = EmployeePersonalDetail.objects.create(
            user=self.user,
            company=self.company,
            name="Employee E005",
            paycode="E005",
            attendance_card_no=105,
            gender="M",
        )

        with self.assertRaises(ValidationError):
            EmployeeProfessionalDetail.objects.create(
                user=self.user,
                company=self.company,
                employee=employee,
                date_of_joining=date(2024, 1, 1),
                date_of_confirm=date(2024, 1, 1),
                resigned=True,
                resignation_date=None,
            )
