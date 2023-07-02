# Generated by Django 4.1.5 on 2023-06-03 00:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_leavegrade_mandatory_leave'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='leavegrade',
            constraint=models.UniqueConstraint(fields=('user', 'company', 'name'), name='unique_leave_grade_name_per_user'),
        ),
    ]