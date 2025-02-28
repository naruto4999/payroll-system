# Generated by Django 5.0 on 2025-01-18 22:40

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0048_attendancemachineconfig'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExtraFeaturesConfig',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enable_calculate_ot_attendance_using_earned_salary', models.BooleanField(default=False)),
                ('company', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='extra_features_configuration', to='api.company')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='extra_features_configuration', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
