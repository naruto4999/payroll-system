import json
from io import StringIO

from django.core.management import call_command
from django.test import TestCase

from api.models import EmployeeAttendance, EmployeeAttendanceOvertimeDetail, EmployeeSalaryPrepared, OvertimePolicy
from api.tests.base import AttendanceTestDataMixin


class OvertimeAuditCommandTests(AttendanceTestDataMixin, TestCase):
    def run_audit(self):
        output = StringIO()
        call_command("audit_overtime_integrity", format="json", stdout=output)
        return json.loads(output.getvalue())

    def test_reports_stable_identifiers_and_reconciliation_issues_without_writes(self):
        employee = self.create_employee()
        missing_detail = self.create_attendance(employee, ot_min=30)
        mismatched_detail = self.create_attendance(employee, work_date=missing_detail.date.replace(day=3), ot_min=60)
        self.create_overtime_detail(mismatched_detail, minutes=30)

        legacy_salary = self.create_prepared_salary(employee, net_minutes=30, amount=50)
        mismatched_salary = self.create_prepared_salary(
            employee,
            period=legacy_salary.date.replace(month=2),
            net_minutes=60,
            amount=100,
        )
        self.create_prepared_overtime_detail(mismatched_salary, net_minutes=30, amount=50)

        empty_selected = self.create_overtime_policy(
            earnings_basis=OvertimePolicy.EARNINGS_BASIS_SELECTED,
        )
        before_counts = (
            OvertimePolicy.objects.count(),
            EmployeeAttendance.objects.count(),
            EmployeeSalaryPrepared.objects.count(),
        )

        report = self.run_audit()

        self.assertEqual(report["attendance_positive_ot_without_details"]["records"][0]["id"], missing_detail.id)
        self.assertEqual(report["attendance_detail_total_mismatches"]["records"][0]["detail_total"], 30)
        self.assertEqual(report["prepared_salary_positive_ot_without_breakdown"]["records"][0]["id"], legacy_salary.id)
        self.assertEqual(report["prepared_salary_breakdown_mismatches"]["records"][0]["id"], mismatched_salary.id)
        self.assertEqual(report["malformed_selected_heads_policies"]["records"][0]["id"], empty_selected.id)
        self.assertEqual(
            before_counts,
            (
                OvertimePolicy.objects.count(),
                EmployeeAttendance.objects.count(),
                EmployeeSalaryPrepared.objects.count(),
            ),
        )

    def test_reports_company_with_no_active_default(self):
        OvertimePolicy.objects.filter(company=self.company, is_default=True).update(is_default=False)

        report = self.run_audit()

        record = report["companies_without_one_active_default"]["records"][0]
        self.assertEqual(record["id"], self.company.id)
        self.assertEqual(record["active_default_count"], 0)

    def test_reports_exclusion_mismatches_and_migrated_legacy_rows(self):
        employee = self.create_employee()
        attendance = self.create_attendance(employee)
        legacy = self.create_overtime_detail(
            attendance,
            excluded_minutes=5,
            exclusion_reason='MEAL_BREAK',
        )
        EmployeeAttendanceOvertimeDetail.objects.filter(pk=legacy.pk).update(
            exclusion_reason='LEGACY_UNSPECIFIED',
        )
        note_mismatch = self.create_overtime_detail(
            attendance,
            minutes=20,
            work_date=attendance.date,
        )
        EmployeeAttendanceOvertimeDetail.objects.filter(pk=note_mismatch.pk).update(
            exclusion_note='unexpected',
        )

        report = self.run_audit()

        self.assertEqual(
            report['attendance_detail_legacy_unspecified_exclusions']['records'][0]['id'],
            legacy.id,
        )
        mismatch = report['attendance_detail_exclusion_state_mismatches']['records'][0]
        self.assertEqual(mismatch['id'], note_mismatch.id)
        self.assertIn('ZERO_EXCLUSION_WITH_NOTE', mismatch['reason_codes'])
