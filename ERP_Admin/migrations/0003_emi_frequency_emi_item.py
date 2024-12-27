# Generated by Django 5.1 on 2024-12-27 03:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ERP_Admin', '0002_emi'),
    ]

    operations = [
        migrations.AddField(
            model_name='emi',
            name='frequency',
            field=models.CharField(choices=[('yearly', 'Yearly'), ('quarterly', 'Quarterly'), ('monthly', 'Monthly'), ('lifetime', 'Lifetime'), ('bi-monthly', 'Bi-Monthly (2 months)')], default='monthly', max_length=20),
        ),
        migrations.CreateModel(
            name='EMI_Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('installment_amount', models.BigIntegerField()),
                ('principal', models.BigIntegerField()),
                ('interest', models.BigIntegerField()),
                ('outstanding_principal', models.BigIntegerField()),
                ('emi', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='emi_items', to='ERP_Admin.emi')),
            ],
        ),
    ]
