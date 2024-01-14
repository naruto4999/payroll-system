# Generated by Django 5.0 on 2024-01-12 10:43

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0019_bonuscalculation_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='BonusPercentage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bonus_percentage', models.DecimalField(decimal_places=2, default=8.33, max_digits=5, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('company', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='bonus_percentage', to='api.company')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='all_company_bonus_percentage', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
