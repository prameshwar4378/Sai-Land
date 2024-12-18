from django_filters import FilterSet, ModelChoiceFilter, DateFilter
import django_filters
from django.forms import Select, DateInput
from ERP_Admin.models import *

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
        self.filters['start_date'].label = "Start Date - MM/DD/YYYY"
        self.filters['end_date'].label = "End Date - MM/DD/YYYY"

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
        self.filters['start_date'].label = "Start Date - MM/DD/YYYY"
        self.filters['end_date'].label = "End Date - MM/DD/YYYY"

    class Meta:
        model = Purchase
        fields = ['start_date', 'end_date', 'amount_less_than', 'amount_greater_than', 'bill_type', 'bill_no']

