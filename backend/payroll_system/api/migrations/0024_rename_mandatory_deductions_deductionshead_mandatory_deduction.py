# Generated by Django 4.1.5 on 2023-06-26 23:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0023_deductionshead_mandatory_deductions'),
    ]

    operations = [
        migrations.RenameField(
            model_name='deductionshead',
            old_name='mandatory_deductions',
            new_name='mandatory_deduction',
        ),
    ]