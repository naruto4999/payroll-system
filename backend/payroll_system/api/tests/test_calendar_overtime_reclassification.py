from datetime import date, datetime, timedelta
from unittest.mock import patch
from zoneinfo import ZoneInfo

from django.test import TestCase
from rest_framework.test import APIClient

from api.models import (
    EmployeeAttendance,
    EmployeeProfessionalDetail,
    EmployeeSalaryDetail,
    OwnerToRegular,
    Regular,
)
from api.services.attendance_overtime import replace_attendance_overtime
from api.tests.base import AttendanceTestDataMixin


class CalendarOvertimeReclassificationTests(AttendanceTestDataMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.employee = cls.create_employee(cls, weekly_off='sun')
        cls.employee.visible = True
        cls.employee.save(update_fields=['visible'])
        cls.regular = Regular.objects.create_user(
            username='calendar-regular',
            email='calendar-regular@example.com',
            password='password',
            phone_no=9999999998,
        )
        OwnerToRegular.objects.create(owner=cls.user, user=cls.regular)

    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def create_preserved_detail(self, *, actor=None, work_date=date(2024, 1, 3)):
        actor = actor or self.user
        attendance = EmployeeAttendance.objects.create(
            user=actor,
            company=self.company,
            employee=self.employee,
            date=work_date,
            first_half=self.leave_present,
            second_half=self.leave_present,
        )
        payroll_tz = ZoneInfo(self.company.company_details.payroll_timezone)
        start = datetime.combine(work_date, datetime.min.time(), tzinfo=payroll_tz) + timedelta(hours=18)
        detail = replace_attendance_overtime(
            attendance=attendance,
            intervals=[{
                'start_datetime': start,
                'end_datetime': start + timedelta(minutes=45),
                'excluded_minutes': 5,
                'exclusion_reason': 'OTHER',
                'exclusion_note': 'approved',
            }],
            source='TRANSFER',
            actor=actor,
        )[0]
        return attendance, detail

    @staticmethod
    def preserved_values(detail):
        return {
            field.attname: getattr(detail, field.attname)
            for field in detail._meta.concrete_fields
            if field.name not in {'day_type', 'updated_at'}
        }

    def test_holiday_create_reclassifies_owner_and_linked_regular_details_in_place(self):
        _, owner_detail = self.create_preserved_detail()
        _, regular_detail = self.create_preserved_detail(actor=self.regular)
        owner_before = self.preserved_values(owner_detail)
        regular_before = self.preserved_values(regular_detail)

        response = self.client.post(
            f'/api/holiday/{self.company.pk}',
            {'company': self.company.pk, 'name': 'Calendar holiday', 'date': '2024-01-03'},
            format='json',
        )

        self.assertEqual(response.status_code, 201)
        owner_detail.refresh_from_db()
        regular_detail.refresh_from_db()
        self.assertEqual(owner_detail.day_type, 'HOLIDAY')
        self.assertEqual(regular_detail.day_type, 'HOLIDAY')
        self.assertEqual(self.preserved_values(owner_detail), owner_before)
        self.assertEqual(self.preserved_values(regular_detail), regular_before)

    def test_holiday_move_and_delete_reclassify_old_and_new_dates(self):
        old_attendance, old_detail = self.create_preserved_detail(work_date=date(2024, 1, 3))
        new_attendance, new_detail = self.create_preserved_detail(work_date=date(2024, 1, 4))
        holiday = self.create_holiday(holiday_date=date(2024, 1, 3), name='Moving holiday')
        old_detail.day_type = 'HOLIDAY'
        old_detail.save(update_fields=['day_type'])

        response = self.client.put(
            f'/api/holiday/{self.company.pk}/{holiday.pk}',
            {'company': self.company.pk, 'name': holiday.name, 'date': '2024-01-04'},
            format='json',
        )
        self.assertEqual(response.status_code, 201)
        old_detail.refresh_from_db()
        new_detail.refresh_from_db()
        self.assertEqual(old_detail.day_type, 'REGULAR')
        self.assertEqual(new_detail.day_type, 'HOLIDAY')

        response = self.client.delete(f'/api/holiday/{self.company.pk}/{holiday.pk}')
        self.assertEqual(response.status_code, 204)
        new_detail.refresh_from_db()
        self.assertEqual(new_detail.day_type, 'REGULAR')
        self.assertEqual(old_attendance.ot_min, new_attendance.ot_min)

    def test_weekly_and_extra_off_update_reclassifies_only_real_calendar_change(self):
        _, weekly_detail = self.create_preserved_detail(work_date=date(2024, 1, 7))
        _, extra_detail = self.create_preserved_detail(work_date=date(2024, 1, 10))
        weekly_detail.day_type = 'WEEKLY_OFF'
        weekly_detail.save(update_fields=['day_type'])

        response = self.client.patch(
            f'/api/employee-professional-detail/{self.company.pk}/{self.employee.pk}',
            {'weekly_off': 'mon', 'extra_off': 'wed2'},
            format='json',
        )

        self.assertEqual(response.status_code, 200)
        weekly_detail.refresh_from_db()
        extra_detail.refresh_from_db()
        self.assertEqual(weekly_detail.day_type, 'REGULAR')
        self.assertEqual(extra_detail.day_type, 'WEEKLY_OFF')

        with patch('api.views.reclassify_many') as reclassify:
            response = self.client.patch(
                f'/api/employee-professional-detail/{self.company.pk}/{self.employee.pk}',
                {'date_of_confirm': '2024-01-02'},
                format='json',
            )
        self.assertEqual(response.status_code, 200)
        reclassify.assert_not_called()

    def test_holiday_name_only_update_does_not_reclassify(self):
        holiday = self.create_holiday(holiday_date=date(2024, 1, 3), name='Original name')
        self.create_preserved_detail(work_date=holiday.date)

        with patch('api.views.reclassify_many') as reclassify:
            response = self.client.put(
                f'/api/holiday/{self.company.pk}/{holiday.pk}',
                {'company': self.company.pk, 'name': 'Corrected name', 'date': '2024-01-03'},
                format='json',
            )

        self.assertEqual(response.status_code, 201)
        reclassify.assert_not_called()

    def test_daily_employee_uses_calendar_meaning_when_calendar_changes(self):
        salary = EmployeeSalaryDetail.objects.get(employee=self.employee)
        salary.salary_mode = 'daily'
        salary.save(update_fields=['salary_mode'])
        _, detail = self.create_preserved_detail(work_date=date(2024, 1, 3))

        response = self.client.post(
            f'/api/holiday/{self.company.pk}',
            {'company': self.company.pk, 'name': 'Daily holiday', 'date': '2024-01-03'},
            format='json',
        )

        self.assertEqual(response.status_code, 201)
        detail.refresh_from_db()
        self.assertEqual(detail.day_type, 'HOLIDAY')

    def test_holiday_and_professional_mutations_roll_back_when_reclassification_fails(self):
        self.create_preserved_detail(work_date=date(2024, 1, 3))
        with patch('api.views.reclassify_many', side_effect=RuntimeError('reclassification failed')):
            with self.assertRaisesRegex(RuntimeError, 'reclassification failed'):
                self.client.post(
                    f'/api/holiday/{self.company.pk}',
                    {'company': self.company.pk, 'name': 'Rolled back', 'date': '2024-01-03'},
                    format='json',
                )
        self.assertFalse(self.user.holidays.filter(name='Rolled back').exists())

        professional = EmployeeProfessionalDetail.objects.get(employee=self.employee)
        self.create_preserved_detail(work_date=date(2024, 1, 7))
        with patch('api.views.reclassify_many', side_effect=RuntimeError('reclassification failed')):
            with self.assertRaisesRegex(RuntimeError, 'reclassification failed'):
                self.client.patch(
                    f'/api/employee-professional-detail/{self.company.pk}/{self.employee.pk}',
                    {'weekly_off': 'mon'},
                    format='json',
                )
        professional.refresh_from_db()
        self.assertEqual(professional.weekly_off, 'sun')

    def test_unbackfilled_aggregate_is_not_selected_for_calendar_edit(self):
        EmployeeAttendance.objects.create(
            user=self.user,
            company=self.company,
            employee=self.employee,
            date=date(2024, 1, 3),
            first_half=self.leave_present,
            second_half=self.leave_present,
            ot_min=30,
        )

        response = self.client.post(
            f'/api/holiday/{self.company.pk}',
            {'company': self.company.pk, 'name': 'No details', 'date': '2024-01-03'},
            format='json',
        )

        self.assertEqual(response.status_code, 201)
