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



 
class ProductFilter(django_filters.FilterSet):
    product_code = django_filters.CharFilter(field_name='product_code', lookup_expr='icontains', label='Product Code')
    product_name = django_filters.CharFilter(field_name='product_name', lookup_expr='icontains', label='Product Name')
    model = django_filters.ModelChoiceFilter(queryset=VehicleModel.objects.all(), label='Model')
    # For filtering stock
    minimum_stock_alert = django_filters.ChoiceFilter(
        choices=[('1', 'Less than Minimum Stock Alert'), ('2', 'Out of Stock'), ('3', 'Available Stock')], 
        label='Stock Status',
        method='filter_stock'
    )

    class Meta:
        model = Product
        fields = ['product_code', 'product_name', 'model', 'minimum_stock_alert']

    def filter_stock(self, queryset, name, value):
        if value == '1':  # Less than Minimum Stock Alert
            return queryset.filter(available_stock__lt=models.F('minimum_stock_alert'),available_stock__gt=0)
        elif value == '2':  # Out of Stock
            return queryset.filter(available_stock__lt=1)
        elif value == '3':  # Available Stock > Minimum Stock Alert
            return queryset.filter(available_stock__gt=models.F('minimum_stock_alert'))
        return queryset

 
class BreakdownFilter(django_filters.FilterSet): 
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
    class Meta:
        model = Breakdown
        fields = ['start_date','end_date','is_resolved',] 