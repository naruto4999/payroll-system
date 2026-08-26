from concurrent.futures import ThreadPoolExecutor
from datetime import date, datetime, timedelta
from threading import Barrier
from unittest.mock import patch
from zoneinfo import ZoneInfo

from django.core.exceptions import ValidationError
from django.db import close_old_connections
from django.test import TestCase, TransactionTestCase

from api.models import Company, EmployeeAttendance, EmployeeAttendanceOvertimeDetail, User
from api.services.attendance_overtime import (
    OVERTIME_DETAIL_CREATE_BATCH_SIZE,
    OVERTIME_UPDATE_BATCH_SIZE,
    classify_work_date,
    clear_attendance_overtime,
    reclassify_attendance_overtime,
    reclassify_many,
    replace_attendance_overtime,
    replace_many_attendance_overtime,
    split_interval_at_payroll_midnights,
    sync_attendance_ot_min,
)
from api.tests.base import AttendanceTestDataMixin


PAYROLL_TZ = ZoneInfo('Asia/Kolkata')


class AttendanceOvertimeServiceTests(AttendanceTestDataMixin, TestCase):
    def setUp(self):
        self.employee = self.create_employee(weekly_off='tue', extra_off='wed2')
        self.attendance = self.create_attendance(self.employee)

    def duration(self, minutes=30, work_date=date(2024, 1, 2), **overrides):
        entry = {'work_date': work_date, 'gross_minutes': minutes}
        entry.update(overrides)
        return entry

    def test_classification_uses_calendar_for_all_salary_modes(self):
        holiday_date = date(2024, 1, 2)
        self.create_holiday(holiday_date=holiday_date, name='Precedence')
        self.assertEqual(classify_work_date(
            owner=self.user, company=self.company, employee=self.employee, work_date=holiday_date,
        ), 'HOLIDAY')
        self.assertEqual(classify_work_date(
            owner=self.user, company=self.company, employee=self.employee, work_date=date(2024, 1, 10),
        ), 'WEEKLY_OFF')

        daily = self.create_employee(
            paycode='DAILY', attendance_card_no=202, salary_mode='daily', weekly_off='tue', extra_off='wed2',
        )
        self.assertEqual(classify_work_date(
            owner=self.user, company=self.company, employee=daily, work_date=holiday_date,
        ), 'HOLIDAY')
        self.assertEqual(classify_work_date(
            owner=self.user, company=self.company, employee=daily, work_date=date(2024, 1, 9),
        ), 'WEEKLY_OFF')
        self.assertEqual(classify_work_date(
            owner=self.user, company=self.company, employee=daily, work_date=date(2024, 1, 10),
        ), 'WEEKLY_OFF')

    def test_split_converts_timezone_and_handles_month_and_year_boundaries(self):
        start = datetime(2024, 12, 31, 18, 0, tzinfo=ZoneInfo('UTC'))
        segments = split_interval_at_payroll_midnights(
            start_datetime=start,
            end_datetime=start + timedelta(hours=2),
            payroll_timezone='Asia/Kolkata',
        )
        self.assertEqual([item['work_date'] for item in segments], [date(2024, 12, 31), date(2025, 1, 1)])
        self.assertEqual([item['gross_minutes'] for item in segments], [30, 90])
        self.assertEqual(sum(item['gross_minutes'] for item in segments), 120)

        month_end_start = datetime(2024, 1, 31, 18, 0, tzinfo=ZoneInfo('UTC'))
        month_segments = split_interval_at_payroll_midnights(
            start_datetime=month_end_start,
            end_datetime=month_end_start + timedelta(hours=1),
            payroll_timezone='Asia/Kolkata',
        )
        self.assertEqual(
            [item['work_date'] for item in month_segments],
            [date(2024, 1, 31), date(2024, 2, 1)],
        )

    def test_same_day_exact_and_duration_entries_are_raw_and_synchronized(self):
        start = datetime(2024, 1, 2, 19, 0, tzinfo=PAYROLL_TZ)
        created = replace_attendance_overtime(
            attendance=self.attendance,
            intervals=[{'start_datetime': start, 'end_datetime': start + timedelta(minutes=45)}],
            duration_entries=[self.duration(20)],
            source='MANUAL',
            actor=self.user,
        )
        self.assertEqual([detail.gross_minutes for detail in created], [45, 20])
        self.attendance.refresh_from_db()
        self.assertEqual(self.attendance.ot_min, 65)

    def test_replacement_supports_fallback_and_mixed_entry_sources(self):
        start = datetime(2024, 1, 2, 19, 0, tzinfo=PAYROLL_TZ)
        created = replace_attendance_overtime(
            attendance=self.attendance,
            intervals=[{
                'start_datetime': start,
                'end_datetime': start + timedelta(minutes=20),
                'source': 'IMPORTED',
            }],
            duration_entries=[
                self.duration(15, work_date=date(2024, 1, 3)),
                self.duration(10, work_date=date(2024, 1, 4), source='TRANSFER'),
            ],
            source='MANUAL',
            actor=self.user,
        )
        self.assertEqual([detail.source for detail in created], ['IMPORTED', 'MANUAL', 'TRANSFER'])

    def test_sources_are_validated_before_replacement_and_empty_needs_no_source(self):
        original = self.create_overtime_detail(self.attendance, minutes=30)
        for source in (None, 'INVALID'):
            with self.assertRaises(ValidationError):
                replace_attendance_overtime(
                    attendance=self.attendance,
                    duration_entries=[self.duration(source=source)],
                    source='MANUAL',
                    actor=self.user,
                )
            self.assertTrue(EmployeeAttendanceOvertimeDetail.objects.filter(pk=original.pk).exists())

        clear_attendance_overtime(attendance=self.attendance, actor=self.user)
        replace_attendance_overtime(attendance=self.attendance, actor=self.user)
        self.assertFalse(self.attendance.overtime_details.exists())

    def test_midnight_split_classifies_second_segment_holiday(self):
        self.create_holiday(holiday_date=date(2024, 1, 3), name='Next day')
        start = datetime(2024, 1, 2, 23, 30, tzinfo=PAYROLL_TZ)
        created = replace_attendance_overtime(
            attendance=self.attendance,
            intervals=[{'start_datetime': start, 'end_datetime': start + timedelta(hours=1)}],
            source='IMPORTED',
            actor=self.user,
        )
        self.assertEqual([(item.work_date, item.day_type) for item in created], [
            (date(2024, 1, 2), 'WEEKLY_OFF'),
            (date(2024, 1, 3), 'HOLIDAY'),
        ])

    def test_cross_midnight_timed_exclusion_is_allocated_without_guessing(self):
        start = datetime(2024, 1, 2, 23, 30, tzinfo=PAYROLL_TZ)
        created = replace_attendance_overtime(
            attendance=self.attendance,
            intervals=[{
                'start_datetime': start,
                'end_datetime': start + timedelta(hours=1),
                'exclusions': [{
                    'start_datetime': start + timedelta(minutes=40),
                    'end_datetime': start + timedelta(minutes=50),
                    'exclusion_reason': 'MEAL_BREAK',
                }],
            }],
            source='IMPORTED',
            actor=self.user,
        )
        self.assertEqual([item.excluded_minutes for item in created], [0, 10])
        self.assertEqual([item.exclusion_reason for item in created], ['NONE', 'MEAL_BREAK'])
        self.attendance.refresh_from_db()
        self.assertEqual(self.attendance.ot_min, 50)

        with self.assertRaises(ValidationError):
            replace_attendance_overtime(
                attendance=self.attendance,
                intervals=[{
                    'start_datetime': start,
                    'end_datetime': start + timedelta(hours=1),
                    'excluded_minutes': 10,
                    'exclusion_reason': 'MEAL_BREAK',
                }],
                source='IMPORTED',
                actor=self.user,
            )

    def test_exclusion_state_is_trimmed_and_legacy_or_blank_required_note_is_rejected(self):
        created = replace_attendance_overtime(
            attendance=self.attendance,
            duration_entries=[self.duration(
                excluded_minutes=5,
                exclusion_reason='OTHER',
                exclusion_note='  approved exception  ',
            )],
            source='MANUAL',
            actor=self.user,
        )
        self.assertEqual(created[0].exclusion_note, 'approved exception')
        for reason in ('OTHER', 'LEGACY_UNSPECIFIED'):
            with self.assertRaises(ValidationError):
                replace_attendance_overtime(
                    attendance=self.attendance,
                    duration_entries=[self.duration(excluded_minutes=5, exclusion_reason=reason)],
                    source='MANUAL',
                    actor=self.user,
                )

    def test_overlap_duplicate_rejected_and_adjacency_allowed(self):
        start = datetime(2024, 1, 2, 19, 0, tzinfo=PAYROLL_TZ)
        with self.assertRaises(ValidationError):
            replace_attendance_overtime(
                attendance=self.attendance,
                intervals=[
                    {'start_datetime': start, 'end_datetime': start + timedelta(minutes=30)},
                    {'start_datetime': start + timedelta(minutes=15), 'end_datetime': start + timedelta(minutes=45)},
                ],
                source='MANUAL',
                actor=self.user,
            )
        created = replace_attendance_overtime(
            attendance=self.attendance,
            intervals=[
                {'start_datetime': start, 'end_datetime': start + timedelta(minutes=30)},
                {'start_datetime': start + timedelta(minutes=30), 'end_datetime': start + timedelta(minutes=60)},
            ],
            source='MANUAL',
            actor=self.user,
        )
        self.assertEqual(len(created), 2)

    def test_overlap_is_rejected_globally_across_mixed_sources(self):
        start = datetime(2024, 1, 2, 19, 0, tzinfo=PAYROLL_TZ)
        with self.assertRaises(ValidationError):
            replace_attendance_overtime(
                attendance=self.attendance,
                intervals=[
                    {
                        'start_datetime': start,
                        'end_datetime': start + timedelta(minutes=30),
                        'source': 'MANUAL',
                    },
                    {
                        'start_datetime': start + timedelta(minutes=15),
                        'end_datetime': start + timedelta(minutes=45),
                        'source': 'IMPORTED',
                    },
                ],
                actor=self.user,
            )

    def test_replace_clear_sync_and_failure_preserve_previous_state(self):
        original = self.create_overtime_detail(self.attendance, minutes=30)
        self.attendance.ot_min = 30
        self.attendance.save(update_fields=['ot_min'])
        with self.assertRaises(ValidationError):
            replace_attendance_overtime(
                attendance=self.attendance,
                duration_entries=[self.duration(minutes=10, excluded_minutes=10, exclusion_reason='MEAL_BREAK')],
                source='MANUAL',
                actor=self.user,
            )
        self.assertTrue(EmployeeAttendanceOvertimeDetail.objects.filter(pk=original.pk).exists())
        self.attendance.refresh_from_db()
        self.assertEqual(self.attendance.ot_min, 30)

        EmployeeAttendance.objects.filter(pk=self.attendance.pk).update(ot_min=99)
        self.assertEqual(sync_attendance_ot_min(attendance=self.attendance), 30)
        clear_attendance_overtime(attendance=self.attendance, actor=self.user)
        self.attendance.refresh_from_db()
        self.assertIsNone(self.attendance.ot_min)
        self.assertFalse(self.attendance.overtime_details.exists())

    def test_sync_rejects_unbackfilled_positive_overtime(self):
        EmployeeAttendance.objects.filter(pk=self.attendance.pk).update(ot_min=25)
        self.attendance.refresh_from_db()
        with self.assertRaises(ValidationError) as context:
            sync_attendance_ot_min(attendance=self.attendance)
        self.assertIn('unbackfilled_overtime', context.exception.message_dict)
        self.attendance.refresh_from_db()
        self.assertEqual(self.attendance.ot_min, 25)

    def test_reclassify_updates_only_day_type_in_place(self):
        detail = replace_attendance_overtime(
            attendance=self.attendance,
            duration_entries=[self.duration(
                work_date=date(2024, 1, 4),
                excluded_minutes=5,
                exclusion_reason='OTHER',
                exclusion_note='approved',
                source='TRANSFER',
            )],
            actor=self.user,
        )[0]
        before = {
            field.attname: getattr(detail, field.attname)
            for field in detail._meta.concrete_fields
            if field.name != 'day_type'
        }
        self.create_holiday(holiday_date=detail.work_date, name='Reclassified')

        returned = reclassify_attendance_overtime(attendance=self.attendance, actor=self.user)

        detail.refresh_from_db()
        after = {
            field.attname: getattr(detail, field.attname)
            for field in detail._meta.concrete_fields
            if field.name != 'day_type'
        }
        self.assertEqual([item.pk for item in returned], [detail.pk])
        self.assertEqual(detail.day_type, 'HOLIDAY')
        self.assertEqual(after, before)

    def test_reclassify_many_is_deterministic_and_rolls_back_for_unbackfilled(self):
        second = self.create_attendance(self.employee, work_date=date(2024, 1, 3))
        first_detail = replace_attendance_overtime(
            attendance=self.attendance,
            duration_entries=[self.duration(work_date=date(2024, 1, 4))],
            source='MANUAL',
            actor=self.user,
        )[0]
        second_detail = replace_attendance_overtime(
            attendance=second,
            duration_entries=[self.duration(work_date=date(2024, 1, 5))],
            source='IMPORTED',
            actor=self.user,
        )[0]
        self.create_holiday(holiday_date=date(2024, 1, 4), name='First')
        self.create_holiday(holiday_date=date(2024, 1, 5), name='Second')

        returned = reclassify_many(attendances=[second, self.attendance], actor=self.user)
        self.assertEqual([detail.pk for detail in returned], [first_detail.pk, second_detail.pk])

        EmployeeAttendanceOvertimeDetail.objects.filter(pk=second_detail.pk).delete()
        EmployeeAttendance.objects.filter(pk=second.pk).update(ot_min=30)
        EmployeeAttendanceOvertimeDetail.objects.filter(pk=first_detail.pk).update(day_type='REGULAR')
        with self.assertRaises(ValidationError) as context:
            reclassify_many(attendances=[self.attendance, second], actor=self.user)
        self.assertIn('unbackfilled_overtime', context.exception.message_dict)
        first_detail.refresh_from_db()
        self.assertEqual(first_detail.day_type, 'REGULAR')

    def test_ownership_and_many_replacement_are_all_or_nothing(self):
        second = self.create_attendance(self.employee, work_date=date(2024, 1, 3))
        self.create_overtime_detail(self.attendance, minutes=30)
        self.create_overtime_detail(second, minutes=20)
        with self.assertRaises(ValidationError):
            replace_many_attendance_overtime(replacements=[
                {'attendance': self.attendance, 'duration_entries': [self.duration(40)], 'source': 'MANUAL'},
                {'attendance': second, 'duration_entries': [self.duration(10, excluded_minutes=10, exclusion_reason='OTHER')], 'source': 'MANUAL'},
            ], actor=self.user)
        self.assertEqual(self.attendance.overtime_details.get().eligible_minutes, 30)
        self.assertEqual(second.overtime_details.get().eligible_minutes, 20)

        other = User.objects.create_user(
            username='other-owner', email='other-owner@example.com', password='password', phone_no=9666666666,
        )
        other_company = Company.objects.create(user=other, name='Other')
        with self.assertRaises(ValidationError):
            classify_work_date(owner=other, company=other_company, employee=self.employee, work_date=self.attendance.date)
        with self.assertRaises(ValidationError):
            replace_attendance_overtime(
                attendance=self.attendance,
                duration_entries=[self.duration(30)],
                source='MANUAL',
                actor=other,
            )

    def test_many_replacement_bounds_bulk_write_batches(self):
        detail_manager = EmployeeAttendanceOvertimeDetail.objects
        attendance_manager = EmployeeAttendance.objects
        with patch.object(detail_manager, 'bulk_create', wraps=detail_manager.bulk_create) as bulk_create:
            with patch.object(attendance_manager, 'bulk_update', wraps=attendance_manager.bulk_update) as bulk_update:
                replace_many_attendance_overtime(
                    replacements=[{
                        'attendance': self.attendance,
                        'duration_entries': [self.duration(30)],
                        'source': 'MANUAL',
                    }],
                    actor=self.user,
                )

        self.assertEqual(bulk_create.call_args.kwargs['batch_size'], OVERTIME_DETAIL_CREATE_BATCH_SIZE)
        self.assertEqual(bulk_update.call_args.kwargs['batch_size'], OVERTIME_UPDATE_BATCH_SIZE)


class AttendanceOvertimeConcurrencyTests(AttendanceTestDataMixin, TransactionTestCase):
    reset_sequences = True

    def setUp(self):
        self.setUpTestData()
        employee = self.create_employee()
        self.attendance = self.create_attendance(employee)

    def test_concurrent_replacements_leave_one_complete_synchronized_set(self):
        barrier = Barrier(2)

        def worker(minutes):
            close_old_connections()
            actor = User.objects.get(pk=self.user.pk)
            attendance = EmployeeAttendance.objects.get(pk=self.attendance.pk)
            barrier.wait()
            replace_attendance_overtime(
                attendance=attendance,
                duration_entries=[{'work_date': attendance.date, 'gross_minutes': minutes}],
                source='MANUAL',
                actor=actor,
            )
            close_old_connections()

        with ThreadPoolExecutor(max_workers=2) as executor:
            futures = [executor.submit(worker, minutes) for minutes in (30, 45)]
            for future in futures:
                future.result()

        self.attendance.refresh_from_db()
        details = list(self.attendance.overtime_details.values_list('eligible_minutes', flat=True))
        self.assertIn(details, ([30], [45]))
        self.assertEqual(self.attendance.ot_min, sum(details))
