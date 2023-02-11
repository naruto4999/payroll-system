# Generated by Django 4.1.5 on 2023-03-04 14:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(db_index=True, max_length=255, unique=True)),
                ('email', models.EmailField(blank=True, db_index=True, max_length=254, null=True, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=256, unique=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='companies', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Deparment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='deparments', to='api.company')),
            ],
        ),
        migrations.CreateModel(
            name='CompanyDetails',
            fields=[
                ('company', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='company_details', serialize=False, to='api.company')),
                ('address', models.TextField()),
                ('key_person', models.CharField(blank=True, max_length=64)),
                ('involving_industry', models.CharField(blank=True, max_length=64)),
                ('phone_no', models.PositiveBigIntegerField()),
                ('email', models.EmailField(max_length=254)),
                ('pf_no', models.CharField(max_length=30)),
                ('esi_no', models.PositiveBigIntegerField()),
                ('head_office_address', models.TextField()),
                ('pan_no', models.CharField(max_length=10, unique=True)),
                ('gst_no', models.CharField(blank=True, max_length=15)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='all_companies_details', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
