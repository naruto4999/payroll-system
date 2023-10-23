# Generated by Django 4.1.5 on 2023-08-02 02:19

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0068_remove_weeklyoffholidayoff_id_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PfEsiSetup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ac1_epf_employee_percentage', models.DecimalField(decimal_places=2, default=12, max_digits=5, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('ac1_epf_employee_limit', models.PositiveIntegerField(default=15000)),
                ('ac1_epf_employer_percentage', models.DecimalField(decimal_places=2, default=3.67, max_digits=5, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('ac1_epf_employer_limit', models.PositiveIntegerField(default=15000)),
                ('ac10_eps_employer_percentage', models.DecimalField(decimal_places=2, default=8.33, max_digits=5, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('ac10_eps_employer_value', models.PositiveIntegerField(default=15000)),
                ('ac2_employer_percentage', models.DecimalField(decimal_places=2, default=0.5, max_digits=5, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('ac21_employer_percentage', models.DecimalField(decimal_places=2, default=0.5, max_digits=5, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('ac22_employer_percentage', models.DecimalField(decimal_places=2, default=0, max_digits=5, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('employer_pf_code', models.CharField(blank=True, max_length=100, null=True)),
                ('esi_employee_percentage', models.DecimalField(decimal_places=2, default=0.75, max_digits=5, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('esi_employee_limit', models.PositiveIntegerField(default=21000)),
                ('esi_employer_percentage', models.DecimalField(decimal_places=2, default=3.25, max_digits=5, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('esi_employer_limit', models.PositiveIntegerField(default=21000)),
                ('employer_esi_code', models.CharField(blank=True, max_length=100, null=True)),
                ('company', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='pf_esi_setup_details', to='api.company')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pf_esi_setup_details', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]