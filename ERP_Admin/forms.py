# forms.py

from django import forms
from .models import Vehicle

from django.contrib.auth.forms import UserCreationForm
from .models import *

from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm
import re

        
class LoginForm(forms.Form):
    username = forms.CharField(label='Username')
    password = forms.CharField(widget=forms.PasswordInput, label='Password')
 
class UserRegistrationForm(UserCreationForm):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('account', 'Account'),
        ('workshop', 'Workshop'),
        ('finance', 'Finance'),
    ]
    
    role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.RadioSelect, label="Role")

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2', 'role','is_active']
 

    def clean_username(self):
        username = self.cleaned_data.get('username')
        user_id = self.instance.id  # Get the current user instance ID (if updating an existing user)
        if CustomUser.objects.filter(username=username).exclude(id=user_id).exists():
            raise ValidationError("A user with that username already exists.")
        return username

    def save(self, commit=True):
        user = super().save(commit=False)
        role = self.cleaned_data.get('role')

        # Reset all roles to False
        user.is_admin = False
        user.is_account = False
        user.is_workshop = False
        user.is_finance = False

        # Set the selected role to True
        if role == 'admin':
            user.is_admin = True
        elif role == 'account':
            user.is_account = True
        elif role == 'workshop':
            user.is_workshop = True
        elif role == 'finance':
            user.is_finance = True

        if commit:
            user.save()
        return user
    

class UpdatePasswordForm(forms.Form):
    new_password1 = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter new password'}),
        min_length=8
    )
    new_password2 = forms.CharField(
        label="Confirm New Password",
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm new password'}),
        min_length=8
    )

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("new_password1")
        password2 = cleaned_data.get("new_password2")

        # Check if the passwords match
        if password1 != password2:
            raise ValidationError("The two password fields must match.")
        return cleaned_data


class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['vehicle_number', 'vehicle_name']  # Fields to include in the form

    def clean_vehicle_number(self):
        vehicle_number = self.cleaned_data.get('vehicle_number') 
        vehicle_id = self.instance.id   
        if Vehicle.objects.filter(vehicle_number=vehicle_number).exclude(id=vehicle_id).exists():
            raise ValidationError("This Vehicle number is already registered.")
        return vehicle_number


class DriverRegistrationForm(UserCreationForm):
    driver_name = forms.CharField(max_length=20, required=True, label="Driver Name")
    adhaar_number = forms.CharField(max_length=20, required=True, label="Aadhaar Number", widget=forms.TextInput(attrs={'oninput': 'generate_username()',}))
    license_number = forms.CharField(max_length=20, required=True, label="License Number")
    mobile_number = forms.CharField(max_length=15, required=True, label="Mobile Number")
    alternate_mobile_number = forms.CharField(max_length=15, required=False, label="Alternate Mobile Number")
    adhaar_card_photo=forms.FileField(required=False, label="Upload Adhaar Card")
    pan_card_photo=forms.FileField(required=False, label="Upload Pan Card")
    driving_license_photo=forms.FileField(required=False, label="Upload Driving License")
    profile_photo=forms.ImageField(required=False, label="Upload Profile Photo")
    address = forms.CharField(widget=forms.Textarea, required=False, label="Address")
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=True,
        label="Date of Birth"
    )
    date_joined = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=True,
        label="Date Joined"
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2','is_active']
        widgets={ 
            'username': forms.TextInput(attrs={'readonly': True }), 
        }

    def clean_license_number(self):
        license_number = self.cleaned_data.get('license_number')
        if not re.match(r"^[A-Z0-9-]+$", license_number):
            raise ValidationError("License number can only contain letters, numbers, and hyphens.")
        if Driver.objects.filter(license_number=license_number).exists():
            raise ValidationError("This license number is already registered.")
        return license_number

    def clean_adhaar_number(self):
        adhaar_number = self.cleaned_data.get('adhaar_number')
        if not re.match(r"^\d{12}$", adhaar_number):  # Aadhaar must be 12 digits
            raise ValidationError("Aadhaar number must be a 12-digit number.")
        if Driver.objects.filter(adhaar_number=adhaar_number).exists():
            raise ValidationError("This Aadhaar number is already registered.")
        return adhaar_number

    def clean_mobile_number(self):
        mobile_number = self.cleaned_data.get('mobile_number')
        if not re.match(r"^\d{10}$", mobile_number):  # Validate exactly 10 digits
            raise ValidationError("mobile number must be 10 digits.")
        return mobile_number

    def clean_alternate_mobile_number(self):
        alternate_mobile_number = self.cleaned_data.get('alternate_mobile_number')
        if alternate_mobile_number:
            if not re.match(r"^\d{10}$", alternate_mobile_number):  # Validate exactly 10 digits
                raise ValidationError("Alternate mobile number must be 10 digits.")
        return alternate_mobile_number

    def save(self, commit=True):
        user = super().save(commit=False)
        last_emp_id = EMP_ID.objects.order_by('-id').first()
        if last_emp_id:
            last_number = int(last_emp_id.emp_id.split('-')[1])
            new_emp_id = EMP_ID.objects.create(emp_id=f"SLD-{last_number + 1}")
        else:
            new_emp_id = EMP_ID.objects.create(emp_id="SLD-1")
 
        if commit:
            fm=user
            fm.is_driver=True
            fm.emp_id=new_emp_id
            fm.save()
            Driver.objects.create(
                user=user, 
                driver_name=self.cleaned_data['driver_name'],
                adhaar_number=self.cleaned_data['adhaar_number'],
                license_number=self.cleaned_data['license_number'],
                mobile_number=self.cleaned_data['mobile_number'],
                alternate_mobile_number=self.cleaned_data['alternate_mobile_number'],
                address=self.cleaned_data.get('address'),
                date_of_birth=self.cleaned_data.get('date_of_birth'),
                date_joined=self.cleaned_data.get('date_joined'),
                adhaar_card_photo=self.cleaned_data.get('adhaar_card_photo'),
                pan_card_photo=self.cleaned_data.get('pan_card_photo'),
                driving_license_photo=self.cleaned_data.get('driving_license_photo'),
                profile_photo=self.cleaned_data.get('profile_photo')
            )
        return user
    


