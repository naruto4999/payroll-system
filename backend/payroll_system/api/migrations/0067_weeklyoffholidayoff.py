# Generated by Django 4.1.5 on 2023-07-30 01:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0066_alter_employeesalaryearning_from_date_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='WeeklyOffHolidayOff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('min_days_for_weekly_off', models.PositiveSmallIntegerField(default=0)),
                ('min_days_for_holiday_off', models.PositiveSmallIntegerField(default=0)),
                ('company', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='weekly_off_holiday_off_entry', to='api.company')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='weekly_off_holiday_off_entries', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]