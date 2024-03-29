# Generated by Django 5.0 on 2024-02-10 13:53

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0033_delete_subuserovertimesettings'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubUserOvertimeSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('max_ot_hrs', models.PositiveSmallIntegerField()),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='company_sub_user_settings', to='api.company')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='all_companies_sub_user_settings', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
