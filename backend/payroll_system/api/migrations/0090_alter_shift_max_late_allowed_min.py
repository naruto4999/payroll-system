# Generated by Django 4.1.5 on 2023-08-23 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0089_shift_max_late_allowed_min'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shift',
            name='max_late_allowed_min',
            field=models.PositiveSmallIntegerField(),
        ),
    ]
