# Generated by Django 4.1.5 on 2023-11-16 12:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeemonthlyattendancedetails',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='all_employees_monthly_attendance_details', to='api.company'),
        ),
        migrations.AlterField(
            model_name='employeemonthlyattendancedetails',
            name='employee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='monthly_attendance_details', to='api.employeepersonaldetail'),
        ),
    ]