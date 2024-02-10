# Generated by Django 5.0 on 2024-02-08 13:30

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0031_remove_holiday_unique_hodiday_name_per_user_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubUserOvertimeSettings',
            fields=[
                ('company', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='company_sub_user_settings', serialize=False, to='api.company')),
                ('date', models.DateField()),
                ('max_ot_hrs', models.PositiveSmallIntegerField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='all_companies_sub_user_settings', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]