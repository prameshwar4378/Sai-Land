# Generated by Django 5.1 on 2025-02-23 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ERP_Admin', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='breakdown',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
