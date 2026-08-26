import json

from django.core.management.base import BaseCommand
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Count, F, IntegerField, OuterRef, Q, Subquery, Sum, Value
from django.db.models.functions import Coalesce

from api.models import (
    Company,
    EmployeeAttendance,
    EmployeeAttendanceOvertimeDetail,
    EmployeeSalaryPrepared,
    OvertimePolicy,
)


class Command(BaseCommand):
    help = "Report overtime policy, attendance detail, and prepared salary integrity issues without modifying data."

    def add_arguments(self, parser):
        parser.add_argument(
            "--format",
            choices=("text", "json"),
            default="text",
            help="Output format (default: text).",
        )

    def handle(self, *args, **options):
        report = self.build_report()
        if options["format"] == "json":
            self.stdout.write(json.dumps(report, cls=DjangoJSONEncoder, sort_keys=True))
            return

        for section, result in report.items():
            self.stdout.write(f"{section}: {result['count']}")
            for record in result["records"]:
                values = " ".join(f"{key}={value}" for key, value in record.items())
                self.stdout.write(f"  {values}")

    @staticmethod
    def build_report():
        active_default_count = Count(
            "overtime_policies",
            filter=Q(overtime_policies__is_default=True, overtime_policies__is_active=True),
        )
        companies = list(
            Company.objects.annotate(active_default_count=active_default_count)
            .exclude(active_default_count=1)
            .order_by("id")
            .values("id", "user_id", "name", "active_default_count")
        )

        selected_policies = OvertimePolicy.objects.filter(earnings_basis=OvertimePolicy.EARNINGS_BASIS_SELECTED)
        malformed_policies = []
        for policy in selected_policies.prefetch_related("selected_earning_heads__earnings_head").order_by("id"):
            selected_heads = list(policy.selected_earning_heads.all())
            reasons = []
            if not selected_heads:
                reasons.append("EMPTY_SELECTED_HEADS")
            if any(item.earnings_head.company_id != policy.company_id for item in selected_heads):
                reasons.append("CROSS_COMPANY_SELECTED_HEAD")
            if reasons:
                malformed_policies.append({
                    "id": policy.id,
                    "company_id": policy.company_id,
                    "code": policy.code,
                    "reason_codes": reasons,
                })

        attendance_with_totals = EmployeeAttendance.objects.annotate(
            detail_count=Count("overtime_details"),
            detail_total=Coalesce(Sum("overtime_details__eligible_minutes"), Value(0)),
        )
        missing_details = list(
            attendance_with_totals.filter(ot_min__gt=0, detail_count=0)
            .order_by("id")
            .values("id", "user_id", "company_id", "employee_id", "date", "ot_min")
        )
        detail_mismatches = list(
            attendance_with_totals.filter(detail_count__gt=0)
            .exclude(ot_min=F("detail_total"))
            .order_by("id")
            .values("id", "user_id", "company_id", "employee_id", "date", "ot_min", "detail_total")
        )

        valid_exclusion_reasons = dict(EmployeeAttendanceOvertimeDetail.EXCLUSION_REASON_CHOICES)
        exclusion_state_mismatches = []
        exclusion_details = EmployeeAttendanceOvertimeDetail.objects.filter(
            Q(excluded_minutes=0) & (~Q(exclusion_reason=EmployeeAttendanceOvertimeDetail.EXCLUSION_NONE) | ~Q(exclusion_note=''))
            | Q(excluded_minutes__gt=0, exclusion_reason=EmployeeAttendanceOvertimeDetail.EXCLUSION_NONE)
            | Q(
                excluded_minutes__gt=0,
                exclusion_reason__in=(
                    EmployeeAttendanceOvertimeDetail.EXCLUSION_MANUAL_ADJUSTMENT,
                    EmployeeAttendanceOvertimeDetail.EXCLUSION_OTHER,
                ),
            )
            | ~Q(exclusion_reason__in=valid_exclusion_reasons)
        ).order_by('id')
        for detail in exclusion_details:
            reasons = []
            if detail.exclusion_reason not in valid_exclusion_reasons:
                reasons.append('INVALID_EXCLUSION_REASON')
            if detail.excluded_minutes == 0:
                if detail.exclusion_reason != EmployeeAttendanceOvertimeDetail.EXCLUSION_NONE:
                    reasons.append('ZERO_EXCLUSION_WITH_REASON')
                if detail.exclusion_note:
                    reasons.append('ZERO_EXCLUSION_WITH_NOTE')
            elif detail.exclusion_reason == EmployeeAttendanceOvertimeDetail.EXCLUSION_NONE:
                reasons.append('POSITIVE_EXCLUSION_WITH_NONE_REASON')
            if (
                detail.exclusion_reason in (
                    EmployeeAttendanceOvertimeDetail.EXCLUSION_MANUAL_ADJUSTMENT,
                    EmployeeAttendanceOvertimeDetail.EXCLUSION_OTHER,
                )
                and not detail.exclusion_note.strip()
            ):
                reasons.append('REQUIRED_NOTE_BLANK')
            exclusion_state_mismatches.append({
                'id': detail.id,
                'attendance_id': detail.attendance.id,
                'excluded_minutes': detail.excluded_minutes,
                'exclusion_reason': detail.exclusion_reason,
                'exclusion_note': detail.exclusion_note,
                'reason_codes': reasons,
            })
        legacy_unspecified = list(
            EmployeeAttendanceOvertimeDetail.objects.filter(
                exclusion_reason=EmployeeAttendanceOvertimeDetail.EXCLUSION_LEGACY_UNSPECIFIED,
            ).order_by('id').values(
                'id',
                'employee_id',
                'attendance_date',
                'user_id',
                'company_id',
                'excluded_minutes',
                'exclusion_note',
            )
        )

        salary_totals = (
            EmployeeSalaryPrepared.objects.filter(pk=OuterRef("pk"))
            .values("pk")
            .annotate(
                minute_total=Sum("overtime_breakdown__net_minutes"),
                amount_total=Sum("overtime_breakdown__amount"),
            )
        )
        salaries_with_totals = EmployeeSalaryPrepared.objects.annotate(
            breakdown_count=Count("overtime_breakdown"),
            breakdown_minute_total=Coalesce(
                Subquery(salary_totals.values("minute_total")[:1], output_field=IntegerField()),
                Value(0),
            ),
            breakdown_amount_total=Coalesce(
                Subquery(salary_totals.values("amount_total")[:1], output_field=IntegerField()),
                Value(0),
            ),
        )
        missing_breakdowns = list(
            salaries_with_totals.filter(
                Q(net_ot_minutes_monthly__gt=0) | Q(net_ot_amount_monthly__gt=0),
                breakdown_count=0,
            )
            .order_by("id")
            .values(
                "id",
                "user_id",
                "company_id",
                "employee_id",
                "date",
                "net_ot_minutes_monthly",
                "net_ot_amount_monthly",
            )
        )
        breakdown_mismatches = list(
            salaries_with_totals.filter(breakdown_count__gt=0)
            .filter(
                ~Q(net_ot_minutes_monthly=F("breakdown_minute_total"))
                | ~Q(net_ot_amount_monthly=F("breakdown_amount_total"))
            )
            .order_by("id")
            .values(
                "id",
                "user_id",
                "company_id",
                "employee_id",
                "date",
                "net_ot_minutes_monthly",
                "breakdown_minute_total",
                "net_ot_amount_monthly",
                "breakdown_amount_total",
            )
        )

        return {
            "companies_without_one_active_default": Command.section(companies),
            "malformed_selected_heads_policies": Command.section(malformed_policies),
            "attendance_positive_ot_without_details": Command.section(missing_details),
            "attendance_detail_total_mismatches": Command.section(detail_mismatches),
            "attendance_detail_exclusion_state_mismatches": Command.section(exclusion_state_mismatches),
            "attendance_detail_legacy_unspecified_exclusions": Command.section(legacy_unspecified),
            "prepared_salary_positive_ot_without_breakdown": Command.section(missing_breakdowns),
            "prepared_salary_breakdown_mismatches": Command.section(breakdown_mismatches),
        }

    @staticmethod
    def section(records):
        return {"count": len(records), "records": records}
