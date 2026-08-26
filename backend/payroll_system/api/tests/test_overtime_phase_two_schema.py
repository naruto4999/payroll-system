from datetime import date, datetime, timedelta, timezone as datetime_timezone
from decimal import Decimal

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.test import TestCase, TransactionTestCase
from rest_framework.test import APIClient

from api.models import (
    Company,
    CompanyDetails,
    EmployeeAttendanceOvertimeDetail,
    EmployeeSalaryPrepared,
    EmployeeSalaryPreparedOvertimeDetail,
    OvertimePolicy,
    User,
)
from api.services.overtime_policy import ensure_standard_overtime_policies
from api.tests.base import AttendanceTestDataMixin


class PhaseTwoModelValidationTests(AttendanceTestDataMixin, TestCase):
    def setUp(self):
        self.employee = self.create_employee()
        self.attendance = self.create_attendance(self.employee)

    def exact_detail(self, start, end, **overrides):
        values = {
            'attendance': self.attendance,
            'work_date': date(2024, 1, 2),
            'day_type': 'REGULAR',
            'source': 'MANUAL',
            'start_datetime': start,
            'end_datetime': end,
            'gross_minutes': 30,
            'excluded_minutes': 0,
            'eligible_minutes': 30,
        }
        values.update(overrides)
        return EmployeeAttendanceOvertimeDetail(**values)

    def test_company_details_are_provisioned_with_explicit_payroll_timezone(self):
        details = CompanyDetails.objects.get(company=self.company)
        self.assertEqual(details.payroll_timezone, settings.PAYROLL_DEFAULT_TIMEZONE)
        self.assertEqual(details.user, self.user)

        policies = ensure_standard_overtime_policies(self.company)
        self.assertTrue(all(policy.rounding_increment_minutes == 30 for policy in policies.values()))
        self.assertTrue(all(policy.round_up_from_minutes == 16 for policy in policies.values()))
        system_policy = policies['ALL_DAYS_DOUBLE']
        system_policy.rounding_increment_minutes = 45
        system_policy.round_up_from_minutes = 25
        system_policy.save()

        ensure_standard_overtime_policies(self.company)
        system_policy.refresh_from_db()
        self.assertEqual((system_policy.rounding_increment_minutes, system_policy.round_up_from_minutes), (45, 25))

    def test_invalid_iana_timezone_is_rejected(self):
        details = self.company.company_details
        details.payroll_timezone = 'Not/A_Timezone'
        with self.assertRaises(ValidationError):
            details.full_clean()

    def test_company_details_post_updates_provisioned_row_and_preserves_timezone(self):
        client = APIClient()
        client.force_authenticate(self.user)

        response = client.post('/api/company-details', {
            'company': self.company.pk,
            'address': 'Updated address',
        }, format='json')

        self.assertEqual(response.status_code, 201, response.data)
        self.assertEqual(CompanyDetails.objects.filter(company=self.company).count(), 1)
        details = CompanyDetails.objects.get(company=self.company)
        self.assertEqual(details.address, 'Updated address')
        self.assertEqual(details.payroll_timezone, settings.PAYROLL_DEFAULT_TIMEZONE)

    def test_company_details_post_rejects_cross_company_scope(self):
        other_owner = User.objects.create_user(
            username='details-other',
            email='details-other@example.com',
            password='password',
            phone_no=9999999901,
        )
        other_company = Company.objects.create(user=other_owner, name='Other details')
        client = APIClient()
        client.force_authenticate(self.user)

        response = client.post('/api/company-details', {'company': other_company.pk}, format='json')

        self.assertEqual(response.status_code, 400)
        self.assertIn('company', response.data)

    def test_exact_interval_requires_awareness_exact_minutes_and_local_work_date(self):
        aware_start = datetime(2024, 1, 2, 12, 0, tzinfo=datetime_timezone.utc)
        self.exact_detail(aware_start, aware_start + timedelta(minutes=30)).full_clean()

        with self.assertRaises(ValidationError):
            self.exact_detail(datetime(2024, 1, 2, 12), datetime(2024, 1, 2, 12, 30)).full_clean()
        with self.assertRaises(ValidationError):
            self.exact_detail(aware_start, aware_start + timedelta(minutes=30, seconds=1)).full_clean()
        with self.assertRaises(ValidationError):
            self.exact_detail(aware_start, aware_start + timedelta(days=1)).full_clean()

    def test_following_local_midnight_is_allowed_and_overlap_is_rejected(self):
        midnight_segment_start = datetime(2024, 1, 2, 18, 0, tzinfo=datetime_timezone.utc)
        self.exact_detail(
            midnight_segment_start,
            midnight_segment_start + timedelta(minutes=30),
        ).full_clean()

        first_start = datetime(2024, 1, 2, 17, 0, tzinfo=datetime_timezone.utc)
        first = self.exact_detail(first_start, first_start + timedelta(minutes=30))
        first.save()

        adjacent_start = first.end_datetime
        self.exact_detail(adjacent_start, adjacent_start + timedelta(minutes=30)).full_clean()
        with self.assertRaises(ValidationError):
            self.exact_detail(first_start + timedelta(minutes=15), first_start + timedelta(minutes=45)).full_clean()

    def test_duration_only_entries_and_new_sources_remain_valid(self):
        for source in ('LEGACY_BACKFILL', 'TRANSFER', 'EARNED_SALARY'):
            detail = EmployeeAttendanceOvertimeDetail(
                attendance=self.attendance,
                work_date=self.attendance.date,
                day_type='REGULAR',
                source=source,
                gross_minutes=30,
                excluded_minutes=5,
                eligible_minutes=25,
                exclusion_reason='MEAL_BREAK',
            )
            detail.full_clean()

    def test_exclusion_metadata_validation_and_legacy_write_protection(self):
        for values in (
            {'excluded_minutes': 0, 'eligible_minutes': 30, 'exclusion_reason': 'MEAL_BREAK'},
            {'excluded_minutes': 0, 'eligible_minutes': 30, 'exclusion_note': 'unexpected'},
            {'excluded_minutes': 5, 'eligible_minutes': 25, 'exclusion_reason': 'NONE'},
            {'excluded_minutes': 5, 'eligible_minutes': 25, 'exclusion_reason': 'OTHER'},
            {'excluded_minutes': 5, 'eligible_minutes': 25, 'exclusion_reason': 'LEGACY_UNSPECIFIED'},
        ):
            detail = EmployeeAttendanceOvertimeDetail(
                attendance=self.attendance,
                work_date=self.attendance.date,
                day_type='REGULAR',
                source='MANUAL',
                gross_minutes=30,
                **values,
            )
            with self.assertRaises(ValidationError):
                detail.full_clean()

        detail = EmployeeAttendanceOvertimeDetail(
            attendance=self.attendance,
            work_date=self.attendance.date,
            day_type='REGULAR',
            source='MANUAL',
            gross_minutes=30,
            excluded_minutes=5,
            eligible_minutes=25,
            exclusion_reason='MANUAL_ADJUSTMENT',
            exclusion_note='  approved correction  ',
        )
        detail.full_clean()
        self.assertEqual(detail.exclusion_note, 'approved correction')

    def test_detail_rejects_inconsistent_attendance_scope(self):
        other_owner = User.objects.create_user(
            username='scope-other',
            email='scope-other@example.com',
            password='password',
            phone_no=9999999902,
        )
        other_company = Company.objects.create(user=other_owner, name='Other scope')
        other_employee = type(self.employee).objects.create(
            user=other_owner,
            company=other_company,
            name='Other employee',
            paycode='OTHER',
            attendance_card_no=902,
        )
        malformed_attendance = self.create_attendance(self.employee, work_date=date(2024, 1, 3))
        malformed_attendance.employee = other_employee
        malformed_attendance.save()
        detail = EmployeeAttendanceOvertimeDetail(
            attendance=malformed_attendance,
            work_date=malformed_attendance.date,
            day_type='REGULAR',
            source='MANUAL',
            gross_minutes=30,
            excluded_minutes=0,
            eligible_minutes=30,
        )

        with self.assertRaises(ValidationError):
            detail.full_clean()


