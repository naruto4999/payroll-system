from django.db import migrations


def backfill_legacy_attendance_overtime_details(apps, schema_editor):
    with schema_editor.connection.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO api_employeeattendanceovertimedetail (
                user_id,
                company_id,
                employee_id,
                attendance_date,
                work_date,
                day_type,
                source,
                start_datetime,
                end_datetime,
                gross_minutes,
                excluded_minutes,
                eligible_minutes,
                exclusion_reason,
                exclusion_note,
                created_at,
                updated_at
            )
            SELECT
                attendance.user_id,
                attendance.company_id,
                attendance.employee_id,
                attendance.date,
                attendance.date,
                CASE
                    WHEN first_half.name IN ('HD', 'HD*') AND second_half.name IN ('HD', 'HD*') THEN 'HOLIDAY'
                    WHEN first_half.name IN ('WO', 'WO*') AND second_half.name IN ('WO', 'WO*') THEN 'WEEKLY_OFF'
                    ELSE 'REGULAR'
                END,
                'LEGACY_BACKFILL',
                NULL,
                NULL,
                attendance.ot_min,
                0,
                attendance.ot_min,
                'NONE',
                '',
                CURRENT_TIMESTAMP,
                CURRENT_TIMESTAMP
            FROM api_employeeattendance attendance
            INNER JOIN api_leavegrade first_half ON first_half.id = attendance.first_half_id
            INNER JOIN api_leavegrade second_half ON second_half.id = attendance.second_half_id
            WHERE attendance.ot_min IS NOT NULL
            AND attendance.ot_min > 0
            AND NOT EXISTS (
                SELECT 1
                FROM api_employeeattendanceovertimedetail detail
                WHERE detail.employee_id = attendance.employee_id
                AND detail.attendance_date = attendance.date
                AND detail.user_id = attendance.user_id
            );
            """
        )


def noop_reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0059_partition_attendance_tables'),
    ]

    operations = [
        migrations.RunPython(backfill_legacy_attendance_overtime_details, noop_reverse),
    ]
