from decimal import Decimal, ROUND_CEILING, ROUND_HALF_UP

from django.db import migrations, models
import django.db.models.deletion


def backfill_esi_configuration_and_snapshots(apps, schema_editor):
    EarningsHead = apps.get_model('api', 'EarningsHead')
    EmployeePfEsiDetail = apps.get_model('api', 'EmployeePfEsiDetail')
    EmployeeSalaryPrepared = apps.get_model('api', 'EmployeeSalaryPrepared')
    PfEsiSetup = apps.get_model('api', 'PfEsiSetup')
    PfEsiSetupEarningsHead = apps.get_model('api', 'PfEsiSetupEarningsHead')

    links = []
    for setup in PfEsiSetup.objects.all().iterator():
        for head_id in EarningsHead.objects.filter(
            company_id=setup.company_id,
            user_id=setup.user_id,
        ).values_list('pk', flat=True):
            links.append(PfEsiSetupEarningsHead(
                pf_esi_setup_id=setup.pk,
                earnings_head_id=head_id,
            ))
    PfEsiSetupEarningsHead.objects.bulk_create(links, ignore_conflicts=True)

    setups = {setup.company_id: setup for setup in PfEsiSetup.objects.all()}
    details = {
        detail.employee_id: detail
        for detail in EmployeePfEsiDetail.objects.all()
    }
    for salary in EmployeeSalaryPrepared.objects.prefetch_related(
        'current_salary_earned_amounts'
    ).iterator(chunk_size=500):
        setup = setups.get(salary.company_id)
        detail = details.get(salary.employee_id)
        if setup is None or detail is None or not detail.esi_allow:
            continue

        earnings_basis = sum(
            row.earned_amount for row in salary.current_salary_earned_amounts.all()
        )
        overtime_applies = detail.esi_on_ot or salary.user.role == 'REGULAR'
        basis_with_overtime = earnings_basis + (
            salary.net_ot_amount_monthly if overtime_applies else 0
        )
        employee_wages_without_overtime = min(
            setup.esi_employee_limit, earnings_basis
        )
        employee_wages = min(setup.esi_employee_limit, basis_with_overtime)
        employer_wages = min(setup.esi_employer_limit, basis_with_overtime)

        salary.esi_employee_wages = employee_wages
        salary.esi_employee_wages_without_overtime = employee_wages_without_overtime
        salary.esi_deducted_without_overtime = int((
            Decimal(employee_wages_without_overtime)
            * setup.esi_employee_percentage
            / Decimal(100)
        ).quantize(Decimal('1'), rounding=ROUND_CEILING))
        salary.esi_employer_contribution = int((
            Decimal(employer_wages)
            * setup.esi_employer_percentage
            / Decimal(100)
        ).quantize(Decimal('1'), rounding=ROUND_HALF_UP))
        salary.save(update_fields=[
            'esi_employee_wages',
            'esi_employee_wages_without_overtime',
            'esi_deducted_without_overtime',
            'esi_employer_contribution',
        ])


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0063_companyreportconfiguration'),
    ]

    operations = [
        migrations.CreateModel(
            name='PfEsiSetupEarningsHead',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('earnings_head', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='esi_setup_links', to='api.earningshead')),
                ('pf_esi_setup', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='esi_earnings_head_links', to='api.pfesisetup')),
            ],
            options={
                'constraints': [models.UniqueConstraint(fields=('pf_esi_setup', 'earnings_head'), name='unique_pf_esi_setup_earning_head')],
            },
        ),
        migrations.AddField(
            model_name='pfesisetup',
            name='esi_earnings_heads',
            field=models.ManyToManyField(blank=True, related_name='esi_setups', through='api.PfEsiSetupEarningsHead', to='api.earningshead'),
        ),
        migrations.AddField(
            model_name='employeesalaryprepared',
            name='esi_deducted_without_overtime',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='employeesalaryprepared',
            name='esi_employee_wages',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='employeesalaryprepared',
            name='esi_employee_wages_without_overtime',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='employeesalaryprepared',
            name='esi_employer_contribution',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.RunPython(
            backfill_esi_configuration_and_snapshots,
            migrations.RunPython.noop,
        ),
    ]
