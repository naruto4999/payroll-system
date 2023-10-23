# Generated by Django 4.1.5 on 2023-07-08 06:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0051_alter_employeesalarydetails_overtime_rate'),
    ]

    operations = [
        migrations.AddField(
            model_name='employeesalarydetails',
            name='account_number',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='employeesalarydetails',
            name='bank_name',
            field=models.CharField(blank=True, max_length=75, null=True),
        ),
        migrations.AddField(
            model_name='employeesalarydetails',
            name='bonus_allow',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='employeesalarydetails',
            name='bonus_exg',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='employeesalarydetails',
            name='ifcs',
            field=models.CharField(blank=True, max_length=25, null=True),
        ),
        migrations.AddField(
            model_name='employeesalarydetails',
            name='labour_wellfare_fund',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='employeesalarydetails',
            name='late_deduction',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='employeesalarydetails',
            name='payment_mode',
            field=models.CharField(choices=[('bank_transfer', 'Bank Transfer'), ('cheque', 'Cheque'), ('cash', 'Cash'), ('rtgs', 'RTGS'), ('neft', 'NEFT')], default='bank_transfer', max_length=20),
        ),
        migrations.AddField(
            model_name='employeesalarydetails',
            name='salary_mode',
            field=models.CharField(choices=[('monthly', 'Monthly'), ('daily', 'Daily'), ('piece_rate', 'Piece Rate')], default='monthly', max_length=20),
        ),
    ]