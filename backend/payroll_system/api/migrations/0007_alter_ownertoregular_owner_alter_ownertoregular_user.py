# Generated by Django 4.1.5 on 2023-05-11 15:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_otp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ownertoregular',
            name='owner',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='regulars', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='ownertoregular',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='owners', to=settings.AUTH_USER_MODEL),
        ),
    ]
