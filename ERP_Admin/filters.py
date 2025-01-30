from django_filters import FilterSet, ModelChoiceFilter, DateFilter
import django_filters
from django.forms import Select, DateInput
from ERP_Admin.models import *
from django.db.models import Sum, F, Q


class JobCardFilter(django_filters.FilterSet):
    start_date = django_filters.DateFilter(
        field_name='date',
        lookup_expr='gte',
        widget=DateInput(attrs={'type': 'date'}),
        label='Start Date'
    )
    end_date = django_filters.DateFilter(
        field_name='date',
        lookup_expr='lte',
        widget=DateInput(attrs={'type': 'date'}),
        label='End Date'
    )
    # Technician dropdown
    technician = ModelChoiceFilter(
        queryset=Technician.objects.all(),  # Fetch all technicians
        field_name='technician',  # Related field
        widget=Select(attrs={'class': 'form-control','id':'filter_technician'}),
        label='Technician'
    )
    # Driver dropdown
    driver = ModelChoiceFilter(
        queryset=Driver.objects.all(),  # Fetch all drivers
        field_name='driver',  # Related field
        widget=Select(attrs={'class': 'form-control','id':'filter_driver'}),
        label='Driver'
    )
    # Party dropdown
    party = ModelChoiceFilter(
        queryset=Party.objects.all(),  # Fetch all parties
        field_name='party',  # Related field
        widget=Select(attrs={'class': 'form-control','id':'filter_party'}),
        label='Party'
    )
    # Vehicle dropdown
    vehicle = ModelChoiceFilter(
        queryset=Vehicle.objects.all(),  # Fetch all vehicles
        field_name='vehicle',  # Related field
        widget=Select(attrs={'class': 'form-control','id':'filter_vehicle'}),
        label='Vehicle Registration Number'
    )

    def __init__(self, *args, **kwargs):
        super(JobCardFilter, self).__init__(*args, **kwargs)
        self.filters['start_date'].label = "Start Date"
        self.filters['end_date'].label = "End Date"
 
    class Meta:
        model = JobCard
        fields = ['start_date', 'end_date', 'technician', 'party', 'vehicle', 'driver','job_card_number','status']


 
class PurchaseFilter(django_filters.FilterSet):
    start_date = django_filters.DateFilter(
        field_name='bill_date',
        lookup_expr='gte',
        widget=DateInput(attrs={'type': 'date'}),
        label='Start Date'
    )
    end_date = django_filters.DateFilter(
        field_name='bill_date',
        lookup_expr='lte',
        widget=DateInput(attrs={'type': 'date'}),
        label='End Date'
    )
    amount_less_than = django_filters.NumberFilter(
        field_name='total_cost',
        lookup_expr='lte',
        label='Amount Less Than'
    )
    
    amount_greater_than = django_filters.NumberFilter(
        field_name='total_cost',
        lookup_expr='gte',
        label='Amount Greater Than'
    )
    

    def __init__(self, *args, **kwargs):
        super(PurchaseFilter, self).__init__(*args, **kwargs)
        self.filters['start_date'].label = "Start Date"
        self.filters['end_date'].label = "End Date"

    class Meta:
        model = Purchase
        fields = ['start_date', 'end_date', 'amount_less_than', 'amount_greater_than', 'bill_type', 'bill_no']












class EMIFilter(django_filters.FilterSet):
    # Filtering options
    loan_amount_gte = django_filters.NumberFilter(field_name="loan_amount", lookup_expr="gte", label="Loan Amount (≥)")
    loan_amount_lte = django_filters.NumberFilter(field_name="loan_amount", lookup_expr="lte", label="Loan Amount (≤)")
    next_due_date_gte = django_filters.DateFilter(field_name="next_due_date", lookup_expr="gte", label="Next Due Date (From)",widget=DateInput(attrs={'type': 'date'}),)
    next_due_date_lte = django_filters.DateFilter(field_name="next_due_date", lookup_expr="lte", label="Next Due Date (To)",widget=DateInput(attrs={'type': 'date'}), )
    frequency = django_filters.ChoiceFilter(field_name="frequency", choices=FREQUENCY_CHOICES, label="Frequency")
    status = django_filters.ChoiceFilter(field_name="status", choices=EMI_STATUS_CHOICES, label="Status")
    vehicle = django_filters.CharFilter(field_name="vehicle__vehicle_number", lookup_expr="icontains", label="Vehicle")


    def __init__(self, *args, **kwargs):
        super(EMIFilter, self).__init__(*args, **kwargs)
        self.filters['loan_amount_gte']
        self.filters['loan_amount_lte']
        self.filters['next_due_date_gte']
        self.filters['next_due_date_lte']


    class Meta:
        model = EMI
        fields = [
            "vehicle", "loan_amount", "loan_amount_gte", "loan_amount_lte",
            "next_due_date_gte", "next_due_date_lte", "frequency", "status"
        ]

from django import forms
 
class VehicleFilterForFinance(forms.Form):
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False,
        label="Start Date"
    )
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False,
        label="End Date"
    )

  

class EnquiryFilter(django_filters.FilterSet):
    start_date = django_filters.DateFilter(
        field_name='date',
        lookup_expr='gte',
        widget=DateInput(attrs={'type': 'date'}),
        label='Start Date'
    )
    end_date = django_filters.DateFilter(
        field_name='date',
        lookup_expr='lte',
        widget=DateInput(attrs={'type': 'date'}),
        label='End Date'
    ) 

    def __init__(self, *args, **kwargs):
        super(EnquiryFilter, self).__init__(*args, **kwargs)
        self.filters['start_date'].label = "Start Date"
        self.filters['end_date'].label = "End Date"

    class Meta:
        model = Enquiry
        fields = ['start_date', 'end_date']




