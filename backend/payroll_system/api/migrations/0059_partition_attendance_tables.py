from datetime import date

from django.db import migrations
from django.db.migrations.exceptions import IrreversibleError


ATTENDANCE_COLUMNS = (
    'id',
    'user_id',
    'employee_id',
    'company_id',
    'machine_in',
    'machine_out',
    'manual_in',
    'manual_out',
    'first_half_id',
    'second_half_id',
    'date',
    'ot_min',
    'late_min',
    'pay_multiplier',
    'manual_mode',
)

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

ATTENDANCE_HISTORY_CUTOFF = date(2009, 1, 1)


def month_starts(start, end):
    current = date(start.year, start.month, 1)
    final = date(end.year, end.month, 1)
    while current <= final:
        yield current
        if current.month == 12:
            current = date(current.year + 1, 1, 1)
        else:
            current = date(current.year, current.month + 1, 1)


def add_month(value):
    if value.month == 12:
        return date(value.year + 1, 1, 1)
    return date(value.year, value.month + 1, 1)


def add_months(value, months):
    result = value
    for _ in range(months):
        result = add_month(result)
    return result


def get_partition_start(cursor, old_table, partition_column):
    cursor.execute(f'SELECT MIN({partition_column}) FROM {old_table};')
    minimum = cursor.fetchone()[0]
    return minimum or date.today()


def create_monthly_partitions(cursor, parent_table, partition_column, old_table):
    start = get_partition_start(cursor, old_table, partition_column)
    end = add_months(date.today(), 24)
    for lower in month_starts(start, end):
        upper = add_month(lower)
        partition_name = f'{parent_table}_{lower:%Y_%m}'
        cursor.execute(
            f'''
            CREATE TABLE {partition_name}
            PARTITION OF {parent_table}
            FOR VALUES FROM (%s) TO (%s);
            ''',
            [lower, upper],
        )
    cursor.execute(
        f'''
        CREATE TABLE {parent_table}_default
        PARTITION OF {parent_table} DEFAULT;
        '''
    )


def rename_existing_indexes(cursor, table_name):
    cursor.execute(
        """
        SELECT indexname
        FROM pg_indexes
        WHERE schemaname = current_schema()
        AND tablename = %s;
        """,
        [table_name],
    )
    for (index_name,) in cursor.fetchall():
        new_name = f'{index_name}_old'
        if len(new_name) > 63:
            new_name = f'{index_name[:59]}_old'
        cursor.execute(f'ALTER INDEX IF EXISTS {index_name} RENAME TO {new_name};')


def replace_identity_sequence(cursor, table_name):
    old_sequence_name = f'{table_name}_old_id_seq'
    sequence_name = f'{table_name}_id_seq'
    cursor.execute(f'ALTER SEQUENCE IF EXISTS {sequence_name} RENAME TO {old_sequence_name};')
    cursor.execute(f'CREATE SEQUENCE {sequence_name} AS bigint;')


def validate_no_null_partition_keys(cursor):
    cursor.execute('SELECT COUNT(*) FROM api_employeeattendance WHERE date IS NULL;')
    attendance_null_count = cursor.fetchone()[0]
    cursor.execute(
        'SELECT COUNT(*) FROM api_employeeattendanceovertimedetail WHERE attendance_date IS NULL;'
    )
    detail_null_count = cursor.fetchone()[0]
    if attendance_null_count or detail_null_count:
        raise RuntimeError(
            'Attendance partition keys must be non-null before partitioning: '
            f'api_employeeattendance.date={attendance_null_count}, '
            f'api_employeeattendanceovertimedetail.attendance_date={detail_null_count}'
        )


def delete_invalid_pre_2009_attendance_history(cursor):
    lower_bound = date(1986, 1, 1)
    cursor.execute(
        """
        DELETE FROM api_employeeattendanceovertimedetail
        WHERE attendance_date >= %s
        AND attendance_date < %s;
        """,
        [lower_bound, ATTENDANCE_HISTORY_CUTOFF],
    )
    cursor.execute(
        """
        DELETE FROM api_employeeattendance
        WHERE date >= %s
        AND date < %s;
        """,
        [lower_bound, ATTENDANCE_HISTORY_CUTOFF],
    )
    cursor.execute(
        """
        DELETE FROM api_employeegenerativeleaverecord
        WHERE date >= %s
        AND date < %s;
        """,
        [lower_bound, ATTENDANCE_HISTORY_CUTOFF],
    )
    cursor.execute(
        """
        DELETE FROM api_employeemonthlyattendancedetails
        WHERE date >= %s
        AND date < %s;
        """,
        [lower_bound, ATTENDANCE_HISTORY_CUTOFF],
    )


