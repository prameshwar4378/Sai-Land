# Generated by Django 5.1 on 2024-12-25 03:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ERP_Admin', '0003_alter_jobcard_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobcard',
            name='closing_date',
            field=models.DateField(auto_now=True, null=True),
        ),
    ]