class DriverUpdateForm(forms.ModelForm):
    is_active = forms.BooleanField(
        required=False,
        label="Is Active for Login",
        initial=True  # Set default value
    )
    class Meta:
        model = Driver
        fields = [
            'driver_name',
            'license_number',
            'adhaar_number',
            'mobile_number',
            'alternate_mobile_number',
            'address',
            'date_of_birth',
            'date_joined',
            'adhaar_card_photo',
            'pan_card_photo',
            'driving_license_photo',
            'profile_photo'
        ]
        
        # You can customize field widgets if needed
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'date_joined': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 3, 'cols': 40}),
            'mobile_number': forms.TextInput(attrs={'pattern': '[0-9]{10}', 'maxlength': '15'}),
            'alternate_mobile_number': forms.TextInput(attrs={'pattern': '[0-9]{10}', 'maxlength': '15'}),
        }
     
        
        # Optional: Add some additional validation
        def clean_license_number(self):
            license_number = self.cleaned_data.get('license_number')
            if not re.match(r"^[A-Z0-9-]+$", license_number):
                raise ValidationError("License number can only contain letters, numbers, and hyphens.")
            if Driver.objects.filter(license_number=license_number).exists():
                raise ValidationError("This license number is already registered.")
            return license_number

        def clean_adhaar_number(self):
            adhaar_number = self.cleaned_data.get('adhaar_number')
            if not re.match(r"^\d{12}$", adhaar_number):  # Aadhaar must be 12 digits
                raise ValidationError("Aadhaar number must be a 12-digit number.")
            if Driver.objects.filter(adhaar_number=adhaar_number).exists():
                raise ValidationError("This Aadhaar number is already registered.")
            return adhaar_number

        def clean_mobile_number(self):
            mobile_number = self.cleaned_data.get('mobile_number')
            if len(mobile_number) != 10:
                raise forms.ValidationError("Mobile number must be exactly 10 digits.")
            return mobile_number

        def clean_alternate_mobile_number(self):
            alternate_mobile_number = self.cleaned_data.get('alternate_mobile_number')
            if alternate_mobile_number and len(alternate_mobile_number) != 10:
                raise forms.ValidationError("Alternate mobile number must be exactly 10 digits.")
            return alternate_mobile_number
     

