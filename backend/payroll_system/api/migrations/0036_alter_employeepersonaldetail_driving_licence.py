# Generated by Django 4.1.5 on 2023-07-02 00:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0035_alter_employeepersonaldetail_education_qualification_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeepersonaldetail',
            name='driving_licence',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
