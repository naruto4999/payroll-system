# Generated by Django 4.1.5 on 2023-09-19 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0105_alter_employeemonthlyattendancedetails_user_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='employeemonthlyattendancedetails',
            name='net_ot_minutes_monthly',
            field=models.PositiveIntegerField(default=0),
        ),
    ]