class TechnicianRegistrationForm(forms.ModelForm):
    pan_card=forms.FileField(required=False, label="Upload Pan Card")
    adhaar_card=forms.FileField(required=False, label="Upload Adhaar Card")
    profile_photo=forms.FileField(required=False, label="Upload Profile Photo")
    additional_docs=forms.FileField(required=False, label="Upload Additional Document")

    technician_name = forms.CharField(
        max_length=100, 
        required=True, 
        label="Technician Name",
            )
    adhaar_number = forms.CharField(
        max_length=12, 
        required=True, 
        label="Aadhaar Number", 
            )
    mobile_number = forms.CharField(
        max_length=10, 
        required=True, 
        label="Mobile Number", 
     )
    alternate_mobile_number = forms.CharField(
        max_length=10, 
        required=False,  # This line makes the field optional
        label="Alternate Mobile Number",
    )
    email = forms.EmailField(
        required=False, 
        label="Email Address", 
            )
    address = forms.CharField(
        required=False, 
        label="Address", 
            )
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False, 
        label="Date of Birth", 
            )

    class Meta:
        model = Technician
        fields = [
            'technician_name',
            'adhaar_number',
            'mobile_number',
            'alternate_mobile_number',
            'email',
            'address',
            'date_of_birth',
            'pan_card',
            'adhaar_card',
            'profile_photo',
            'additional_docs',
        ]  
        
    def clean_adhaar_number(self):
        adhaar_number = self.cleaned_data.get('adhaar_number')
        if not re.match(r"^\d{12}$", adhaar_number):  # Aadhaar must be 12 digits
            raise ValidationError("Aadhaar number must be a 12-digit number.") 
        return adhaar_number

    def clean_mobile_number(self):
        mobile_number = self.cleaned_data.get('mobile_number')
        if not re.match(r"^\d{10}$", mobile_number):  # Validate exactly 10 digits
            raise ValidationError("Mobile number must be 10 digits.") 
        return mobile_number

    def clean_alternate_mobile_number(self):
        alternate_mobile_number = self.cleaned_data.get('alternate_mobile_number')
        if not alternate_mobile_number:
            return None
        elif not re.match(r"^\d{10}$", alternate_mobile_number):  # Validate exactly 10 digits
            raise ValidationError("Alternate mobile number must be 10 digits.")
        return alternate_mobile_number
 
  
    def save(self, commit=True):
        technician = super().save(commit=False)
        if commit:
            technician.save()
        return technician


class TechnicianUpdateForm(forms.ModelForm):
    class Meta:
        model = Technician
        fields = [
            'technician_name',
            'adhaar_number',
            'mobile_number',
            'alternate_mobile_number',
            'email',
            'address',
            'date_of_birth',
            'pan_card',
            'adhaar_card',
            'profile_photo',
            'additional_docs',
        ]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # If needed, you can customize field widgets or add attributes here

    def clean_mobile_number(self):
        mobile_number = self.cleaned_data.get('mobile_number')
        if len(mobile_number) != 10 or not mobile_number.isdigit():
            raise forms.ValidationError("Mobile number must be 10 digits.")
        return mobile_number

    def clean_adhaar_number(self):
        adhaar_number = self.cleaned_data.get('adhaar_number')
        if len(adhaar_number) != 12 or not adhaar_number.isdigit():
            raise forms.ValidationError("Aadhaar number must be 12 digits.")
        return adhaar_number

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and Technician.objects.filter(email=email).exclude(id=self.instance.id).exists():
            raise forms.ValidationError("This email is already registered with another technician.")
        return email


class PartyForm(forms.ModelForm):
    class Meta:
        model = Party
        fields = '__all__'
 
    def clean_mobile_number(self):
        mobile_number = self.cleaned_data['mobile_number']
        if len(mobile_number) != 10:
            raise forms.ValidationError("Mobile number must be 10 digits.")
        return mobile_number

    def clean_alternate_mobile_number(self):
        alternate_mobile_number = self.cleaned_data['alternate_mobile_number']
        if alternate_mobile_number:
            if len(alternate_mobile_number) != 10:
                raise forms.ValidationError("Alternate mobile number must be 10 digits.")
        return alternate_mobile_number

class PartyUpdateForm(forms.ModelForm):
    class Meta:
        model = Party
        fields = [
            'business_name',
            'customer_name',
            'gst_number',
            'mobile_number',
            'alternate_mobile_number',
            'address',
            'document1',
            'document2',
            'document3'
        ]
    
    def clean_mobile_number(self):
        mobile_number = self.cleaned_data.get('mobile_number')
        if Party.objects.filter(mobile_number=mobile_number).exclude(id=self.instance.id).exists():
            raise forms.ValidationError("This mobile number is already registered with another party.")
        return mobile_number

    def clean_gst_number(self):
        gst_number = self.cleaned_data.get('gst_number')
        if gst_number and Party.objects.filter(gst_number=gst_number).exclude(id=self.instance.id).exists():
            raise forms.ValidationError("This GST number is already registered with another party.")
        return gst_number
