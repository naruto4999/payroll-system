# Generated by Django 4.1.5 on 2023-09-29 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0116_rename_earning_head_earnedamount_earnings_head'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='earnedamount',
            name='unique_earned_amount_for_each_earning_head',
        ),
        migrations.AddConstraint(
            model_name='earnedamount',
            constraint=models.UniqueConstraint(fields=('earnings_head', 'salary_prepared'), name='unique_earned_amount_for_each_earnings_head'),
        ),
    ]