# Generated by Django 4.1.5 on 2023-08-07 14:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0076_alter_calculations_notice_pay_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmployeeShifts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_date', models.DateField()),
                ('to_date', models.DateField()),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='all_company_employees_shifts', to='api.company')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shifts', to='api.employeepersonaldetail')),
                ('shift', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employees_shifts', to='api.shift')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='all_employees_shifts', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddConstraint(
            model_name='employeeshifts',
            constraint=models.UniqueConstraint(fields=('employee', 'shift', 'from_date'), name='unique_employee_shift_from_date'),
        ),
        migrations.AddConstraint(
            model_name='employeeshifts',
            constraint=models.UniqueConstraint(fields=('shift', 'employee', 'to_date'), name='unique_employee_shift_to_date'),
        ),
    ]