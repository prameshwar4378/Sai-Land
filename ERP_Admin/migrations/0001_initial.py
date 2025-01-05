# Generated by Django 5.1 on 2025-01-05 18:00

import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Driver',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('driver_name', models.CharField(max_length=20)),
                ('license_number', models.CharField(blank=True, max_length=20, null=True, unique=True)),
                ('adhaar_number', models.CharField(blank=True, max_length=20, null=True, unique=True)),
                ('mobile_number', models.CharField(blank=True, max_length=15, null=True)),
                ('alternate_mobile_number', models.CharField(blank=True, max_length=15, null=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('date_joined', models.DateField(blank=True, null=True)),
                ('adhaar_card_photo', models.FileField(blank=True, null=True, upload_to='Documents')),
                ('pan_card_photo', models.FileField(blank=True, null=True, upload_to='Documents')),
                ('driving_license_photo', models.FileField(blank=True, null=True, upload_to='Documents')),
                ('profile_photo', models.ImageField(blank=True, null=True, upload_to='Documents')),
            ],
        ),
        migrations.CreateModel(
            name='EMI',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('loan_amount', models.BigIntegerField()),
                ('total_installments', models.PositiveIntegerField()),
                ('paid_installments', models.PositiveIntegerField(default=0)),
                ('next_due_date', models.DateField()),
                ('file', models.FileField(upload_to='emi/')),
                ('frequency', models.CharField(choices=[('yearly', 'Yearly'), ('quarterly', 'Quarterly'), ('monthly', 'Monthly'), ('lifetime', 'Lifetime'), ('bi-monthly', 'Bi-Monthly (2 months)')], default='monthly', max_length=20)),
                ('status', models.CharField(choices=[('pending', 'Pending EMI'), ('closed', 'Closed EMI')], default='pending', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='EMP_ID',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('emp_id', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Finance_Bank',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bank_name', models.CharField(db_index=True, max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Insurance_Bank',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bank_name', models.CharField(db_index=True, max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Model',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model_name', models.CharField(db_index=True, max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Party',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('business_name', models.CharField(max_length=100)),
                ('customer_name', models.CharField(max_length=100)),
                ('gst_number', models.CharField(blank=True, max_length=15, null=True, unique=True)),
                ('mobile_number', models.CharField(max_length=15, unique=True)),
                ('alternate_mobile_number', models.CharField(blank=True, max_length=15, null=True)),
                ('address', models.TextField(blank=True, null=True, verbose_name='Address')),
                ('document1', models.FileField(blank=True, null=True, upload_to='ClientDocuments')),
                ('document2', models.FileField(blank=True, null=True, upload_to='ClientDocuments')),
                ('document3', models.FileField(blank=True, null=True, upload_to='ClientDocuments')),
            ],
        ),
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bill_no', models.CharField(db_index=True, max_length=50, unique=True)),
                ('supplier_name', models.CharField(blank=True, db_index=True, max_length=100, null=True)),
                ('bill_type', models.CharField(choices=[('GST BILL', 'GST BILL'), ('Without GST BILL', 'Without GST BILL')], db_index=True, max_length=30)),
                ('bill_date', models.DateField(db_index=True)),
                ('total_cost', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('bill_file', models.FileField(null=True, upload_to='Purchase Bill')),
            ],
        ),
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vehicle_name', models.CharField(max_length=100)),
                ('vehicle_number', models.CharField(max_length=50, unique=True)),
                ('status', models.CharField(choices=[('active', 'active'), ('inactive', 'Inactive')], default='active', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='EMI_Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('installment_amount', models.BigIntegerField()),
                ('principal', models.BigIntegerField()),
                ('interest', models.BigIntegerField()),
                ('outstanding_principal', models.BigIntegerField()),
                ('installment_date', models.DateField(null=True)),
                ('emi', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='emi_items', to='ERP_Admin.emi')),
            ],
        ),
        migrations.AddField(
            model_name='emi',
            name='finance_bank',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='emis', to='ERP_Admin.finance_bank'),
        ),
        migrations.CreateModel(
            name='JobCard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_card_number', models.CharField(editable=False, max_length=20, unique=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('reported_defect', models.TextField()),
                ('completed_action', models.TextField(blank=True, null=True)),
                ('completed_date', models.DateTimeField(blank=True, null=True)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('in_progress', 'In Progress'), ('completed', 'Completed')], default='pending', max_length=20)),
                ('labour_cost', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('driver', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='job_cards', to='ERP_Admin.driver')),
                ('party', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='job_cards', to='ERP_Admin.party')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_code', models.CharField(db_index=True, max_length=20, unique=True)),
                ('product_name', models.CharField(db_index=True, max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('sale_price', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('minimum_stock_alert', models.PositiveIntegerField(default=0)),
                ('available_stock', models.IntegerField(blank=True, db_index=True, default=0, null=True)),
                ('product_image', models.ImageField(blank=True, max_length=500, null=True, upload_to='Product Images')),
                ('model', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='items', to='ERP_Admin.model')),
            ],
        ),
        migrations.CreateModel(
            name='JobCardItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('cost', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)])),
                ('total_cost', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('job_card', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='ERP_Admin.jobcard')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='job_card_items', to='ERP_Admin.product')),
            ],
        ),
        migrations.CreateModel(
            name='PurchaseItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('cost_per_unit', models.DecimalField(decimal_places=2, max_digits=10)),
                ('total_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ERP_Admin.product')),
                ('purchase', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='ERP_Admin.purchase')),
            ],
        ),
        migrations.CreateModel(
            name='Technician',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('technician_name', models.CharField(max_length=100, verbose_name='Technician Name')),
                ('adhaar_number', models.CharField(max_length=20, unique=True, verbose_name='Aadhaar Number')),
                ('mobile_number', models.CharField(max_length=10, unique=True, verbose_name='Mobile Number')),
                ('alternate_mobile_number', models.CharField(blank=True, max_length=15, null=True)),
                ('email', models.EmailField(blank=True, max_length=100, null=True, unique=True, verbose_name='Email Address')),
                ('address', models.TextField(blank=True, null=True, verbose_name='Address')),
                ('date_of_birth', models.DateField(blank=True, null=True, verbose_name='Date of Birth')),
                ('date_joined', models.DateField(auto_now_add=True, verbose_name='Date Joined')),
                ('pan_card', models.FileField(blank=True, null=True, upload_to='Documents')),
                ('adhaar_card', models.FileField(blank=True, null=True, upload_to='Documents')),
                ('profile_photo', models.FileField(blank=True, null=True, upload_to='Documents')),
                ('additional_docs', models.FileField(blank=True, null=True, upload_to='Documents')),
                ('emp_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ERP_Admin.emp_id')),
            ],
            options={
                'verbose_name': 'Technician',
                'verbose_name_plural': 'Technicians',
            },
        ),
        migrations.AddField(
            model_name='jobcard',
            name='technician',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='job_cards', to='ERP_Admin.technician'),
        ),
        migrations.CreateModel(
            name='Policy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('policy_number', models.CharField(max_length=50)),
                ('policy_file', models.FileField(upload_to='policies/')),
                ('due_date', models.DateField()),
                ('vehicle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='policies', to='ERP_Admin.vehicle')),
            ],
        ),
        migrations.AddField(
            model_name='jobcard',
            name='vehicle',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='job_cards', to='ERP_Admin.vehicle'),
        ),
        migrations.CreateModel(
            name='InsuranceTaxDue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('insurance_amount', models.FloatField(blank=True, null=True)),
                ('insurance_name', models.CharField(blank=True, max_length=255, null=True)),
                ('insurance_due_date', models.DateField(blank=True, null=True)),
                ('tax_frequency', models.CharField(blank=True, choices=[('yearly', 'Yearly'), ('quarterly', 'Quarterly'), ('monthly', 'Monthly'), ('lifetime', 'Lifetime'), ('bi-monthly', 'Bi-Monthly (2 months)')], max_length=255, null=True)),
                ('tax_amount', models.FloatField(blank=True, null=True)),
                ('tax_due_date', models.DateField(blank=True, null=True)),
                ('fitness_due_date', models.DateField(blank=True, null=True)),
                ('permit_due_date', models.DateField(blank=True, null=True)),
                ('puc_due_date', models.DateField(blank=True, null=True)),
                ('insurance_bank', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='emis', to='ERP_Admin.insurance_bank')),
                ('vehicle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ERP_Admin.vehicle')),
            ],
        ),
        migrations.AddField(
            model_name='emi',
            name='vehicle',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='emis', to='ERP_Admin.vehicle'),
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('is_admin', models.BooleanField(default=False)),
                ('is_account', models.BooleanField(default=False)),
                ('is_workshop', models.BooleanField(default=False)),
                ('is_driver', models.BooleanField(default=False)),
                ('is_finance', models.BooleanField(default=False)),
                ('emp_id', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='ERP_Admin.emp_id')),
                ('groups', models.ManyToManyField(blank=True, related_name='customuser_groups', to='auth.group')),
                ('user_permissions', models.ManyToManyField(blank=True, related_name='customuser_permissions', to='auth.permission')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name='driver',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='AllocateDriverToVehicle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('joining_date_time', models.DateTimeField(auto_now_add=True)),
                ('leaving_date_time', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('driver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='allocated_vehicles', to='ERP_Admin.driver')),
                ('vehicle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='allocated_drivers', to='ERP_Admin.vehicle')),
            ],
            options={
                'indexes': [models.Index(fields=['vehicle', 'is_active'], name='ERP_Admin_a_vehicle_100871_idx'), models.Index(fields=['driver', 'is_active'], name='ERP_Admin_a_driver__e46f8f_idx')],
            },
        ),
    ]
