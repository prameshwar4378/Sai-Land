# Generated by Django 5.1 on 2025-02-23 12:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ERP_Admin', '0002_breakdown_is_active'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='breakdown',
            name='is_active',
        ),
    ]
