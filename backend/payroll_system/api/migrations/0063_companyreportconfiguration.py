from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0062_repartition_legacy_overtime_and_drop_old_tables'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyReportConfiguration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('report_type', models.CharField(max_length=64)),
                ('output_format', models.CharField(max_length=32)),
                ('options', models.JSONField(blank=True, default=dict)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='report_configurations', to='api.company')),
            ],
        ),
        migrations.AddConstraint(
            model_name='companyreportconfiguration',
            constraint=models.UniqueConstraint(fields=('company', 'report_type', 'output_format'), name='unique_company_report_configuration'),
        ),
    ]
