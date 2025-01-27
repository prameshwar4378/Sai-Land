# Generated by Django 5.1 on 2025-01-09 15:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ERP_Admin', '0005_remove_insurancetaxdue_insurance_name_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='OtherDues',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tax_frequency', models.CharField(blank=True, choices=[('yearly', 'Yearly'), ('quarterly', 'Quarterly'), ('monthly', 'Monthly'), ('lifetime', 'Lifetime'), ('bi-monthly', 'Bi-Monthly (2 months)')], max_length=255, null=True)),
                ('tax_amount', models.FloatField(blank=True, null=True)),
                ('tax_due_date', models.DateField(blank=True, null=True)),
                ('fitness_due_date', models.DateField(blank=True, null=True)),
                ('permit_due_date', models.DateField(blank=True, null=True)),
                ('puc_due_date', models.DateField(blank=True, null=True)),
                ('vehicle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ERP_Admin.vehicle')),
            ],
        ),
    ]
