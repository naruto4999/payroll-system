# Generated by Django 5.0 on 2024-05-20 06:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0046_remove_employeeleaveopening_unique_year_per_employee_per_company_per_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeeleaveopening',
            name='leave_count',
            field=models.SmallIntegerField(),
        ),
    ]
