# Generated by Django 5.1 on 2025-01-06 16:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ERP_Admin', '0003_rename_loan_ac_no_emi_loan_account_no'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emi',
            name='finance_bank',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='emis', to='ERP_Admin.finance_bank'),
        ),
        migrations.AlterField(
            model_name='insurancetaxdue',
            name='insurance_bank',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='emis', to='ERP_Admin.insurance_bank'),
        ),
    ]
