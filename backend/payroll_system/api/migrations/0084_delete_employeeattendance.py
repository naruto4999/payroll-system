# Generated by Django 4.1.5 on 2023-08-16 17:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0083_employeeattendance_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='EmployeeAttendance',
        ),
    ]
