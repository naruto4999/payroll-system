# Generated by Django 4.1.5 on 2023-06-26 23:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0022_deductionshead'),
    ]

    operations = [
        migrations.AddField(
            model_name='deductionshead',
            name='mandatory_deductions',
            field=models.BooleanField(default=False),
        ),
    ]
