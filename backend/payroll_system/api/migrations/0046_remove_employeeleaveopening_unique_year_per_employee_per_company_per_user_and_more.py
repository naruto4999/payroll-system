# Generated by Django 5.0 on 2024-05-02 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0045_alter_employeeleaveopening_leave_count'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='employeeleaveopening',
            name='unique_year_per_employee_per_company_per_user',
        ),
        migrations.AddConstraint(
            model_name='employeeleaveopening',
            constraint=models.UniqueConstraint(fields=('employee', 'year', 'user', 'leave'), name='unique_leave_per_year_per_employee_per_company_per_user'),
        ),
    ]
