# Generated by Django 4.1.5 on 2023-08-22 18:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0087_rename_late_hrs_min_employeeattendance_late_min_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shift',
            old_name='next_shift_dealy',
            new_name='next_shift_delay',
        ),
    ]
