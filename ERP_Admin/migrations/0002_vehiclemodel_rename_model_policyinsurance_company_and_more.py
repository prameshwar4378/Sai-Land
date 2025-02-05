# Generated by Django 5.1 on 2025-02-02 12:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ERP_Admin', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='VehicleModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model_name', models.CharField(db_index=True, max_length=50, unique=True)),
            ],
        ),
        migrations.RenameModel(
            old_name='Model',
            new_name='PolicyInsurance_Company',
        ),
        migrations.RenameField(
            model_name='emi',
            old_name='loan_tenure',
            new_name='tenure',
        ),
        migrations.RenameField(
            model_name='emi_installment',
            old_name='due_date',
            new_name='next_due_date',
        ),
        migrations.RenameField(
            model_name='policyinsurance_company',
            old_name='model_name',
            new_name='name',
        ),
        migrations.RemoveField(
            model_name='emi',
            name='due_date',
        ),
        migrations.RemoveField(
            model_name='emi',
            name='paid_tenure',
        ),
        migrations.RemoveField(
            model_name='emi',
            name='total_loan_amount',
        ),
        migrations.RemoveField(
            model_name='vehicle',
            name='vehicle_name',
        ),
        migrations.AddField(
            model_name='emi',
            name='emi_amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='otherdues',
            name='fitness_document',
            field=models.ImageField(blank=True, null=True, upload_to='PolicyDocuments'),
        ),
        migrations.AddField(
            model_name='otherdues',
            name='permit_document',
            field=models.ImageField(blank=True, null=True, upload_to='PolicyDocuments'),
        ),
        migrations.AddField(
            model_name='otherdues',
            name='puc_document',
            field=models.ImageField(blank=True, null=True, upload_to='PolicyDocuments'),
        ),
        migrations.AddField(
            model_name='policy',
            name='insurance_company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Insurance', to='ERP_Admin.insurance_bank'),
        ),
        migrations.AddField(
            model_name='policy',
            name='premium_amount',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='owner_name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='emi',
            name='total_installments',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='emi_installment',
            name='emi_amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='model_name',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='vehicle_model_name', to='ERP_Admin.vehiclemodel'),
        ),
        migrations.AlterField(
            model_name='product',
            name='model',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='items', to='ERP_Admin.vehiclemodel'),
        ),
    ]
