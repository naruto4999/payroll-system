from decimal import Decimal

from django.db import migrations


POLICIES = (
    ('Regular days - single rate', 'REGULAR_DAYS_SINGLE', Decimal('1')),
    ('Regular days - double rate', 'REGULAR_DAYS_DOUBLE', Decimal('2')),
)


def create_regular_days_policies(apps, schema_editor):
    Company = apps.get_model('api', 'Company')
    OvertimePolicy = apps.get_model('api', 'OvertimePolicy')
    OvertimePolicyDayRule = apps.get_model('api', 'OvertimePolicyDayRule')

    for company in Company.objects.all():
        for name, code, multiplier in POLICIES:
            policy, _ = OvertimePolicy.objects.get_or_create(
                company=company,
                code=code,
                defaults={
                    'name': name,
                    'is_default': False,
                    'is_active': True,
                    'is_system': True,
                    'earnings_basis': 'ALL_EARNINGS',
                    'rounding_increment_minutes': 30,
                    'round_up_from_minutes': 16,
                },
            )
            OvertimePolicyDayRule.objects.update_or_create(
                policy=policy,
                day_type='REGULAR',
                defaults={
                    'multiplier': multiplier,
                    'late_deduction_priority': 1,
                },
            )


def noop_reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0055_alter_user_phone_no'),
    ]

    operations = [
        migrations.RunPython(create_regular_days_policies, noop_reverse),
    ]
