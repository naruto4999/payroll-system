# Generated by Django 4.1.5 on 2023-06-03 00:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_remove_leavegrade_unique_leave_grade_name_per_user'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='leavegrade',
            constraint=models.UniqueConstraint(fields=('user', 'company', 'name'), name='unique_leave_grade_name_per_user'),
        ),
    ]
