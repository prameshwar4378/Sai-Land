# Generated by Django 5.1.1 on 2025-02-12 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ERP_Admin', '0012_alter_emi_total_installments'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otherdues',
            name='fitness_document',
            field=models.FileField(blank=True, null=True, upload_to='PolicyDocuments'),
        ),
        migrations.AlterField(
            model_name='otherdues',
            name='invoice',
            field=models.FileField(blank=True, null=True, upload_to='PolicyDocuments'),
        ),
        migrations.AlterField(
            model_name='otherdues',
            name='permit_document',
            field=models.FileField(blank=True, null=True, upload_to='PolicyDocuments'),
        ),
        migrations.AlterField(
            model_name='otherdues',
            name='puc_document',
            field=models.FileField(blank=True, null=True, upload_to='PolicyDocuments'),
        ),
        migrations.AlterField(
            model_name='otherdues',
            name='rc_book',
            field=models.FileField(blank=True, null=True, upload_to='PolicyDocuments'),
        ),
    ]
