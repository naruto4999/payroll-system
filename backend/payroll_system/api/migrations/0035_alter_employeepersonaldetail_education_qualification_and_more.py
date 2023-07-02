# Generated by Django 4.1.5 on 2023-07-01 21:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0034_alter_employeepersonaldetail_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeepersonaldetail',
            name='education_qualification',
            field=models.CharField(blank=True, choices=[('0', 'No Qualification'), ('1', '1st class'), ('2', '2nd class'), ('3', '3rd class'), ('4', '4th class'), ('5', '5th class'), ('6', '6th class'), ('7', '7th class'), ('8', '8th class'), ('9', '9th class'), ('10', '10th class'), ('11', '11th class'), ('12', '12th class'), ('G', 'Graduate'), ('PG', ' Post Graduate')], max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='employeepersonaldetail',
            name='gender',
            field=models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Others')], max_length=1, null=True),
        ),
    ]
