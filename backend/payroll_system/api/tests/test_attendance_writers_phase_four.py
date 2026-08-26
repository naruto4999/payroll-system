from datetime import date, datetime, time
from io import BytesIO
from unittest.mock import patch
from zoneinfo import ZoneInfo

import pandas as pd
from django.contrib import admin
from django.core.exceptions import ValidationError
from django.test import TestCase
from rest_framework.test import APIClient

from api.models import (
    Company,
    EmployeeAttendance,
    EmployeeAttendanceOvertimeDetail,
    OwnerToRegular,
    Regular,
    SubUserMiscSettings,
    SubUserOvertimeSettings,
    User,
)
from api.tests.base import AttendanceTestDataMixin


class AttendanceWriterPhaseFourTests(AttendanceTestDataMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.employee = cls.create_employee(cls, overtime_type='no_overtime')
        cls.employee.visible = True
        cls.employee.save(update_fields=['visible'])
        cls.regular = Regular.objects.create_user(
            username='regular',
            email='regular@example.com',
            password='password',
            phone_no=9999999998,
        )
        OwnerToRegular.objects.create(owner=cls.user, user=cls.regular)
        SubUserMiscSettings.objects.create(user=cls.user, company=cls.company)

    def test_autofill_destructively_cascades_details_and_writes_canonical_null(self):
        old_attendance = self.create_attendance(self.employee, work_date=date(2024, 1, 2), ot_min=20)
        old_detail = self.create_overtime_detail(old_attendance, minutes=20)

        with patch('api.models.EmployeeGenerativeLeaveRecord.objects.generate_update_monthly_record'):
            EmployeeAttendance.objects.bulk_autofill(
                from_date=date(2024, 1, 2),
                to_date=date(2024, 1, 2),
                company_id=self.company.id,
                user=self.user,
                employee_ids=[self.employee.id],
            )

        replacement = EmployeeAttendance.objects.get(
            user=self.user, employee=self.employee, date=date(2024, 1, 2),
        )
        self.assertIsNone(replacement.ot_min)
        self.assertFalse(EmployeeAttendanceOvertimeDetail.objects.filter(pk=old_detail.pk).exists())
        self.assertFalse(replacement.overtime_details.exists())

    def test_autofill_rolls_back_destructive_replacement_when_summary_fails(self):
        old_attendance = self.create_attendance(self.employee, work_date=date(2024, 1, 2), ot_min=20)
        old_detail = self.create_overtime_detail(old_attendance, minutes=20)

        with patch(
            'api.models.EmployeeGenerativeLeaveRecord.objects.generate_update_monthly_record',
            side_effect=RuntimeError('summary failed'),
        ):
            with self.assertRaisesRegex(RuntimeError, 'summary failed'):
                EmployeeAttendance.objects.bulk_autofill(
                    from_date=date(2024, 1, 2),
                    to_date=date(2024, 1, 2),
                    company_id=self.company.id,
                    user=self.user,
                    employee_ids=[self.employee.id],
                )

        self.assertTrue(EmployeeAttendance.objects.filter(pk=old_attendance.pk).exists())
        self.assertTrue(EmployeeAttendanceOvertimeDetail.objects.filter(pk=old_detail.pk).exists())

    def test_autofill_rejects_employee_outside_requested_company(self):
        other_owner = User.objects.create_user(
            username='writer-other-owner',
            email='writer-other-owner@example.com',
            password='password',
            phone_no=9999999996,
        )
        other_company = Company.objects.create(user=other_owner, name='Writer Other')
        other_employee = self.employee.__class__.objects.create(
            user=other_owner,
            company=other_company,
            name='Other employee',
            paycode='OTHER',
            attendance_card_no=999,
            gender='M',
        )

        with self.assertRaisesMessage(ValidationError, 'Every employee must belong to the requested company.'):
            EmployeeAttendance.objects.bulk_autofill(
                from_date=date(2024, 1, 2),
                to_date=date(2024, 1, 2),
                company_id=self.company.id,
                user=self.user,
                employee_ids=[other_employee.id],
            )

    def test_default_creation_rolls_back_when_summary_fails(self):
        with patch(
            'api.models.EmployeeGenerativeLeaveRecord.objects.generate_update_monthly_record',
            side_effect=RuntimeError('summary failed'),
        ):
            with self.assertRaisesRegex(RuntimeError, 'summary failed'):
                EmployeeAttendance.objects.mark_default_attendance(
                    from_date=date(2024, 1, 2),
                    to_date=date(2024, 1, 2),
                    company_id=self.company.id,
                    user=self.user,
                )

        self.assertFalse(EmployeeAttendance.objects.filter(
            user=self.user, employee=self.employee, date=date(2024, 1, 2),
        ).exists())

    def test_transfer_derives_raw_transfer_interval_without_legacy_gate(self):
        source = EmployeeAttendance.objects.create(
            user=self.user,
            company=self.company,
            employee=self.employee,
            date=date(2024, 1, 3),
            machine_in=time(8, 0),
            machine_out=time(18, 0),
            first_half=self.leave_present,
            second_half=self.leave_present,
        )
        SubUserOvertimeSettings.objects.create(
            user=self.user,
            company=self.company,
            date=source.date,
            max_ot_hrs=1,
        )

        with patch('api.models.EmployeeGenerativeLeaveRecord.objects.generate_update_monthly_record'):
            EmployeeAttendance.objects.transfer_attendance_from_owner_to_regular(
                month=1,
                year=2024,
                company_id=self.company.id,
                user=self.user,
            )

        target = EmployeeAttendance.objects.get(user=self.regular, employee=self.employee, date=source.date)
        self.assertEqual(target.machine_in, time(8, 50))
        self.assertEqual(target.machine_out, time(18, 0))
        self.assertEqual(target.ot_min, 60)
        detail = target.overtime_details.get()
        self.assertEqual(detail.source, 'TRANSFER')
        self.assertEqual(detail.gross_minutes, 60)
        payroll_tz = ZoneInfo(self.company.company_details.payroll_timezone)
        self.assertEqual(detail.start_datetime.astimezone(payroll_tz), datetime(2024, 1, 3, 17, 0, tzinfo=payroll_tz))
        self.assertEqual(detail.end_datetime.astimezone(payroll_tz), datetime(2024, 1, 3, 18, 0, tzinfo=payroll_tz))

    def test_daily_weekly_off_transfer_uses_regular_interval_geometry(self):
        employee = self.create_employee(
            paycode='TRANSFER-DAILY',
            attendance_card_no=204,
            salary_mode='daily',
            weekly_off='sun',
        )
        employee.visible = True
        employee.save(update_fields=['visible'])
        source = EmployeeAttendance.objects.create(
            user=self.user,
            company=self.company,
            employee=employee,
            date=date(2024, 1, 7),
            machine_in=time(8, 0),
            machine_out=time(18, 0),
            first_half=self.leave_present,
            second_half=self.leave_present,
        )
        SubUserOvertimeSettings.objects.create(
            user=self.user,
            company=self.company,
            date=source.date,
            max_ot_hrs=8,
        )

        with patch('api.models.EmployeeGenerativeLeaveRecord.objects.generate_update_monthly_record'):
            EmployeeAttendance.objects.transfer_attendance_from_owner_to_regular(
                month=1,
                year=2024,
                company_id=self.company.id,
                user=self.user,
            )

        target = EmployeeAttendance.objects.get(user=self.regular, employee=employee, date=source.date)
        self.assertEqual(target.ot_min, 60)
        detail = target.overtime_details.get()
        self.assertEqual((detail.source, detail.day_type, detail.gross_minutes), ('TRANSFER', 'WEEKLY_OFF', 60))

    def test_manual_mdb_and_transfer_writers_persist_equivalent_split_facts(self):
        work_date = date(2024, 1, 6)
        expected_fact = [
            (date(2024, 1, 6), 'REGULAR', 420),
            (date(2024, 1, 7), 'WEEKLY_OFF', 30),
        ]
        manual_create_employee = self.create_employee(paycode='PARITY-C', attendance_card_no=201)
        manual_update_employee = self.create_employee(paycode='PARITY-U', attendance_card_no=202)
        imported_employee = self.create_employee(paycode='PARITY-I', attendance_card_no=203)
        update_attendance = self.create_attendance(manual_update_employee, work_date=work_date)

        def manual_row(employee, **overrides):
            row = {
                'employee': employee.id,
                'company': self.company.id,
                'date': work_date.isoformat(),
                'firstHalf': self.leave_present.id,
                'secondHalf': self.leave_present.id,
                'manualMode': True,
                'overtimeIntervals': [{
                    'startDatetime': '2024-01-06T17:00:00+05:30',
                    'endDatetime': '2024-01-07T00:30:00+05:30',
                }],
                'overtimeDurationEntries': [],
            }
            row.update(overrides)
            return row

        client = APIClient()
        client.force_authenticate(self.user)
        with patch('api.views.EmployeeGenerativeLeaveRecord.objects.generate_update_monthly_record'):
            create_response = client.post(
                f'/api/employee-attendance/{self.company.id}/{manual_create_employee.id}',
                {'employeeAttendance': [manual_row(manual_create_employee)]},
                format='json',
            )
            update_response = client.put(
                f'/api/employee-attendance-update/{self.company.id}/{manual_update_employee.id}',
                {'employeeAttendance': [manual_row(manual_update_employee, id=update_attendance.id)]},
                format='json',
            )
        self.assertEqual(create_response.status_code, 200, create_response.data)
        self.assertEqual(update_response.status_code, 200, update_response.data)

        checkins = pd.DataFrame(
            [[5001, '01/06/24 09:00:00'], [5001, '01/07/24 00:30:00']],
            columns=['USERID', 'CHECKTIME'],
        )
        users = pd.DataFrame(
            [[5001, str(imported_employee.attendance_card_no)]],
            columns=['USERID', 'Badgenumber'],
        )

        def read_table(_path, table):
            return {'CHECKINOUT': checkins, 'USERINFO': users}[table].copy()

        with patch('api.managers.mdb.read_table', side_effect=read_table):
            with patch('api.models.EmployeeGenerativeLeaveRecord.objects.generate_update_monthly_record'):
                EmployeeAttendance.objects.machine_attendance(
                    from_date=work_date,
                    to_date=work_date,
                    company_id=self.company.id,
                    user=self.user,
                    all_employees_machine_attendance=False,
                    mdb_database=BytesIO(b'fake-mdb'),
                    employee=imported_employee.id,
                )

        EmployeeAttendance.objects.create(
            user=self.user,
            company=self.company,
            employee=self.employee,
            date=work_date,
            machine_in=time(9, 0),
            machine_out=time(0, 30),
            first_half=self.leave_present,
            second_half=self.leave_present,
        )
        SubUserOvertimeSettings.objects.create(
            user=self.user, company=self.company, date=work_date, max_ot_hrs=8,
        )
        with patch('api.models.EmployeeGenerativeLeaveRecord.objects.generate_update_monthly_record'):
            EmployeeAttendance.objects.transfer_attendance_from_owner_to_regular(
                month=1, year=2024, company_id=self.company.id, user=self.user,
            )

        written = (
            (manual_create_employee, self.user, {'MANUAL'}),
            (manual_update_employee, self.user, {'MANUAL'}),
            (imported_employee, self.user, {'LATE_DEPARTURE'}),
            (self.employee, self.regular, {'TRANSFER'}),
        )
        for employee, actor, expected_sources in written:
            with self.subTest(employee=employee.paycode, source=expected_sources):
                attendance = EmployeeAttendance.objects.get(
                    employee=employee, user=actor, date=work_date,
                )
                details = attendance.overtime_details.order_by('work_date')
                self.assertEqual(
                    list(details.values_list('work_date', 'day_type', 'eligible_minutes')),
                    expected_fact,
                )
                self.assertEqual(set(details.values_list('source', flat=True)), expected_sources)
                self.assertEqual(attendance.ot_min, 450)

    def test_transfer_rolls_back_attendance_and_details_when_summary_fails(self):
        EmployeeAttendance.objects.create(
            user=self.user,
            company=self.company,
            employee=self.employee,
            date=date(2024, 1, 4),
            machine_in=time(9, 0),
            machine_out=time(18, 0),
            first_half=self.leave_present,
            second_half=self.leave_present,
        )
        SubUserOvertimeSettings.objects.create(
            user=self.user, company=self.company, date=date(2024, 1, 4), max_ot_hrs=1,
        )

        with patch(
            'api.models.EmployeeGenerativeLeaveRecord.objects.generate_update_monthly_record',
            side_effect=RuntimeError('summary failed'),
        ):
            with self.assertRaisesRegex(RuntimeError, 'summary failed'):
                EmployeeAttendance.objects.transfer_attendance_from_owner_to_regular(
                    month=1,
                    year=2024,
                    company_id=self.company.id,
                    user=self.user,
                )

        self.assertFalse(EmployeeAttendance.objects.filter(user=self.regular, employee=self.employee).exists())
        self.assertFalse(EmployeeAttendanceOvertimeDetail.objects.filter(
            attendance__user=self.regular, attendance__employee=self.employee,
        ).exists())


class AttendanceUtilityPhaseFourTests(AttendanceTestDataMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.employee = cls.create_employee(cls)

    def test_attendance_deletion_cascades_overtime_details(self):
        attendance = self.create_attendance(self.employee, ot_min=30)
        detail = self.create_overtime_detail(attendance, minutes=30)

        attendance.delete()

        self.assertFalse(EmployeeAttendanceOvertimeDetail.objects.filter(pk=detail.pk).exists())

    def test_admin_prevents_direct_overtime_and_punch_edits(self):
        self.assertNotIn(EmployeeAttendance, admin.site._registry)
        self.assertNotIn(EmployeeAttendanceOvertimeDetail, admin.site._registry)


class AttendanceWriterApiAuthorizationTests(AttendanceTestDataMixin, TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_active_writer_endpoints_require_authentication(self):
        requests = (
            ('/api/employee-attendance-bulk-autofill', {'company': self.company.id, 'year': 2024, 'month': 1, 'monthFromDate': 1, 'monthToDate': 1}),
            ('/api/bulk-default-attendance', {'company': self.company.id, 'year': 2024, 'month': 1}),
            ('/api/employee-machine-attendance', {}),
            ('/api/attendance-transfer-owner-to-regular', {'company': self.company.id, 'year': 2024, 'month': 1}),
        )
        for url, payload in requests:
            with self.subTest(url=url):
                self.assertEqual(self.client.post(url, payload).status_code, 401)

    def test_default_writer_rejects_another_owners_company(self):
        other = User.objects.create_user(
            username='other-owner',
            email='other-owner@example.com',
            password='password',
            phone_no=9999999997,
        )
        other_company = Company.objects.create(user=other, name='Other')
        self.client.force_authenticate(self.user)

        response = self.client.post(
            '/api/bulk-default-attendance',
            {'company': other_company.id, 'year': 2024, 'month': 1},
        )

        self.assertEqual(response.status_code, 404)
