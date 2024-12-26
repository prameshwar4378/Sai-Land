from django import forms
from ERP_Admin.models import Policy
from django.core.exceptions import ValidationError

class PolicyForm(forms.ModelForm):
    class Meta:
        model = Policy
        fields = ['vehicle', 'policy_file', 'due_date']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_vehicle(self):
        vehicle = self.cleaned_data.get('vehicle')
        # Check if a policy already exists for the selected vehicle
        if Policy.objects.filter(vehicle=vehicle).exists():
            raise ValidationError(f"A policy for this vehicle already exists.")
        
        return vehicle