def validate_attendance_history_cutoff(cursor):
    cursor.execute('SELECT MIN(date) FROM api_employeeattendance;')
    minimum = cursor.fetchone()[0]
    if minimum is not None and minimum < ATTENDANCE_HISTORY_CUTOFF:
        raise RuntimeError(
            'Attendance rows before 2009-01-01 remain after pre-partition cleanup: '
            f'min_date={minimum}'
        )


def validate_row_count(cursor, table_name, old_table_name):
    cursor.execute(f'SELECT COUNT(*) FROM {table_name};')
    new_count = cursor.fetchone()[0]
    cursor.execute(f'SELECT COUNT(*) FROM {old_table_name};')
    old_count = cursor.fetchone()[0]
    if new_count != old_count:
        raise RuntimeError(
            f'Partitioning row count mismatch for {table_name}: '
            f'new={new_count}, old={old_count}'
        )


def sync_sequence(cursor, table_name):
    cursor.execute(
        """
        SELECT setval(
            pg_get_serial_sequence(%s, 'id'),
            COALESCE((SELECT MAX(id) FROM %s), 1),
            true
        );
        """ % ("'%s'" % table_name, table_name)
    )
    cursor.execute(
        f"ALTER SEQUENCE {table_name}_id_seq OWNED BY {table_name}.id;"
    )


def create_employee_attendance(cursor):
    cursor.execute(
        """
        CREATE TABLE api_employeeattendance (
            id bigint NOT NULL DEFAULT nextval('api_employeeattendance_id_seq'::regclass),
            user_id bigint NOT NULL,
            employee_id bigint NOT NULL,
            company_id bigint NOT NULL,
            machine_in time without time zone,
            machine_out time without time zone,
            manual_in time without time zone,
            manual_out time without time zone,
            first_half_id bigint NOT NULL,
            second_half_id bigint NOT NULL,
            date date NOT NULL,
            ot_min smallint,
            late_min smallint,
            pay_multiplier numeric(3, 1) NOT NULL,
            manual_mode boolean NOT NULL,
            CONSTRAINT api_employeeattendance_pkey PRIMARY KEY (id, date),
            CONSTRAINT unique_employee_attendance_date_wise UNIQUE (employee_id, date, user_id),
            CONSTRAINT api_employeeattendance_ot_min_nonnegative CHECK (ot_min >= 0),
            CONSTRAINT api_employeeattendance_late_min_nonnegative CHECK (late_min >= 0),
            CONSTRAINT api_employeeattendance_user_id_fk FOREIGN KEY (user_id)
                REFERENCES api_user(id) DEFERRABLE INITIALLY DEFERRED,
            CONSTRAINT api_employeeattendance_employee_id_fk FOREIGN KEY (employee_id)
                REFERENCES api_employeepersonaldetail(id) DEFERRABLE INITIALLY DEFERRED,
            CONSTRAINT api_employeeattendance_company_id_fk FOREIGN KEY (company_id)
                REFERENCES api_company(id) DEFERRABLE INITIALLY DEFERRED,
            CONSTRAINT api_employeeattendance_first_half_id_fk FOREIGN KEY (first_half_id)
                REFERENCES api_leavegrade(id) DEFERRABLE INITIALLY DEFERRED,
            CONSTRAINT api_employeeattendance_second_half_id_fk FOREIGN KEY (second_half_id)
                REFERENCES api_leavegrade(id) DEFERRABLE INITIALLY DEFERRED
        ) PARTITION BY RANGE (date);
        """
    )
    create_monthly_partitions(cursor, 'api_employeeattendance', 'date', 'api_employeeattendance_old')
    columns = ', '.join(ATTENDANCE_COLUMNS)
    cursor.execute(
        f'''
        INSERT INTO api_employeeattendance ({columns})
        SELECT {columns}
        FROM api_employeeattendance_old;
        '''
    )
    cursor.execute('SET CONSTRAINTS ALL IMMEDIATE;')
    cursor.execute('CREATE INDEX api_employeeattendance_employee_idx ON api_employeeattendance (employee_id);')
    cursor.execute('CREATE INDEX api_employeeattendance_date_idx ON api_employeeattendance (date);')
    cursor.execute('CREATE INDEX api_employeeattendance_company_idx ON api_employeeattendance (company_id);')
    cursor.execute('CREATE INDEX api_employeeattendance_user_idx ON api_employeeattendance (user_id);')
    sync_sequence(cursor, 'api_employeeattendance')


