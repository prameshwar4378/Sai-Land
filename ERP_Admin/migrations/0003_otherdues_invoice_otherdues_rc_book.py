# Generated by Django 5.1 on 2025-02-02 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ERP_Admin', '0002_vehiclemodel_rename_model_policyinsurance_company_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='otherdues',
            name='invoice',
            field=models.ImageField(blank=True, null=True, upload_to='PolicyDocuments'),
        ),
        migrations.AddField(
            model_name='otherdues',
            name='rc_book',
            field=models.ImageField(blank=True, null=True, upload_to='PolicyDocuments'),
        ),
    ]
