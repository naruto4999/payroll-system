# Generated by Django 4.1.5 on 2023-11-17 10:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_employeemonthlyattendancedetails_company_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeeprofessionaldetail',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='same_category_employees', to='api.category'),
        ),
        migrations.AlterField(
            model_name='employeeprofessionaldetail',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='all_employee_professional_details', to='api.company'),
        ),
        migrations.AlterField(
            model_name='employeeprofessionaldetail',
            name='department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='same_department_employees', to='api.deparment'),
        ),
        migrations.AlterField(
            model_name='employeeprofessionaldetail',
            name='designation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='same_designation_employees', to='api.designation'),
        ),
        migrations.AlterField(
            model_name='employeeprofessionaldetail',
            name='salary_grade',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='same_salary_grade_employees', to='api.salarygrade'),
        ),
        migrations.AlterField(
            model_name='employeeprofessionaldetail',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='all_companys_employee_professional_details', to=settings.AUTH_USER_MODEL),
        ),
    ]