def create_overtime_detail(cursor):
    cursor.execute(
        """
        CREATE TABLE api_employeeattendanceovertimedetail (
            id bigint NOT NULL DEFAULT nextval('api_employeeattendanceovertimedetail_id_seq'::regclass),
            user_id bigint NOT NULL,
            company_id bigint NOT NULL,
            employee_id bigint NOT NULL,
            attendance_date date NOT NULL,
            work_date date NOT NULL,
            day_type varchar(20) NOT NULL,
            source varchar(20) NOT NULL,
            start_datetime timestamp with time zone,
            end_datetime timestamp with time zone,
            gross_minutes smallint NOT NULL,
            excluded_minutes smallint NOT NULL DEFAULT 0,
            eligible_minutes smallint NOT NULL,
            exclusion_reason varchar(24) NOT NULL DEFAULT 'NONE',
            exclusion_note varchar(255) NOT NULL DEFAULT '',
            created_at timestamp with time zone NOT NULL,
            updated_at timestamp with time zone NOT NULL,
            CONSTRAINT api_employeeattendanceovertimedetail_pkey PRIMARY KEY (id, attendance_date),
            CONSTRAINT api_employeeattendanceot_user_id_fk FOREIGN KEY (user_id)
                REFERENCES api_user(id) DEFERRABLE INITIALLY DEFERRED,
            CONSTRAINT api_employeeattendanceot_company_id_fk FOREIGN KEY (company_id)
                REFERENCES api_company(id) DEFERRABLE INITIALLY DEFERRED,
            CONSTRAINT api_employeeattendanceot_employee_id_fk FOREIGN KEY (employee_id)
                REFERENCES api_employeepersonaldetail(id) DEFERRABLE INITIALLY DEFERRED,
            CONSTRAINT attendance_ot_detail_attendance_composite_fk
                FOREIGN KEY (employee_id, attendance_date, user_id)
                REFERENCES api_employeeattendance (employee_id, date, user_id)
                ON DELETE CASCADE
                DEFERRABLE INITIALLY DEFERRED,
            CONSTRAINT attendance_ot_detail_datetimes_both_set_or_null
                CHECK (((start_datetime IS NULL) AND (end_datetime IS NULL)) OR ((start_datetime IS NOT NULL) AND (end_datetime IS NOT NULL))),
            CONSTRAINT attendance_ot_detail_gross_positive CHECK (gross_minutes > 0),
            CONSTRAINT attendance_ot_detail_excluded_nonnegative CHECK (excluded_minutes >= 0),
            CONSTRAINT attendance_ot_detail_excluded_lte_gross CHECK (excluded_minutes <= gross_minutes),
            CONSTRAINT attendance_ot_detail_eligible_positive CHECK (eligible_minutes > 0),
            CONSTRAINT attendance_ot_detail_start_before_end CHECK ((start_datetime IS NULL) OR (start_datetime < end_datetime)),
            CONSTRAINT attendance_ot_detail_eligible_arithmetic CHECK (eligible_minutes = (gross_minutes - excluded_minutes)),
            CONSTRAINT attendance_ot_detail_exclusion_reason_matches_minutes
                CHECK (((excluded_minutes = 0) AND ((exclusion_reason)::text = 'NONE'::text)) OR ((excluded_minutes > 0) AND ((exclusion_reason)::text <> 'NONE'::text)))
        ) PARTITION BY RANGE (attendance_date);
        """
    )
    create_monthly_partitions(
        cursor,
        'api_employeeattendanceovertimedetail',
        'attendance_date',
        'api_employeeattendanceovertimedetail_old',
    )
    columns = ', '.join(OVERTIME_DETAIL_COLUMNS)
    cursor.execute(
        f'''
        INSERT INTO api_employeeattendanceovertimedetail ({columns})
        SELECT {columns}
        FROM api_employeeattendanceovertimedetail_old;
        '''
    )
    cursor.execute('SET CONSTRAINTS ALL IMMEDIATE;')
    cursor.execute(
        """
        CREATE INDEX api_employeeattendanceot_user_company_employee_date_idx
        ON api_employeeattendanceovertimedetail (user_id, company_id, employee_id, attendance_date);
        """
    )
    cursor.execute(
        """
        CREATE INDEX api_employeeattendanceot_attendance_work_idx
        ON api_employeeattendanceovertimedetail (attendance_date, work_date);
        """
    )
    cursor.execute(
        """
        CREATE INDEX api_employeeattendanceot_employee_attendance_user_work_day_idx
        ON api_employeeattendanceovertimedetail (employee_id, attendance_date, user_id, work_date, day_type);
        """
    )
    cursor.execute('CREATE INDEX api_employeeattendanceot_user_idx ON api_employeeattendanceovertimedetail (user_id);')
    cursor.execute('CREATE INDEX api_employeeattendanceot_company_idx ON api_employeeattendanceovertimedetail (company_id);')
    cursor.execute('CREATE INDEX api_employeeattendanceot_employee_idx ON api_employeeattendanceovertimedetail (employee_id);')
    sync_sequence(cursor, 'api_employeeattendanceovertimedetail')


