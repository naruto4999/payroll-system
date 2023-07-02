# Generated by Django 4.1.5 on 2023-05-29 14:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_bank'),
    ]

    operations = [
        migrations.CreateModel(
            name='LeaveGrade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('limit', models.PositiveSmallIntegerField(default=0)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='leave_grades', to='api.company')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='leave_grades', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]