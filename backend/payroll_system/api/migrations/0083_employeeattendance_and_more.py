# Generated by Django 4.1.5 on 2023-08-16 17:30

import api.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0082_delete_employeeattendance'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmployeeAttendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('machine_in', models.TimeField(blank=True, null=True)),
                ('machine_out', models.TimeField(blank=True, null=True)),
                ('manual_in', models.TimeField(blank=True, null=True)),
                ('manual_out', models.TimeField(blank=True, null=True)),
                ('date', models.DateField()),
                ('pay_multiplier', api.models.LimitedFloatField(decimal_places=1, max_digits=3, validators=[api.models.validate_pay_multiplier_allowed_values])),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='all_company_employees_attendance', to='api.company')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attendance', to='api.employeepersonaldetail')),
                ('first_half', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='employees_first_half_attendances_with_same_leave', to='api.leavegrade')),
                ('second_half', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='employees_second_half_attendances_with_same_leave', to='api.leavegrade')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='all_employees_attendance', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddConstraint(
            model_name='employeeattendance',
            constraint=models.UniqueConstraint(fields=('employee', 'date', 'company'), name='unique_employee_attendance_date_wise'),
        ),
    ]
