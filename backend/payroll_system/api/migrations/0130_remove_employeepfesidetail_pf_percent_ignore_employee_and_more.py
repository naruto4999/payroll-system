# Generated by Django 4.1.5 on 2023-11-03 07:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0129_alter_companydetails_address_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employeepfesidetail',
            name='pf_percent_ignore_employee',
        ),
        migrations.RemoveField(
            model_name='employeepfesidetail',
            name='pf_percent_ignore_employee_value',
        ),
        migrations.RemoveField(
            model_name='employeepfesidetail',
            name='pf_percent_ignore_employer',
        ),
        migrations.RemoveField(
            model_name='employeepfesidetail',
            name='pf_percent_ignore_employer_value',
        ),
    ]
