from django.db import migrations, models
from django.db.models.expressions import RawSQL


def apply_composite_primary_keys(apps, schema_editor):
    if schema_editor.connection.vendor != 'postgresql':
        return

    with schema_editor.connection.cursor() as cursor:
        cursor.execute(
            """
            ALTER TABLE api_employeeattendance
            DROP CONSTRAINT IF EXISTS api_employeeattendance_pkey;
            """
        )
        cursor.execute(
            """
            ALTER TABLE api_employeeattendance
            ADD CONSTRAINT api_employeeattendance_pkey PRIMARY KEY (id, date);
            """
        )
        cursor.execute(
            """
            ALTER TABLE api_employeeattendanceovertimedetail
            DROP CONSTRAINT IF EXISTS api_employeeattendanceovertimedetail_pkey;
            """
        )
        cursor.execute(
            """
            ALTER TABLE api_employeeattendanceovertimedetail
            ADD CONSTRAINT api_employeeattendanceovertimedetail_pkey PRIMARY KEY (id, attendance_date);
            """
        )


def reverse_composite_primary_keys(apps, schema_editor):
    if schema_editor.connection.vendor != 'postgresql':
        return

    with schema_editor.connection.cursor() as cursor:
        cursor.execute(
            """
            ALTER TABLE api_employeeattendanceovertimedetail
            DROP CONSTRAINT IF EXISTS api_employeeattendanceovertimedetail_pkey;
            """
        )
        cursor.execute(
            """
            ALTER TABLE api_employeeattendanceovertimedetail
            ADD CONSTRAINT api_employeeattendanceovertimedetail_pkey PRIMARY KEY (id);
            """
        )
        cursor.execute(
            """
            ALTER TABLE api_employeeattendance
            DROP CONSTRAINT IF EXISTS api_employeeattendance_pkey;
            """
        )
        cursor.execute(
            """
            ALTER TABLE api_employeeattendance
            ADD CONSTRAINT api_employeeattendance_pkey PRIMARY KEY (id);
            """
        )


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0057_alter_employeesalarypreparedovertimedetail_amount'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[
                migrations.RunPython(apply_composite_primary_keys, reverse_composite_primary_keys),
            ],
            state_operations=[
                migrations.AlterField(
                    model_name='employeeattendance',
                    name='id',
                    field=models.BigIntegerField(db_default=RawSQL("nextval('api_employeeattendance_id_seq'::regclass)", ()), editable=False),
                ),
                migrations.AddField(
                    model_name='employeeattendance',
                    name='pk',
                    field=models.CompositePrimaryKey('id', 'date', blank=True, editable=False, primary_key=True, serialize=False),
                ),
                migrations.AlterField(
                    model_name='employeeattendanceovertimedetail',
                    name='id',
                    field=models.BigIntegerField(db_default=RawSQL("nextval('api_employeeattendanceovertimedetail_id_seq'::regclass)", ()), editable=False),
                ),
                migrations.AddField(
                    model_name='employeeattendanceovertimedetail',
                    name='pk',
                    field=models.CompositePrimaryKey('id', 'attendance_date', blank=True, editable=False, primary_key=True, serialize=False),
                ),
            ],
        ),
    ]
