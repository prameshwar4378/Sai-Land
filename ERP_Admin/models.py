from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models, transaction
import os

from django.conf import settings

class EMP_ID(models.Model):
    emp_id = models.CharField(max_length=20) 
    def __str__(self):
        return f"{self.emp_id}"

class CustomUser(AbstractUser):
    is_admin = models.BooleanField(default=False)
    is_account = models.BooleanField(default=False)
    is_workshop = models.BooleanField(default=False)
    is_driver = models.BooleanField(default=False)
    is_finance = models.BooleanField(default=False)
    is_fuel = models.BooleanField(default=False) 
    emp_id = models.OneToOneField(EMP_ID, on_delete=models.CASCADE, null=True)
    profile_photo=models.ImageField(upload_to="profile_images", max_length=None, null=True, blank=True)
    groups = models.ManyToManyField(
        Group,
        related_name='customuser_groups',  # Custom reverse relation name
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_permissions',  # Custom reverse relation name
        blank=True
    )
     
    def __str__(self):
        return self.username


 
class VehicleModel(models.Model):
    model_name = models.CharField(max_length=50, unique=True, db_index=True) 
    def __str__(self):
        return self.model_name
 
class Insurance_Bank(models.Model):
    bank_name = models.CharField(max_length=50, unique=True, db_index=True) 
    def __str__(self):
        return self.bank_name
 
class Finance_Bank(models.Model):
    bank_name = models.CharField(max_length=50, unique=True, db_index=True) 
    def __str__(self):
        return self.bank_name
 
class PolicyInsurance_Company(models.Model):
    name = models.CharField(max_length=50, unique=True, db_index=True) 
    def __str__(self):
        return self.name


VEHICLE_STATUS = (
    ('active', 'active'),
    ('inactive', 'Inactive'), 
) 



class Vehicle(models.Model):
    owner_name = models.CharField(max_length=50,null=True,blank=True)
    model_name = models.ForeignKey(VehicleModel, related_name='vehicle_model_name', null=True, blank=True, on_delete=models.CASCADE)
    vehicle_number = models.CharField(max_length=50, unique=True)
    status=models.CharField(max_length=50, default='active', choices=VEHICLE_STATUS)
    def __str__(self):
        return f"{self.model_name.model_name} ({self.vehicle_number[:-5]} {self.vehicle_number[-4:]})"


class Driver(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True)
    driver_name = models.CharField(max_length=20, null=False, blank=False)
    license_number = models.CharField(max_length=20, unique=True, null=True, blank=True)
    adhaar_number = models.CharField(max_length=20, unique=True, null=True, blank=True)
    mobile_number = models.CharField(max_length=15, null=True, blank=True)
    alternate_mobile_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    date_joined = models.DateField(auto_now_add=False, null=True, blank=True)
    adhaar_card_photo=models.FileField(upload_to="Documents", max_length=None, null=True, blank=True)
    pan_card_photo=models.FileField(upload_to="Documents", max_length=None, null=True, blank=True)
    driving_license_photo=models.FileField(upload_to="Documents", max_length=None, null=True, blank=True)
    profile_photo=models.ImageField(upload_to="Documents", max_length=None, null=True, blank=True)
    
    def __str__(self):
        return f"{self.driver_name} - {self.user.username}"
    


class Technician(models.Model):
    emp_id = models.ForeignKey(EMP_ID, on_delete=models.CASCADE, null=True)
    technician_name = models.CharField(max_length=100, verbose_name="Technician Name")
    adhaar_number = models.CharField(max_length=20, unique=True, verbose_name="Aadhaar Number")
    mobile_number = models.CharField(max_length=10, unique=True, verbose_name="Mobile Number")
    alternate_mobile_number = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(max_length=100, unique=True, null=True, blank=True, verbose_name="Email Address")
    address = models.TextField(null=True, blank=True, verbose_name="Address")
    date_of_birth = models.DateField(null=True, blank=True, verbose_name="Date of Birth")
    date_joined = models.DateField(auto_now_add=True, verbose_name="Date Joined") 
    pan_card=models.FileField(upload_to="Documents", max_length=None, null=True, blank=True)
    adhaar_card=models.FileField(upload_to="Documents", max_length=None, null=True, blank=True)
    profile_photo=models.FileField(upload_to="Documents", max_length=None, null=True, blank=True)
    additional_docs=models.FileField(upload_to="Documents", max_length=None, null=True, blank=True)

    
    def save(self, *args, **kwargs):
        if not self.id:  # Only execute this logic when creating a new driver instance
            last_emp_id = EMP_ID.objects.order_by('-id').first()
            if last_emp_id:
                last_number = int(last_emp_id.emp_id.split('-')[1])
                # Create a new EMP_ID instance or fetch it if necessary
                new_emp_id = EMP_ID.objects.create(emp_id=f"SLD-{last_number + 1}")
                self.emp_id = new_emp_id  # Assign the EMP_ID instance to emp_id
            else:
                # Create the first EMP_ID instance
                new_emp_id = EMP_ID.objects.create(emp_id="SLD-1")
                self.emp_id = new_emp_id  # Assign the EMP_ID instance to emp_id
        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.technician_name}"

    class Meta:
        verbose_name = "Technician"
        verbose_name_plural = "Technicians"


