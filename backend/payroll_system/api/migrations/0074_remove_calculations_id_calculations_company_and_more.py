# Generated by Django 4.1.5 on 2023-08-04 04:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0073_calculations'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='calculations',
            name='id',
        ),
        migrations.AddField(
            model_name='calculations',
            name='company',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='calculations', serialize=False, to='api.company'),
        ),
        migrations.AddField(
            model_name='calculations',
            name='user',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='calculations', to=settings.AUTH_USER_MODEL),
        ),
    ]