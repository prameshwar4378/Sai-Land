# Generated by Django 5.1 on 2025-02-02 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ERP_Admin', '0003_otherdues_invoice_otherdues_rc_book'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchase',
            name='paid_status',
            field=models.CharField(choices=[('Paid', 'Paid'), ('UnPaid', 'UnPaid')], default='UnPaid', max_length=20),
        ),
    ]
