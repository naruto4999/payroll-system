# Generated by Django 5.0 on 2024-02-11 15:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0036_remove_subusermiscsettings_max_female_ot_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subusermiscsettings',
            name='date',
        ),
    ]
