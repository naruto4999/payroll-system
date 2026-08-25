from django.db import migrations, models
from django.db.models import Q


def clear_inactive_default_flags(apps, schema_editor):
    OvertimePolicy = apps.get_model('api', 'OvertimePolicy')
    OvertimePolicy.objects.filter(is_default=True, is_active=False).update(is_default=False)


class Migration(migrations.Migration):
    dependencies = [
        ('api', '0050_employeesalarypreparedovertimedetail_overtimepolicy_and_more'),
    ]

    operations = [
        migrations.RunPython(clear_inactive_default_flags, migrations.RunPython.noop),
        migrations.AddConstraint(
            model_name='overtimepolicy',
            constraint=models.CheckConstraint(
                check=Q(is_default=False) | Q(is_active=True),
                name='overtime_policy_default_requires_active',
            ),
        ),
    ]
