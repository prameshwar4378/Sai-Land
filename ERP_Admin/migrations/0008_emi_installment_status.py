# Generated by Django 5.1 on 2025-02-03 19:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ERP_Admin', '0007_alter_emi_interest_rate'),
    ]

    operations = [
        migrations.AddField(
            model_name='emi_installment',
            name='status',
            field=models.CharField(choices=[('Paid', 'Paid'), ('Pending', 'Pending')], default='Pending', max_length=20),
        ),
    ]
