# Generated by Django 5.1 on 2024-12-23 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ERP_Admin', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchase',
            name='bill_file',
            field=models.FileField(null=True, upload_to='Purchase Bill'),
        ),
    ]
