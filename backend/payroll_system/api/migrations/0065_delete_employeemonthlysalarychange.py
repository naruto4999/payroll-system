# Generated by Django 4.1.5 on 2023-07-20 13:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0064_remove_employeesalaryearning_unique_employee_earning_head_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='EmployeeMonthlySalaryChange',
        ),
    ]