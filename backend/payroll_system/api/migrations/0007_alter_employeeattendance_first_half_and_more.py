# Generated by Django 4.1.5 on 2023-12-11 16:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_alter_pfesisetup_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeeattendance',
            name='first_half',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='employees_first_half_attendances_with_same_leave', to='api.leavegrade'),
        ),
        migrations.AlterField(
            model_name='employeeattendance',
            name='second_half',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='employees_second_half_attendances_with_same_leave', to='api.leavegrade'),
        ),
    ]
