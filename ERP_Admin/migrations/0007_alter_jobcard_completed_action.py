# Generated by Django 5.1 on 2024-12-13 20:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ERP_Admin', '0006_rename_job_date_jobcard_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobcard',
            name='completed_action',
            field=models.TextField(blank=True, null=True),
        ),
    ]