def partition_attendance_tables(apps, schema_editor):
    if schema_editor.connection.vendor != 'postgresql':
        return

    with schema_editor.connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT relkind
            FROM pg_class
            WHERE oid = 'api_employeeattendance'::regclass;
            """
        )
        if cursor.fetchone()[0] == 'p':
            return

        delete_invalid_pre_2009_attendance_history(cursor)
        validate_attendance_history_cutoff(cursor)
        validate_no_null_partition_keys(cursor)

        cursor.execute(
            """
            ALTER TABLE api_employeeattendanceovertimedetail
            DROP CONSTRAINT IF EXISTS attendance_ot_detail_attendance_composite_fk;
            """
        )
        cursor.execute('ALTER TABLE api_employeeattendance RENAME TO api_employeeattendance_old;')
        cursor.execute('ALTER TABLE api_employeeattendanceovertimedetail RENAME TO api_employeeattendanceovertimedetail_old;')
        replace_identity_sequence(cursor, 'api_employeeattendance')
        replace_identity_sequence(cursor, 'api_employeeattendanceovertimedetail')
        cursor.execute('ALTER TABLE api_employeeattendance_old DROP CONSTRAINT IF EXISTS api_employeeattendance_pkey;')
        cursor.execute('ALTER TABLE api_employeeattendance_old DROP CONSTRAINT IF EXISTS unique_employee_attendance_date_wise;')
        cursor.execute(
            'ALTER TABLE api_employeeattendanceovertimedetail_old '
            'DROP CONSTRAINT IF EXISTS api_employeeattendanceovertimedetail_pkey;'
        )
        rename_existing_indexes(cursor, 'api_employeeattendance_old')
        rename_existing_indexes(cursor, 'api_employeeattendanceovertimedetail_old')

        create_employee_attendance(cursor)
        create_overtime_detail(cursor)

        validate_row_count(cursor, 'api_employeeattendance', 'api_employeeattendance_old')
        validate_row_count(
            cursor,
            'api_employeeattendanceovertimedetail',
            'api_employeeattendanceovertimedetail_old',
        )


def reverse_partition_attendance_tables(apps, schema_editor):
    raise IrreversibleError(
        'Attendance partitioning rollback requires the manual incident procedure documented in attendance-partitioning-execution-plan.md.'
    )


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0058_attendance_composite_primary_keys'),
    ]

    operations = [
        migrations.RunPython(partition_attendance_tables, reverse_partition_attendance_tables),
    ]
