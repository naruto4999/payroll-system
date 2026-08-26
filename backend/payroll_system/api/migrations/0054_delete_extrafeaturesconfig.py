from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0052_companydetails_payroll_timezone_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ExtraFeaturesConfig',
        ),
    ]
