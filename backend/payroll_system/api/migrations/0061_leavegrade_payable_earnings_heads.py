from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0060_backfill_legacy_attendance_overtime_details'),
    ]

    operations = [
        migrations.CreateModel(
            name='LeaveGradePayableEarningsHead',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('earnings_head', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='payable_leave_grade_links', to='api.earningshead')),
                ('leave_grade', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payable_earnings_head_links', to='api.leavegrade')),
            ],
            options={
                'constraints': [models.UniqueConstraint(fields=('leave_grade', 'earnings_head'), name='unique_leave_grade_payable_earning_head')],
            },
        ),
        migrations.AddField(
            model_name='leavegrade',
            name='payable_earnings_heads',
            field=models.ManyToManyField(blank=True, related_name='payable_leave_grades', through='api.LeaveGradePayableEarningsHead', to='api.earningshead'),
        ),
    ]
