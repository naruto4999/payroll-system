# Generated by Django 4.1.5 on 2023-09-13 12:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0100_rename_repaid_employeeadvancepayment_repaid_amount'),
    ]

    operations = [
        migrations.RenameField(
            model_name='employeeadvancepayment',
            old_name='tenure_months',
            new_name='tenure_months_left',
        ),
    ]