class Party(models.Model):
    business_name = models.CharField(max_length=100)
    customer_name = models.CharField(max_length=100)
    gst_number = models.CharField(max_length=15, unique=True, blank=True, null=True)
    mobile_number = models.CharField(max_length=15, unique=True)
    alternate_mobile_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(null=True, blank=True, verbose_name="Address")
    document1=models.FileField(upload_to="ClientDocuments", max_length=None, null=True, blank=True)
    document2=models.FileField(upload_to="ClientDocuments", max_length=None, null=True, blank=True)
    document3=models.FileField(upload_to="ClientDocuments", max_length=None, null=True, blank=True)

    def __str__(self):
        return self.business_name
    



class Product(models.Model):
    product_code = models.CharField(max_length=20, unique=True, db_index=True)
    product_name = models.CharField(max_length=100, db_index=True)
    model = models.ForeignKey(VehicleModel, related_name='items', null=True, blank=True, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)  # Use DecimalField for monetary values
    minimum_stock_alert = models.PositiveIntegerField(default=0)
    available_stock = models.IntegerField(default=0, db_index=True, null=True, blank=True)
    product_image=models.ImageField(upload_to="Product Images", height_field=None, width_field=None, max_length=500, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.product_image:
            self.product_image = 'default_image.webp'  # Set default image if no image is uploaded
        super(Product, self).save(*args, **kwargs)
    
    def __str__(self):
        return f" #{self.product_code} on {self.product_name}"

PURCHASE_GST=(
    ('GST BILL','GST BILL'),
    ('Without GST BILL','Without GST BILL')
)

PURCHASE_PAID_STATUS=(
    ('Paid','Paid'),
    ('UnPaid','UnPaid')
)
class Purchase(models.Model):
    bill_no = models.CharField(max_length=50, db_index=True, unique=True, null=False, blank=False)
    supplier_name = models.CharField(max_length=100, db_index=True, null=True, blank=True)
    bill_type = models.CharField(max_length=30, db_index=True, choices=PURCHASE_GST)
    bill_date = models.DateField(auto_now_add=False, db_index=True)
    total_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
    bill_file = models.FileField(upload_to="Purchase Bill", null=True, blank=False)
    paid_status = models.CharField(max_length=20, choices=PURCHASE_PAID_STATUS, default='UnPaid')
    def __str__(self):
        return f"Purchase #{self.bill_no} on {self.bill_date}"


class PurchaseItem(models.Model):
    purchase = models.ForeignKey(Purchase, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, db_index=True)
    quantity = models.PositiveIntegerField()
    cost_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def save(self, *args, **kwargs):
        # Update product stock on save
        if self.pk is None:  # Only add stock if it's a new record
            self.product.available_stock += self.quantity
        else:  # If updated, adjust stock accordingly
            original = PurchaseItem.objects.get(pk=self.pk)
            self.product.available_stock += self.quantity - original.quantity
        self.product.save()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Adjust stock on deletion
        self.product.available_stock -= self.quantity
        self.product.save()
        super().delete(*args, **kwargs)

    def __str__(self):
        return f"{self.quantity} of {self.product.product_name} in Purchase #{self.purchase.id}"


from django.db import models
from django.core.validators import MinValueValidator

JOB_CARD_STATUS = [
    ('pending', 'Pending'),
    ('in_progress', 'In Progress'),
    ('completed', 'Completed'),
]


class JobCard(models.Model):
    job_card_number = models.CharField(max_length=20, unique=True, editable=False)
    technician = models.ForeignKey('Technician', related_name='job_cards',  on_delete=models.CASCADE, null=True, blank=True)
    driver= models.ForeignKey('Driver', related_name='job_cards',  on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    reported_defect = models.TextField()
    completed_action = models.TextField(null=True, blank=True)
    completed_date = models.DateTimeField(auto_now_add=False,auto_now=False,null=True, blank=True)
    party = models.ForeignKey('Party', related_name='job_cards', on_delete=models.SET_NULL, null=True, blank=True)
    vehicle = models.ForeignKey('Vehicle', related_name='job_cards', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=JOB_CARD_STATUS, default='pending')
    labour_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(0)])
    
    def save(self, *args, **kwargs):
        if not self.id:
            last_job_card = JobCard.objects.order_by('-id').first()
            if last_job_card:
                last_number = int(last_job_card.job_card_number)
                self.job_card_number = int(last_number) + int(1)
            else:
                self.job_card_number = 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Job Card {self.job_card_number} for Vehicle ID {self.vehicle.id}"


