# Generated by Django 5.1 on 2025-02-12 19:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ERP_Admin', '0014_breakdowntype'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allocatedrivertovehicle',
            name='driver',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='allocated_drivers', to='ERP_Admin.driver'),
        ),
        migrations.AlterField(
            model_name='allocatedrivertovehicle',
            name='vehicle',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='allocated_vehicles', to='ERP_Admin.vehicle'),
        ),
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
        migrations.CreateModel(
            name='Breakdown',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(blank=True, null=True)),
                ('date_time', models.DateTimeField(auto_now_add=True)),
                ('audio', models.FileField(upload_to='Breakdown_Audio')),
                ('image1', models.ImageField(blank=True, null=True, upload_to='Breakdown_Images')),
                ('image2', models.ImageField(blank=True, null=True, upload_to='Breakdown_Images')),
                ('image3', models.ImageField(blank=True, null=True, upload_to='Breakdown_Images')),
                ('image4', models.ImageField(blank=True, null=True, upload_to='Breakdown_Images')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='breakdown_type', to='ERP_Admin.vehicle')),
                ('vehicle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='breakdown_vehicle', to='ERP_Admin.vehicle')),
            ],
        ),
    ]
