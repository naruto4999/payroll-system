from datetime import date

from django.conf import settings
from django.db import connection
from django.db.migrations.executor import MigrationExecutor
from django.test import TransactionTestCase


class PhaseTwoMigrationTests(TransactionTestCase):
    migrate_from = ('api', '0049_extrafeaturesconfig')
    migrate_to = ('api', '0060_backfill_legacy_attendance_overtime_details')
    def setUp(self):
        super().setUp()
        executor = MigrationExecutor(connection)
        executor.migrate([self.migrate_from])
        old_apps = executor.loader.project_state([self.migrate_from]).apps
        self.fixture_ids = self.create_old_state(old_apps)
        executor = MigrationExecutor(connection)
        executor.migrate([self.migrate_to])
        self.apps = executor.loader.project_state([self.migrate_to]).apps

    def tearDown(self):
        executor = MigrationExecutor(connection)
        executor.migrate(executor.loader.graph.leaf_nodes())
        super().tearDown()

    def create_old_state(self, apps):
        User = apps.get_model('api', 'User')
        Company = apps.get_model('api', 'Company')
        CompanyDetails = apps.get_model('api', 'CompanyDetails')
        Employee = apps.get_model('api', 'EmployeePersonalDetail')
        Attendance = apps.get_model('api', 'EmployeeAttendance')
        LeaveGrade = apps.get_model('api', 'LeaveGrade')
        SalaryDetail = apps.get_model('api', 'EmployeeSalaryDetail')
        SalaryPrepared = apps.get_model('api', 'EmployeeSalaryPrepared')

        user = User.objects.create(
            username='migration-owner',
            email='migration@example.com',
            phone_no=9888888888,
            password='unused',
        )
        first = Company.objects.create(user=user, name='Existing details')
        second = Company.objects.create(user=user, name='Missing details')
        CompanyDetails.objects.create(user=user, company=first, address='Preserve me')

        mappings = {
            ('no_overtime', None): 'NO_OVERTIME',
            ('all_days', 'S'): 'ALL_DAYS_SINGLE',
            ('all_days', 'D'): 'ALL_DAYS_DOUBLE',
            ('holiday_weekly_off', 'S'): 'WO_HD_SINGLE',
            ('holiday_weekly_off', 'D'): 'WO_HD_DOUBLE',
        }
        salary_detail_ids = {}
        prepared_id = None
        attendance_id = None
        present = LeaveGrade.objects.create(
            user=user,
            company=first,
            name='P',
            paid=True,
            mandatory_leave=True,
        )
        for index, ((overtime_type, overtime_rate), code) in enumerate(mappings.items(), start=1):
            employee = Employee.objects.create(
                user=user,
                company=first,
                name=f'Employee {index}',
                paycode=f'M{index}',
                attendance_card_no=index,
            )
            detail = SalaryDetail.objects.create(
                user=user,
                company=first,
                employee=employee,
                overtime_type=overtime_type,
                overtime_rate=overtime_rate,
            )
            salary_detail_ids[detail.pk] = code
            if prepared_id is None:
                prepared_id = SalaryPrepared.objects.create(
                    user=user,
                    company=first,
                    employee=employee,
                    date=date(2024, 1, 1),
                    net_ot_minutes_monthly=90,
                    net_ot_amount_monthly=123,
                ).pk
                attendance_id = Attendance.objects.create(
                    user=user,
                    company=first,
                    employee=employee,
                    first_half=present,
                    second_half=present,
                    date=date(2024, 1, 2),
                    ot_min=75,
                    pay_multiplier=1,
                ).pk
        return {
            'company_ids': (first.pk, second.pk),
            'salary_detail_ids': salary_detail_ids,
            'prepared_id': prepared_id,
            'attendance_id': attendance_id,
        }

    def test_migration_preserves_legacy_mapping_and_aggregates_and_initializes_phase_two_fields(self):
        CompanyDetails = self.apps.get_model('api', 'CompanyDetails')
        OvertimePolicy = self.apps.get_model('api', 'OvertimePolicy')
        SalaryDetail = self.apps.get_model('api', 'EmployeeSalaryDetail')
        SalaryPrepared = self.apps.get_model('api', 'EmployeeSalaryPrepared')
        Attendance = self.apps.get_model('api', 'EmployeeAttendance')
        AttendanceOvertimeDetail = self.apps.get_model('api', 'EmployeeAttendanceOvertimeDetail')

        details = CompanyDetails.objects.filter(company_id__in=self.fixture_ids['company_ids'])
        self.assertEqual(details.count(), 2)
        self.assertEqual(set(details.values_list('payroll_timezone', flat=True)), {settings.PAYROLL_DEFAULT_TIMEZONE})
        self.assertEqual(details.get(company_id=self.fixture_ids['company_ids'][0]).address, 'Preserve me')

        for salary_detail_id, expected_code in self.fixture_ids['salary_detail_ids'].items():
            self.assertEqual(SalaryDetail.objects.get(pk=salary_detail_id).overtime_policy.code, expected_code)
        for company_id in self.fixture_ids['company_ids']:
            policies = OvertimePolicy.objects.filter(company_id=company_id)
            self.assertEqual(policies.count(), 7)
            self.assertFalse(policies.exclude(rounding_increment_minutes=30, round_up_from_minutes=16).exists())

        salary = SalaryPrepared.objects.get(pk=self.fixture_ids['prepared_id'])
        self.assertEqual((salary.net_ot_minutes_monthly, salary.net_ot_amount_monthly), (90, 123))
        self.assertIsNone(salary.ot_rounding_increment_minutes)
        self.assertIsNone(salary.ot_round_up_from_minutes)
        attendance = Attendance.objects.get(id=self.fixture_ids['attendance_id'], date=date(2024, 1, 2))
        self.assertEqual(attendance.ot_min, 75)
        detail = AttendanceOvertimeDetail.objects.get(
            employee_id=attendance.employee_id,
            attendance_date=attendance.date,
            user_id=attendance.user_id,
        )
        self.assertEqual(detail.source, 'LEGACY_BACKFILL')
        self.assertEqual(detail.day_type, 'REGULAR')
        self.assertIsNone(detail.start_datetime)
        self.assertIsNone(detail.end_datetime)
        self.assertEqual((detail.gross_minutes, detail.excluded_minutes, detail.eligible_minutes), (75, 0, 75))
