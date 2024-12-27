from django import forms
from ERP_Admin.models import Policy,EMI,EMI_Item
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
        fields = ['vehicle', 'loan_amount', 'total_installments', 'paid_installments', 'next_due_date', 'file','frequency','status']
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