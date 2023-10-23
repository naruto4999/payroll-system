# Generated by Django 4.1.5 on 2023-07-20 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0063_employeemonthlysalarychange_and_more'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='employeesalaryearning',
            name='unique_employee_earning_head',
        ),
        migrations.RemoveField(
            model_name='employeesalaryearning',
            name='year',
        ),
        migrations.AddField(
            model_name='employeesalaryearning',
            name='from_date',
            field=models.DateField(default='2023-07-01'),
        ),
        migrations.AddField(
            model_name='employeesalaryearning',
            name='to_date',
            field=models.DateField(default='9999-01-01'),
        ),
        migrations.AddConstraint(
            model_name='employeesalaryearning',
            constraint=models.UniqueConstraint(fields=('employee', 'earnings_head', 'from_date'), name='unique_employee_earnings_head_with_from_date'),
        ),
        migrations.AddConstraint(
            model_name='employeesalaryearning',
            constraint=models.UniqueConstraint(fields=('earnings_head', 'employee', 'to_date'), name='unique_employee_earnings_head_with_to_date'),
        ),
    ]