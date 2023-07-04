# Generated by Django 4.1.5 on 2023-07-03 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0042_remove_employeeprofessionaldetail_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeeprofessionaldetail',
            name='extra_off',
            field=models.CharField(choices=[('no_off', 'No Off'), ('mon1', 'First Monday'), ('mon2', 'Second Monday'), ('mon3', 'Third Monday'), ('mon4', 'Fourth Monday'), ('tue1', 'First Tuesday'), ('tue2', 'Second Tuesday'), ('tue3', 'Third Tuesday'), ('tue4', 'Fourth Tuesday'), ('wed1', 'First Wednesday'), ('wed2', 'Second Wednesday'), ('wed3', 'Third Wednesday'), ('wed4', 'Fourth Wednesday'), ('thu1', 'First Thursday'), ('thu2', 'Second Thursday'), ('thu3', 'Third Thursday'), ('thu4', 'Fourth Thursday'), ('fri1', 'First Friday'), ('fri2', 'Second Friday'), ('fri3', 'Third Friday'), ('fri4', 'Fourth Friday'), ('sat1', 'First Saturday'), ('sat2', 'Second Saturday'), ('sat3', 'Third Saturday'), ('sat4', 'Fourth Saturday'), ('sun1', 'First Sunday'), ('sun2', 'Second Sunday'), ('sun3', 'Third Sunday'), ('sun4', 'Fourth Sunday')], default='no_off', max_length=10),
        ),
    ]