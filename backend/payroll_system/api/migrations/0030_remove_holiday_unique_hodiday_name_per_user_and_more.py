# Generated by Django 5.0 on 2024-02-01 08:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0029_alter_employeeprofessionaldetail_category_and_more'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='holiday',
            name='unique_hodiday_name_per_user',
        ),
        migrations.AddConstraint(
            model_name='holiday',
            constraint=models.UniqueConstraint(fields=('user', 'company', 'name', 'date'), name='unique_hodiday_name_per_user'),
        ),
    ]
