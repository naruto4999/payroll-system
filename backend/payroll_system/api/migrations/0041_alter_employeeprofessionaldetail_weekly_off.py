# Generated by Django 4.1.5 on 2023-07-03 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0040_alter_employeeprofessionaldetail_employee'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeeprofessionaldetail',
            name='weekly_off',
            field=models.CharField(choices=[('mon', 'Monday'), ('tue', 'Tuesday'), ('wed', 'Wednesday'), ('thu', 'Thursday'), ('fri', 'Friday'), ('sat', 'Saturday'), ('sun', 'Sunday')], default='sun', max_length=3),
        ),
    ]