class PhaseTwoDatabaseConstraintTests(AttendanceTestDataMixin, TransactionTestCase):
    reset_sequences = True

    def setUp(self):
        self.setUpTestData()
        self.employee = self.create_employee()
        self.salary = self.create_prepared_salary(self.employee)

    def assert_integrity_error(self, callback):
        with self.assertRaises(IntegrityError), transaction.atomic():
            callback()

    def test_policy_and_salary_rounding_pair_constraints(self):
        policy = OvertimePolicy.objects.filter(company=self.company).first()
        self.assert_integrity_error(lambda: OvertimePolicy.objects.filter(pk=policy.pk).update(rounding_increment_minutes=0))
        self.assert_integrity_error(lambda: OvertimePolicy.objects.filter(pk=policy.pk).update(round_up_from_minutes=0))
        self.assert_integrity_error(lambda: OvertimePolicy.objects.filter(pk=policy.pk).update(round_up_from_minutes=31))

        self.assertIsNone(self.salary.ot_rounding_increment_minutes)
        self.assertIsNone(self.salary.ot_round_up_from_minutes)
        self.assert_integrity_error(
            lambda: EmployeeSalaryPrepared.objects.filter(pk=self.salary.pk).update(ot_rounding_increment_minutes=30)
        )
        self.assert_integrity_error(
            lambda: EmployeeSalaryPrepared.objects.filter(pk=self.salary.pk).update(
                ot_rounding_increment_minutes=30, ot_round_up_from_minutes=31
            )
        )

    def test_attendance_and_prepared_breakdown_constraints(self):
        attendance = self.create_attendance(self.employee)
        self.assert_integrity_error(lambda: EmployeeAttendanceOvertimeDetail.objects.bulk_create([
            EmployeeAttendanceOvertimeDetail(
                attendance=attendance,
                work_date=attendance.date,
                day_type='REGULAR',
                source='MANUAL',
                gross_minutes=30,
                excluded_minutes=5,
                eligible_minutes=30,
            )
        ]))
        for values in (
            {'net_minutes': 29, 'multiplier': Decimal('1'), 'divisor': Decimal('26')},
            {'net_minutes': 30, 'multiplier': Decimal('0'), 'divisor': Decimal('26')},
            {'net_minutes': 30, 'multiplier': Decimal('1'), 'divisor': Decimal('0')},
        ):
            self.assert_integrity_error(lambda values=values: EmployeeSalaryPreparedOvertimeDetail.objects.bulk_create([
                EmployeeSalaryPreparedOvertimeDetail(
                    salary_prepared=self.salary,
                    day_type='REGULAR',
                    gross_minutes=30,
                    deducted_late_minutes=0,
                    eligible_salary_rate=Decimal('100'),
                    amount=1,
                    **values,
                )
            ]))
