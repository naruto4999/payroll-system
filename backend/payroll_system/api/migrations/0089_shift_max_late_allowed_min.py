# Generated by Django 4.1.5 on 2023-08-23 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0088_rename_next_shift_dealy_shift_next_shift_delay'),
    ]

    operations = [
        migrations.AddField(
            model_name='shift',
            name='max_late_allowed_min',
            field=models.PositiveSmallIntegerField(default=120),
        ),
    ]