class JobCardItem(models.Model):
    job_card = models.ForeignKey(JobCard, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='job_card_items', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    cost = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(0)])
    def __str__(self):
        return f"Item {self.product.id} for Job Card {self.job_card.job_card_number}"

    def save(self, *args, **kwargs):
        with transaction.atomic():
            if self.pk is None:  # Only add stock if it's a new record
                self.product.available_stock -= self.quantity
            else:   
                original_item = JobCardItem.objects.get(pk=self.pk)
                quantity_diff = self.quantity - original_item.quantity
                self.product.available_stock -= quantity_diff
            # Save the product with updated stock
            self.product.save()
            super().save(*args, **kwargs)


    def delete(self, *args, **kwargs):
        with transaction.atomic():
            self.product.available_stock += self.quantity
            self.product.save()
            super().delete(*args, **kwargs)

    def __str__(self):
        return f"Job Card {self.job_card.job_card_number} for Vehicle ID {self.job_card.vehicle}"


class Policy(models.Model):
    policy_number=models.CharField(max_length=50) 
    insurance_company = models.ForeignKey(Insurance_Bank, on_delete=models.CASCADE, related_name='Insurance',null=True, blank=True)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='policies')
    policy_file = models.FileField(upload_to='policies/' )
    due_date = models.DateField()
    premium_amount=models.BigIntegerField(null=True, blank=True) 

    def __str__(self):
        return f"Policy for {self.vehicle.vehicle_number[:-5]} {self.vehicle.vehicle_number[-4:]} - {self.vehicle.model_name.model_name}"
 
FREQUENCY_CHOICES = (
    ('yearly', 'Yearly'),
    ('quarterly', 'Quarterly'),
    ('monthly', 'Monthly'),
    ('lifetime', 'Lifetime'),
    ('bi-monthly', 'Bi-Monthly (2 months)'),
)

EMI_STATUS_CHOICES = (
    ('pending', 'Pending EMI'),
    ('closed', 'Closed EMI'), 
) 

class EMI(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='emis')
    finance_bank = models.ForeignKey(Finance_Bank, on_delete=models.CASCADE, related_name='emis',null=True, blank=True)
    loan_account_no=models.CharField(max_length=50,null=True)
    emi_amount = models.DecimalField(max_digits=10,default=0, decimal_places=2)
    loan_amount=models.BigIntegerField()
    total_installments = models.PositiveIntegerField(default=0)
    paid_installments = models.PositiveIntegerField(default=0)
    next_due_date = models.DateField(null=True, blank=True)
    file=models.FileField(upload_to='emi/', max_length=100)
    frequency = models.CharField( max_length=20, choices=FREQUENCY_CHOICES,  default='monthly' )
    status = models.CharField( max_length=20, choices=EMI_STATUS_CHOICES,  default='pending' )

    interest_rate = models.DecimalField(null=True, blank=True,max_digits=5, decimal_places=2, help_text='Interest rate in percentage')
    tenure = models.PositiveIntegerField()
        
    @property
    def remaining_installments(self):
        return self.tenure - self.paid_installments

    def __str__(self):
        return f"EMI for {self.vehicle.vehicle_number[:-5]} {self.vehicle.vehicle_number[-4:]} - ({self.remaining_installments} remaining)"

INSTALLMENT_PAID_STATUS=(
    ('Paid','Paid'),
    ('Pending','Pending')
)
   


