from datetime import date

from django.db import migrations
from django.db.migrations.exceptions import IrreversibleError


ATTENDANCE_TABLE = 'api_employeeattendance'
OVERTIME_DETAIL_TABLE = 'api_employeeattendanceovertimedetail'
OVERTIME_DETAIL_DEFAULT_TABLE = f'{OVERTIME_DETAIL_TABLE}_default'

OVERTIME_DETAIL_COLUMNS = (
    'id',
    'user_id',
    'company_id',
    'employee_id',
    'attendance_date',
    'work_date',
    'day_type',
    'source',
    'start_datetime',
    'end_datetime',
    'gross_minutes',
    'excluded_minutes',
    'eligible_minutes',
    'exclusion_reason',
    'exclusion_note',
    'created_at',
    'updated_at',
)


def add_month(value):
    if value.month == 12:
        return date(value.year + 1, 1, 1)
    return date(value.year, value.month + 1, 1)


def validate_partition_parent(cursor, table_name):
    cursor.execute(
        """
        SELECT pg_class.relkind
        FROM pg_class
        INNER JOIN pg_namespace ON pg_namespace.oid = pg_class.relnamespace
        WHERE pg_namespace.nspname = current_schema()
        AND pg_class.relname = %s;
        """,
        [table_name],
    )
    row = cursor.fetchone()
    if row is None or row[0] != 'p':
        raise RuntimeError(f'{table_name} must be a partitioned table before attendance cleanup.')


def validate_attached_partition(cursor, parent_table, partition_table):
    cursor.execute(
        """
        SELECT EXISTS (
            SELECT 1
            FROM pg_inherits
            INNER JOIN pg_class parent ON parent.oid = pg_inherits.inhparent
            INNER JOIN pg_class child ON child.oid = pg_inherits.inhrelid
            INNER JOIN pg_namespace namespace ON namespace.oid = parent.relnamespace
            WHERE namespace.nspname = current_schema()
            AND parent.relname = %s
            AND child.relname = %s
        );
        """,
        [parent_table, partition_table],
    )
    if not cursor.fetchone()[0]:
        raise RuntimeError(f'{partition_table} must be attached to {parent_table} before attendance cleanup.')


def repartition_legacy_overtime(cursor, schema_editor):
    quote_name = schema_editor.quote_name
    parent = quote_name(OVERTIME_DETAIL_TABLE)
    default_partition = quote_name(OVERTIME_DETAIL_DEFAULT_TABLE)

    cursor.execute(f'LOCK TABLE {parent} IN ACCESS EXCLUSIVE MODE;')
    cursor.execute(f'SELECT COUNT(*) FROM {parent};')
    original_parent_count = cursor.fetchone()[0]
    cursor.execute(f'SELECT COUNT(*) FROM {default_partition};')
    default_count = cursor.fetchone()[0]
    cursor.execute(
        f"""
        SELECT DISTINCT date_trunc('month', attendance_date)::date
        FROM {default_partition}
        ORDER BY 1;
        """
    )
    partition_months = [row[0] for row in cursor.fetchall()]

    cursor.execute(f'ALTER TABLE {parent} DETACH PARTITION {default_partition};')

    for lower in partition_months:
        upper = add_month(lower)
        partition_name = f'{OVERTIME_DETAIL_TABLE}_{lower:%Y_%m}'
        cursor.execute('SELECT to_regclass(%s);', [partition_name])
        if cursor.fetchone()[0] is not None:
            raise RuntimeError(
                f'Cannot create historical overtime partition {partition_name}: relation already exists.'
            )
        cursor.execute(
            f"""
            CREATE TABLE {quote_name(partition_name)}
            PARTITION OF {parent}
            FOR VALUES FROM (%s) TO (%s);
            """,
            [lower, upper],
        )

    columns = ', '.join(quote_name(column) for column in OVERTIME_DETAIL_COLUMNS)
    cursor.execute(
        f"""
        INSERT INTO {parent} ({columns})
        SELECT {columns}
        FROM {default_partition};
        """
    )
    if cursor.rowcount != default_count:
        raise RuntimeError(
            'Historical overtime repartition row count mismatch: '
            f'expected={default_count}, inserted={cursor.rowcount}'
        )

    cursor.execute(f'SELECT COUNT(*) FROM {parent};')
    repartitioned_parent_count = cursor.fetchone()[0]
    if repartitioned_parent_count != original_parent_count:
        raise RuntimeError(
            'Overtime detail row count changed during historical repartitioning: '
            f'before={original_parent_count}, after={repartitioned_parent_count}'
        )

    cursor.execute(f'TRUNCATE TABLE {default_partition};')
    cursor.execute(f'ALTER TABLE {parent} ATTACH PARTITION {default_partition} DEFAULT;')


def cleanup_attendance_partition_tables(apps, schema_editor):
    if schema_editor.connection.vendor != 'postgresql':
        return

    with schema_editor.connection.cursor() as cursor:
        validate_partition_parent(cursor, ATTENDANCE_TABLE)
        validate_partition_parent(cursor, OVERTIME_DETAIL_TABLE)
        validate_attached_partition(
            cursor,
            OVERTIME_DETAIL_TABLE,
            OVERTIME_DETAIL_DEFAULT_TABLE,
        )
        validate_attached_partition(
            cursor,
            ATTENDANCE_TABLE,
            f'{ATTENDANCE_TABLE}_default',
        )

        repartition_legacy_overtime(cursor, schema_editor)

        quote_name = schema_editor.quote_name
        cursor.execute(f'DROP TABLE IF EXISTS {quote_name(f"{OVERTIME_DETAIL_TABLE}_old")};')
        cursor.execute(f'DROP TABLE IF EXISTS {quote_name(f"{ATTENDANCE_TABLE}_old")};')
        cursor.execute(f'DROP SEQUENCE IF EXISTS {quote_name(f"{OVERTIME_DETAIL_TABLE}_old_id_seq")};')
        cursor.execute(f'DROP SEQUENCE IF EXISTS {quote_name(f"{ATTENDANCE_TABLE}_old_id_seq")};')


def reverse_cleanup(apps, schema_editor):
    raise IrreversibleError('Dropped attendance backup tables cannot be restored by a migration rollback.')


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0061_leavegrade_payable_earnings_heads'),
    ]

    operations = [
        migrations.RunPython(cleanup_attendance_partition_tables, reverse_cleanup),
    ]
