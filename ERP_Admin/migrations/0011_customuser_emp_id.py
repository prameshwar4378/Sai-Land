# Generated by Django 5.1 on 2024-12-15 16:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ERP_Admin', '0010_alter_driver_emp_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='emp_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ERP_Admin.emp_id'),
        ),
    ]
