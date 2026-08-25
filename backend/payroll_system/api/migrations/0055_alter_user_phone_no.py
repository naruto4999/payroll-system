from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0054_delete_extrafeaturesconfig'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone_no',
            field=models.PositiveBigIntegerField(),
        ),
    ]