class EMI_Installment(models.Model):
    emi = models.ForeignKey(EMI, on_delete=models.CASCADE, related_name='installments')
    installment_number = models.PositiveIntegerField(default=0)
    next_due_date = models.DateField(null=True, blank=True)
    paid_date = models.DateField(null=True, blank=True)
    emi_amount = models.DecimalField(max_digits=10,default=0, decimal_places=2)
    principal_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    interest_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    outstanding_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField( max_length=20, choices=INSTALLMENT_PAID_STATUS,  default='Pending' )

    def save(self, *args, **kwargs):
        print("success")
        if not self.pk:
            self.emi.paid_installments += 1
            self.emi.save()
        super(EMI_Installment, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.emi.paid_installments > 0:
            self.emi.paid_installments -= 1
            self.emi.save()
        super(EMI_Installment, self).delete(*args, **kwargs)


 

class EMI_Item(models.Model):
    emi = models.ForeignKey('EMI', on_delete=models.CASCADE, related_name='emi_items')
    installment_amount = models.BigIntegerField()
    principal = models.BigIntegerField()
    interest = models.BigIntegerField()
    outstanding_principal = models.BigIntegerField()
    installment_date = models.DateField(null=True)

    def save(self, *args, **kwargs):
        # Check if this is a new record
        if not self.pk:
            # Increment the paid_installments for the associated EMI
            self.emi.paid_installments += 1
            self.emi.save()
        super(EMI_Item, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.emi.paid_installments > 0:
            self.emi.paid_installments -= 1
            self.emi.save()
        super(EMI_Item, self).delete(*args, **kwargs)

    def __str__(self):
        return f"Installment for EMI {self.emi.id} - Amount: {self.installment_amount}"
    
 
class OtherDues(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE) 
    tax_frequency = models.CharField(max_length=255, choices=FREQUENCY_CHOICES,null=True, blank=True)
    tax_amount = models.FloatField(null=True, blank=True)
    tax_due_date = models.DateField(null=True, blank=True) 
    fitness_due_date = models.DateField(null=True,blank=True)
    permit_due_date = models.DateField(null=True,blank=True)
    puc_due_date = models.DateField(null=True,blank=True)
    fitness_document=models.FileField(upload_to="PolicyDocuments", max_length=None, null=True, blank=True)
    permit_document=models.FileField(upload_to="PolicyDocuments", max_length=None, null=True, blank=True)
    puc_document=models.FileField(upload_to="PolicyDocuments", max_length=None, null=True, blank=True)
    rc_book=models.FileField(upload_to="PolicyDocuments", max_length=None, null=True, blank=True)
    invoice=models.FileField(upload_to="PolicyDocuments", max_length=None, null=True, blank=True)
 


class Enquiry(models.Model):
    name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    date = models.DateField(auto_now_add=True,null=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"
    


class AllocateDriverToVehicle(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name="allocated_vehicles")
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, related_name="allocated_drivers")
    joining_date_time = models.DateTimeField(null=True,blank=True)
    leaving_date_time = models.DateTimeField(null=True,blank=True)
    is_active = models.BooleanField(default=True)
 
    class Meta:
        indexes = [
            models.Index(fields=['vehicle', 'is_active']),
            models.Index(fields=['driver', 'is_active']),
    ]
        
    def __str__(self):
        return f"Driver {self.driver} assigned to Vehicle {self.vehicle}"

class BreakdownType(models.Model):
    type = models.CharField(max_length=100) 
    def __str__(self):
        return self.type
      
class Breakdown(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name="breakdown_vehicle", null=True, blank=True)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, related_name="breakdown_driver", null=True, blank=True)
    type = models.ForeignKey(BreakdownType, on_delete=models.CASCADE, related_name="breakdown_type", null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    date_time = models.DateTimeField(auto_now_add=True)
    audio=models.FileField(upload_to="Breakdown_Audio", null=True, blank=True)
    image1=models.ImageField(upload_to="Breakdown_Images", max_length=None, null=True, blank=True)
    image2=models.ImageField(upload_to="Breakdown_Images", max_length=None, null=True, blank=True)
    image3=models.ImageField(upload_to="Breakdown_Images", max_length=None, null=True, blank=True)
    image4=models.ImageField(upload_to="Breakdown_Images", max_length=None, null=True, blank=True)
    
    def __str__(self):
        return f"{self.vehicle.vehicle_number} - {self.date_time}"




class FuelRecord(models.Model):
    vehicle = models.ForeignKey('Vehicle', on_delete=models.CASCADE)
    driver = models.ForeignKey('Driver', on_delete=models.CASCADE,null=True,blank=True)
    fuel_amount = models.DecimalField(max_digits=10, decimal_places=2)  # Cost of fuel
    fuel_liters = models.DecimalField(max_digits=8, decimal_places=2)   # Quantity of fuel in liters
    current_km = models.PositiveIntegerField()                          # Current odometer reading
    dashboard_photo = models.ImageField(upload_to='fuel/dashboard_photos/', blank=True, null=True)
    dispenser_photo = models.ImageField(upload_to='fuel/dispenser_photos/', blank=True, null=True)
    receipt_photo = models.ImageField(upload_to='fuel/receipt_photos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def fuel_efficiency(self):
        """Calculate fuel efficiency (KM per liter)"""
        if self.current_km and self.last_km and self.fuel_liters > 0:
            return (self.current_km - self.last_km) / self.fuel_liters
        return None

    def __str__(self):
        return f"{self.vehicle.vehicle_number} - {self.created_at}"