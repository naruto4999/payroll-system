# Generated by Django 4.1.5 on 2023-08-26 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0090_alter_shift_max_late_allowed_min'),
    ]

    operations = [
        migrations.AddField(
            model_name='employeeattendance',
            name='manual_mode',
            field=models.BooleanField(default=False),
        ),
    ]