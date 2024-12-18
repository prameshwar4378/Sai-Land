# Generated by Django 5.1 on 2024-12-12 20:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ERP_Admin', '0002_alter_jobcard_technician'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobcard',
            name='driver',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='job_cards', to='ERP_Admin.driver'),
        ),
        migrations.AlterField(
            model_name='jobcard',
            name='technician',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='job_cards', to='ERP_Admin.technician'),
        ),
    ]
