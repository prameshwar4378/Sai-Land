# Generated by Django 5.1 on 2025-02-23 03:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ERP_Admin', '0021_alter_fuelrecord_driver'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allocatedrivertovehicle',
            name='joining_date_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
