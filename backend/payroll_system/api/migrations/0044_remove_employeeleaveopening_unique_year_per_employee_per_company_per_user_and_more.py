# Generated by Django 5.0 on 2024-04-16 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0043_alter_fullandfinal_employee_and_more'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='employeeleaveopening',
            name='unique_year_per_employee_per_company_per_user',
        ),
        migrations.AddConstraint(
            model_name='employeeleaveopening',
            constraint=models.UniqueConstraint(fields=('employee', 'year', 'user'), name='unique_year_per_employee_per_company_per_user'),
        ),
    ]
