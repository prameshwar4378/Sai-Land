# Generated by Django 5.1 on 2024-12-15 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ERP_Admin', '0007_alter_jobcard_completed_action'),
    ]

    operations = [
        migrations.CreateModel(
            name='EMP_ID',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('emp_id', models.CharField(max_length=20)),
            ],
        ),
    ]