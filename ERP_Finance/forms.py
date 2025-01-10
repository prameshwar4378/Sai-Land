from django import forms
from ERP_Admin.models import Policy,EMI,EMI_Item,Insurance_Bank,Finance_Bank,OtherDues
from django.core.exceptions import ValidationError
from datetime import date


class PolicyForm(forms.ModelForm):
    class Meta:
        model = Policy
        fields = ['policy_number', 'vehicle', 'policy_file', 'due_date']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_vehicle(self):
        vehicle = self.cleaned_data.get('vehicle')
        # Exclude the current instance (if it exists) from the query
        if Policy.objects.filter(vehicle=vehicle).exclude(pk=self.instance.pk).exists():
            raise ValidationError(f"A policy for this vehicle already exists.")
        return vehicle
    

class EMIForm(forms.ModelForm):
    class Meta:
        model = EMI
        fields = ['vehicle', 'finance_bank','loan_account_no', 'loan_amount', 'total_installments', 'paid_installments', 'next_due_date', 'file','frequency','status']
        widgets = {
            'next_due_date': forms.DateInput(attrs={'type': 'date'}),
            'loan_amount': forms.NumberInput(attrs={'placeholder': 'Enter Loan Amount'}),
            'total_installments': forms.NumberInput(attrs={'placeholder': 'Total Installments'}),
            'paid_installments': forms.NumberInput(attrs={'placeholder': 'Paid Installments'}),
            'file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def clean_next_due_date(self):
        next_due_date = self.cleaned_data.get('next_due_date')
        if next_due_date:
            # Ensure that the next_due_date is a future date
            if next_due_date <= date.today():
                raise ValidationError("The due date cannot be in the past. Please enter a future date.")
        return next_due_date
    
    def clean(self):
        cleaned_data = super().clean()
        vehicle = cleaned_data.get('vehicle')

        # Check if a record for the same vehicle already exists only when creating a new record
        if not self.instance.pk and vehicle and EMI.objects.filter(vehicle=vehicle).exists():
            raise ValidationError({'vehicle': "A record for this vehicle already exists."})
        return cleaned_data
        

class EMIItemForm(forms.ModelForm):
    next_due_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=True, 
        label="Next Due Date", 
            )

    class Meta:
        model = EMI_Item
        fields = ['installment_amount', 'principal', 'interest', 'outstanding_principal','installment_date']
        widgets = {
            'installment_date': forms.DateInput(attrs={'type': 'date'}), 
        }

    def clean_next_due_date(self):
        next_due_date = self.cleaned_data.get('next_due_date')
        if next_due_date:
            if next_due_date <= date.today():
                raise ValidationError("The due date cannot be in the past. Please enter a future date.")
        return next_due_date
    
 


class OtherDuesForm(forms.ModelForm):
    class Meta:
        model =  OtherDues
        fields = [ 
            'tax_frequency', 
            'tax_amount', 
            'tax_due_date',  
            'fitness_due_date', 
            'permit_due_date', 
            'puc_due_date'
        ]
        widgets = {
            'tax_due_date': forms.DateInput(attrs={'type': 'date'}), 
            'fitness_due_date': forms.DateInput(attrs={'type': 'date'}), 
            'permit_due_date': forms.DateInput(attrs={'type': 'date'}), 
            'puc_due_date': forms.DateInput(attrs={'type': 'date'}), 
        }
    def clean(self):
        cleaned_data = super().clean()

        # List of fields to validate for future dates
        date_fields = [
            'tax_due_date',
            'fitness_due_date',
            'permit_due_date',
            'puc_due_date'
        ]

        for field in date_fields:
            value = cleaned_data.get(field)
            if value and value < date.today():
                raise ValidationError({field: f'{field.replace("_", " ").title()} must be in the future.'})

        return cleaned_data
    


class InsuranceBankForm(forms.ModelForm):
    class Meta:
        model = Insurance_Bank
        fields = ['bank_name']

class FinanceBankForm(forms.ModelForm):
    class Meta:
        model = Finance_Bank
        fields = ['bank_name']
