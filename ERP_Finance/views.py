from django.shortcuts import render,get_object_or_404,redirect
from ERP_Admin.models import Policy,EMI,EMI_Item,Vehicle,Insurance_Bank,Finance_Bank,EMI_Installment,Purchase,Product,PurchaseItem
from .forms import *
from django.http import JsonResponse
from django.contrib import messages
from django.core.paginator import Paginator
from datetime import date
from ERP_Admin.filters import EMIFilter,PurchaseFilter
from django.db.models import Sum, F, Q
from django.db.models import Count, Case, When, F, IntegerField,ExpressionWrapper
from django.utils import timezone
from datetime import timedelta 
from collections import Counter
from ERP_Admin.filters import VehicleFilterForFinance
from functools import wraps

from ERP_Admin.views import send_email_in_background
from django.conf import settings
import threading
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

def finance_required(function):
    @wraps(function)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/login')  # Redirect to login if not logged in
        if not request.user.is_finance:
            return redirect('/login')  # Redirect to login if user is not in Finance role
        return function(request, *args, **kwargs)
    return _wrapped_view


def daily_reminder_mail(request):
    # Prepare the subject
    email_subject = "Finance Department Daily Reminder Report"
    current_datetime = datetime.now()

    today = date.today()
    three_days_later = today + timedelta(days=3)
    # Query the different dues in the next 2 days
    emi_dues = EMI.objects.filter(next_due_date__range=[today, three_days_later], vehicle__status="active", status='pending').values('vehicle__id', 'vehicle__vehicle_number', 'next_due_date')
    policy_dues = Policy.objects.filter(due_date__range=[today, three_days_later], vehicle__status="active").values('vehicle__id', 'vehicle__vehicle_number', 'due_date')
    tax_dues = OtherDues.objects.filter(tax_due_date__range=[today, three_days_later], vehicle__status="active").values('vehicle__id', 'vehicle__vehicle_number', 'tax_due_date')
    fitness_dues = OtherDues.objects.filter(fitness_due_date__range=[today, three_days_later], vehicle__status="active").values('vehicle__id', 'vehicle__vehicle_number', 'fitness_due_date')
    permit_dues = OtherDues.objects.filter(permit_due_date__range=[today, three_days_later], vehicle__status="active").values('vehicle__id', 'vehicle__vehicle_number', 'permit_due_date')
    puc_dues = OtherDues.objects.filter(puc_due_date__range=[today, three_days_later], vehicle__status="active").values('vehicle__id', 'vehicle__vehicle_number', 'puc_due_date')

    # Add the due type as a custom field for each query result
    emi_dues_2 = [{'vehicle_id': due['vehicle__id'], 'vehicle_number': due['vehicle__vehicle_number'], 'due_date': due['next_due_date'], 'due_name': 'EMI'} for due in emi_dues]
    policy_dues_2 = [{'vehicle_id': due['vehicle__id'], 'vehicle_number': due['vehicle__vehicle_number'], 'due_date': due['due_date'], 'due_name': 'Policy'} for due in policy_dues]
    tax_dues_2 = [{'vehicle_id': due['vehicle__id'], 'vehicle_number': due['vehicle__vehicle_number'], 'due_date': due['tax_due_date'], 'due_name': 'Tax'} for due in tax_dues]
    fitness_dues_2 = [{'vehicle_id': due['vehicle__id'], 'vehicle_number': due['vehicle__vehicle_number'], 'due_date': due['fitness_due_date'], 'due_name': 'Fitness'} for due in fitness_dues]
    permit_dues_2 = [{'vehicle_id': due['vehicle__id'], 'vehicle_number': due['vehicle__vehicle_number'], 'due_date': due['permit_due_date'], 'due_name': 'Permit'} for due in permit_dues]
    puc_dues_2 = [{'vehicle_id': due['vehicle__id'], 'vehicle_number': due['vehicle__vehicle_number'], 'due_date': due['puc_due_date'], 'due_name': 'PUC'} for due in puc_dues]

    # Combine all dues data
    three_days_later_dues = emi_dues_2 + policy_dues_2 + tax_dues_2 + fitness_dues_2 + permit_dues_2 + puc_dues_2
 
    twelve_months_ago = today - timedelta(days=365)
    one_days_ago = today - timedelta(days=1)

    emi_dues = EMI.objects.filter(next_due_date__range=[twelve_months_ago, one_days_ago], vehicle__status="active", status='pending').values('vehicle__id', 'vehicle__vehicle_number', 'next_due_date')
    policy_dues = Policy.objects.filter(due_date__range=[twelve_months_ago, one_days_ago], vehicle__status="active").values('vehicle__id', 'vehicle__vehicle_number', 'due_date')
    tax_dues = OtherDues.objects.filter(tax_due_date__range=[twelve_months_ago, one_days_ago], vehicle__status="active").values('vehicle__id', 'vehicle__vehicle_number', 'tax_due_date')
    fitness_dues = OtherDues.objects.filter(fitness_due_date__range=[twelve_months_ago, one_days_ago], vehicle__status="active").values('vehicle__id', 'vehicle__vehicle_number', 'fitness_due_date')
    permit_dues = OtherDues.objects.filter(permit_due_date__range=[twelve_months_ago, one_days_ago], vehicle__status="active").values('vehicle__id', 'vehicle__vehicle_number', 'permit_due_date')
    puc_dues = OtherDues.objects.filter(puc_due_date__range=[twelve_months_ago, one_days_ago], vehicle__status="active").values('vehicle__id', 'vehicle__vehicle_number', 'puc_due_date')


    emi_dues = [{'vehicle_id': due['vehicle__id'], 'vehicle_number': due['vehicle__vehicle_number'], 'due_date': due['next_due_date'], 'due_name': 'EMI'} for due in emi_dues]
    policy_dues = [{'vehicle_id': due['vehicle__id'], 'vehicle_number': due['vehicle__vehicle_number'], 'due_date': due['due_date'], 'due_name': 'Policy'} for due in policy_dues]
    tax_dues = [{'vehicle_id': due['vehicle__id'], 'vehicle_number': due['vehicle__vehicle_number'], 'due_date': due['tax_due_date'], 'due_name': 'Tax'} for due in tax_dues]
    fitness_dues = [{'vehicle_id': due['vehicle__id'], 'vehicle_number': due['vehicle__vehicle_number'], 'due_date': due['fitness_due_date'], 'due_name': 'Fitness'} for due in fitness_dues]
    permit_dues = [{'vehicle_id': due['vehicle__id'], 'vehicle_number': due['vehicle__vehicle_number'], 'due_date': due['permit_due_date'], 'due_name': 'Permit'} for due in permit_dues]
    puc_dues = [{'vehicle_id': due['vehicle__id'], 'vehicle_number': due['vehicle__vehicle_number'], 'due_date': due['puc_due_date'], 'due_name': 'PUC'} for due in puc_dues]

    # Combine all dues data
    expire_dues = emi_dues + policy_dues + tax_dues + fitness_dues + permit_dues + puc_dues
      
    
    email_body = render_to_string('finance_daily_reminder_email.html', {
        # Add any dynamic context here, for example:
        'expire_dues': expire_dues,
        'three_days_later_dues':three_days_later_dues,
        'current_datetime':current_datetime
    })

    # Configure the email
    email_message = EmailMessage(
        subject=email_subject,
        body=email_body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=['prameshwar4378@gmail.com'],  # Replace with the appropriate email address
    )
    
    # Set the email content type to HTML
    email_message.content_subtype = 'html'

    # Send the email in a background thread to avoid blocking the request
    email_thread = threading.Thread(target=send_email_in_background, args=(email_message,))
    email_thread.start()

    # Redirect after sending the email
    return redirect('/finance/dashboard/')


@finance_required 
def dashboard(request):
    today = date.today()
    thirty_days_date = today + timedelta(days=30)

    thirty_days_record = {
        'policy_dues': Policy.objects.filter(due_date__range=[today, thirty_days_date], vehicle__status='active'),
        'emi_dues': EMI.objects.filter(next_due_date__range=[today, thirty_days_date], status='pending', vehicle__status='active'),
        'tax_dues': OtherDues.objects.filter(tax_due_date__range=[today, thirty_days_date], vehicle__status='active'),
        'fitness_dues': OtherDues.objects.filter(fitness_due_date__range=[today, thirty_days_date], vehicle__status='active'),
        'permit_dues': OtherDues.objects.filter(permit_due_date__range=[today, thirty_days_date], vehicle__status='active'),
        'puc_dues': OtherDues.objects.filter(puc_due_date__range=[today, thirty_days_date], vehicle__status='active'),
    }
 
    # Count the records
    thirty_days_counts = {
        "policy_dues": thirty_days_record["policy_dues"].count(),
        "emi_dues": thirty_days_record["emi_dues"].count(),
        "tax_dues": thirty_days_record["tax_dues"].count(),
        "fitness_dues": thirty_days_record["fitness_dues"].count(),
        "permit_dues": thirty_days_record["permit_dues"].count(),
        "puc_dues": thirty_days_record["puc_dues"].count(),
    }
  
    # Count individual dues for upcoming and past
    expire_dues_counts = Counter({
        "policy_dues": Policy.objects.filter(due_date__lt=today,due_date__isnull=False,vehicle__status='active').count(),
        "emi_dues": EMI.objects.filter(next_due_date__lt=today,next_due_date__isnull=False, status='pending', vehicle__status='active').count(),
        "tax_dues": OtherDues.objects.filter(tax_due_date__lt=today,tax_due_date__isnull=False,vehicle__status='active').count(),
        "fitness_dues": OtherDues.objects.filter(fitness_due_date__lt=today,fitness_due_date__isnull=False,vehicle__status='active').count(),
        "permit_dues": OtherDues.objects.filter(permit_due_date__lt=today,permit_due_date__isnull=False,vehicle__status='active').count(),
        "puc_dues": OtherDues.objects.filter(puc_due_date__lt=today,puc_due_date__isnull=False,vehicle__status='active').count(),
    })

    three_days_later = today + timedelta(days=3)
    # Query the different dues in the next 2 days
    emi_dues = EMI.objects.filter(next_due_date__range=[today, three_days_later],vehicle__status='active', status='pending').values('vehicle__id', 'vehicle__vehicle_number', 'next_due_date')
    policy_dues = Policy.objects.filter(due_date__range=[today, three_days_later],vehicle__status='active').values('vehicle__id', 'vehicle__vehicle_number', 'due_date')
    tax_dues = OtherDues.objects.filter(tax_due_date__range=[today, three_days_later],vehicle__status='active').values('vehicle__id', 'vehicle__vehicle_number', 'tax_due_date')
    fitness_dues = OtherDues.objects.filter(fitness_due_date__range=[today, three_days_later],vehicle__status='active').values('vehicle__id', 'vehicle__vehicle_number', 'fitness_due_date')
    permit_dues = OtherDues.objects.filter(permit_due_date__range=[today, three_days_later],vehicle__status='active').values('vehicle__id', 'vehicle__vehicle_number', 'permit_due_date')
    puc_dues = OtherDues.objects.filter(puc_due_date__range=[today, three_days_later],vehicle__status='active').values('vehicle__id', 'vehicle__vehicle_number', 'puc_due_date')

    # Add the due type as a custom field for each query result
    emi_dues_2 = [{'vehicle_id': due['vehicle__id'], 'vehicle_number': due['vehicle__vehicle_number'], 'due_date': due['next_due_date'], 'due_name': 'EMI'} for due in emi_dues]
    policy_dues_2 = [{'vehicle_id': due['vehicle__id'], 'vehicle_number': due['vehicle__vehicle_number'], 'due_date': due['due_date'], 'due_name': 'Policy'} for due in policy_dues]
    tax_dues_2 = [{'vehicle_id': due['vehicle__id'], 'vehicle_number': due['vehicle__vehicle_number'], 'due_date': due['tax_due_date'], 'due_name': 'Tax'} for due in tax_dues]
    fitness_dues_2 = [{'vehicle_id': due['vehicle__id'], 'vehicle_number': due['vehicle__vehicle_number'], 'due_date': due['fitness_due_date'], 'due_name': 'Fitness'} for due in fitness_dues]
    permit_dues_2 = [{'vehicle_id': due['vehicle__id'], 'vehicle_number': due['vehicle__vehicle_number'], 'due_date': due['permit_due_date'], 'due_name': 'Permit'} for due in permit_dues]
    puc_dues_2 = [{'vehicle_id': due['vehicle__id'], 'vehicle_number': due['vehicle__vehicle_number'], 'due_date': due['puc_due_date'], 'due_name': 'PUC'} for due in puc_dues]

    # Combine all dues data
    three_days_later_dues = emi_dues_2 + policy_dues_2 + tax_dues_2 + fitness_dues_2 + permit_dues_2 + puc_dues_2
 
    fifteen_days_ago = today - timedelta(days=15)
    one_days_ago = today - timedelta(days=1)

    emi_dues = EMI.objects.filter(next_due_date__range=[fifteen_days_ago, one_days_ago],vehicle__status='active', status='pending').values('vehicle__id', 'vehicle__vehicle_number', 'next_due_date')
    policy_dues = Policy.objects.filter(due_date__range=[fifteen_days_ago, one_days_ago],vehicle__status='active').values('vehicle__id', 'vehicle__vehicle_number', 'due_date')
    tax_dues = OtherDues.objects.filter(tax_due_date__range=[fifteen_days_ago, one_days_ago],vehicle__status='active').values('vehicle__id', 'vehicle__vehicle_number', 'tax_due_date')
    fitness_dues = OtherDues.objects.filter(fitness_due_date__range=[fifteen_days_ago, one_days_ago],vehicle__status='active').values('vehicle__id', 'vehicle__vehicle_number', 'fitness_due_date')
    permit_dues = OtherDues.objects.filter(permit_due_date__range=[fifteen_days_ago, one_days_ago],vehicle__status='active').values('vehicle__id', 'vehicle__vehicle_number', 'permit_due_date')
    puc_dues = OtherDues.objects.filter(puc_due_date__range=[fifteen_days_ago, one_days_ago],vehicle__status='active').values('vehicle__id', 'vehicle__vehicle_number', 'puc_due_date')


    emi_dues = [{'vehicle_id': due['vehicle__id'], 'vehicle_number': due['vehicle__vehicle_number'], 'due_date': due['next_due_date'], 'due_name': 'EMI'} for due in emi_dues]
    policy_dues = [{'vehicle_id': due['vehicle__id'], 'vehicle_number': due['vehicle__vehicle_number'], 'due_date': due['due_date'], 'due_name': 'Policy'} for due in policy_dues]
    tax_dues = [{'vehicle_id': due['vehicle__id'], 'vehicle_number': due['vehicle__vehicle_number'], 'due_date': due['tax_due_date'], 'due_name': 'Tax'} for due in tax_dues]
    fitness_dues = [{'vehicle_id': due['vehicle__id'], 'vehicle_number': due['vehicle__vehicle_number'], 'due_date': due['fitness_due_date'], 'due_name': 'Fitness'} for due in fitness_dues]
    permit_dues = [{'vehicle_id': due['vehicle__id'], 'vehicle_number': due['vehicle__vehicle_number'], 'due_date': due['permit_due_date'], 'due_name': 'Permit'} for due in permit_dues]
    puc_dues = [{'vehicle_id': due['vehicle__id'], 'vehicle_number': due['vehicle__vehicle_number'], 'due_date': due['puc_due_date'], 'due_name': 'PUC'} for due in puc_dues]

    # Combine all dues data
    fifteen_days_ago_expire_dues = emi_dues + policy_dues + tax_dues + fitness_dues + permit_dues + puc_dues
  
    # Pass data to template
    return render(request, 'finance_dashboard.html', { 
        'thirty_days_counts':thirty_days_counts,
        'thirty_days_records':thirty_days_record,
        'expire_dues_counts':expire_dues_counts,
        'three_days_later_dues':three_days_later_dues,
        'fifteen_days_ago_expire_dues':fifteen_days_ago_expire_dues
    })
 

 
@finance_required 
def vehicle_list(request):
    # Instantiate the filter form
    filter_form = VehicleFilterForFinance(request.GET or None)
    queryset = Vehicle.objects.all()

    # Initialize filters
    start_date = filter_form.cleaned_data.get('start_date') if filter_form.is_valid() else None
    end_date = filter_form.cleaned_data.get('end_date') if filter_form.is_valid() else None

    # Prepare the context
    context = []
    for vehicle in queryset:
        # Get related data for each vehicle
        policies = vehicle.policies.all()
        emis = vehicle.emis.all()
        other_dues = vehicle.otherdues_set.first()   

        # Extract relevant due dates
        policy_due_date = policies[0].due_date if policies else None
        emi_due_date = emis[0].next_due_date if emis else None
        tax_due_date = other_dues.tax_due_date if other_dues else None
        fitness_due_date = other_dues.fitness_due_date if other_dues else None
        permit_due_date = other_dues.permit_due_date if other_dues else None
        puc_due_date = other_dues.puc_due_date if other_dues else None

        # Apply date filtering
        if start_date and not end_date:
            # Only dates greater than or equal to start_date
            if not (
                (policy_due_date and policy_due_date >= start_date) or
                (emi_due_date and emi_due_date >= start_date) or 
                (tax_due_date and tax_due_date >= start_date) or
                (fitness_due_date and fitness_due_date >= start_date) or
                (permit_due_date and permit_due_date >= start_date) or
                (puc_due_date and puc_due_date >= start_date)
            ):
                continue  # Skip vehicles that don't match the filter
        elif end_date and not start_date:
            # Only dates less than or equal to end_date
            if not (
                (policy_due_date and policy_due_date <= end_date) or
                (emi_due_date and emi_due_date <= end_date) or 
                (tax_due_date and tax_due_date <= end_date) or
                (fitness_due_date and fitness_due_date <= end_date) or
                (permit_due_date and permit_due_date <= end_date) or
                (puc_due_date and puc_due_date <= end_date)
            ):
                continue  # Skip vehicles that don't match the filter
        elif start_date and end_date:
            # Dates within the range of start_date and end_date
            if not (
                (policy_due_date and start_date <= policy_due_date <= end_date) or
                (emi_due_date and start_date <= emi_due_date <= end_date) or 
                (tax_due_date and start_date <= tax_due_date <= end_date) or
                (fitness_due_date and start_date <= fitness_due_date <= end_date) or
                (permit_due_date and start_date <= permit_due_date <= end_date) or
                (puc_due_date and start_date <= puc_due_date <= end_date)
            ):
                continue  # Skip vehicles that don't match the filter

        # Add vehicle info to the context
        context.append({
            'id': vehicle.id,
            'vehicle_number': vehicle.vehicle_number,
            'policy_due_date': policy_due_date,
            'emi_due_date': emi_due_date, 
            'tax_due_date': tax_due_date,
            'fitness_due_date': fitness_due_date,
            'permit_due_date': permit_due_date,
            'puc_due_date': puc_due_date,
        })

    # Render the template with the filter form and context
    return render(request, 'finance_vehicle_list.html', {
        'filter_form': filter_form,
        'context': context
    })




# View for the EMI section
@finance_required 
def vehicle_dashboard(request,id):
    emi_form=EMIForm()
    policy_form=PolicyForm()

    vehicle = Vehicle.objects.all() or None
    vehicle = Vehicle.objects.get(id=id)
    other_dues_data=OtherDues.objects.filter(vehicle=vehicle) 

    other_dues=OtherDues.objects.filter(vehicle=vehicle).first() 
    other_dues_id=0
    if other_dues:
        other_dues_id=other_dues.id 

    is_data_exist=other_dues_data.exists()

    emi=EMI.objects.filter(vehicle=vehicle).first() 

    policy=Policy.objects.filter(vehicle=vehicle).first()


    form=OtherDuesForm() 
    context={
        'vehicle_id':id,
        'other_dues_id':other_dues_id,
        'other_dues':other_dues,
        'vehicle':vehicle,
        'form':form,
        'emi_form':emi_form,
        'policy_form':policy_form,
        'is_data_exist':is_data_exist,
        'emi':emi,
        'policy':policy, 
    }
    return render(request, 'finance_vehicle_dashboard.html',context)



def create_other_dues(request):
    if request.method == 'POST':
        form = OtherDuesForm(request.POST, request.FILES)

        if form.is_valid():
            try:
                vehicle_id=request.POST.get('vehicle_id') 

                vehicle=Vehicle.objects.get(id=vehicle_id)
                if vehicle and OtherDues.objects.filter(vehicle=vehicle).exists(): 
                    return JsonResponse({'success': False, 'errors': {'non_field_errors': "A record for this vehicle already exists."}}, status=400)
                
                fm=form.save(commit=False)
                fm.vehicle=vehicle
                fm.save()
                messages.success(request,"Record created successfully!")
                return JsonResponse({'success': True, 'message': 'Form Submited'}, status=200)
            except ValidationError as e:
                # Handle explicit model-level validation errors
                return JsonResponse({'success': False, 'errors': {'non_field_errors': str(e)}}, status=400)
        else:
            # Handle form errors, including unique constraint violations
            errors = {
                field: [str(error) for error in error_list]
                for field, error_list in form.errors.items()
            }
            return JsonResponse({'success': False, 'errors': errors}, status=400)
    return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=405)



def update_other_dues(request, id): 
    vehicle = get_object_or_404(OtherDues, id=id)  # Safely retrieve the Driver instance or return a 404 error
    if request.method == 'POST':
        form = OtherDuesForm(request.POST, request.FILES, instance=vehicle)  # Populate the form with the instance data
        if form.is_valid():
            form.save() 
            messages.success(request, 'Record Updated Successfully.')
    else:
        form = OtherDuesForm(instance=vehicle)  # Populate the form with the existing driver data on GET request
    return render(request, 'finance_update_other_dues.html', {'form': form,'data':vehicle})


def update_policy(request, id):
    policy = get_object_or_404(Policy, id=id)  # Safely retrieve the Driver instance or return a 404 error
    if request.method == 'POST':
        form = PolicyForm(request.POST, request.FILES, instance=policy)  # Populate the form with the instance data
        if form.is_valid():
            # print(form.cleaned_data['policy_file'])
            form.save() 
            messages.success(request, 'Policy Updated Successfully.')
    else:
        form = PolicyForm(instance=policy)  # Populate the form with the existing driver data on GET request
    return render(request, 'finance_update_policy.html', {'form': form,'policy':policy})



# View for the EMI section
@finance_required 
def emi_list(request):
    emi=EMI.objects.select_related('vehicle').order_by('next_due_date') 
    filter = EMIFilter(request.GET, queryset=emi)
    filtered_data = filter.qs  # Filtered queryset
    # EMI_Installment.objects.all().delete()
    form=EMIForm()
    context={
        'form':form,
        'emi':filtered_data,
        'filter':filter,
    }
    return render(request, 'finance_emi_list.html',context)


def create_emi(request):
    if request.method == 'POST':
        form = EMIForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                form.save()
                messages.success(request,"EMI created successfully!")
                return JsonResponse({'success': True, 'message': 'Form Submited'}, status=200)
            except ValidationError as e:
                return JsonResponse({'success': False, 'errors': {'non_field_errors': str(e)}}, status=400)
        else:
            errors = {
                field: [str(error) for error in error_list]
                for field, error_list in form.errors.items()
            }
            return JsonResponse({'success': False, 'errors': errors}, status=400)
    return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=405)



def update_emi(request, id):
    emi = get_object_or_404(EMI, id=id)  # Safely retrieve the Driver instance or return a 404 error
    if request.method == 'POST':
        form = EMIForm(request.POST, request.FILES, instance=emi)  # Populate the form with the instance data
        if form.is_valid():
            form.save() 
            messages.success(request, 'EMI Updated Successfully.')
        else:
            errors = {
                field: [str(error) for error in error_list]
                for field, error_list in form.errors.items()
            }
            messages.error(request, f'EMI Not Updated.{errors}')
    else:
        form = EMIForm(instance=emi)  # Populate the form with the existing driver data on GET request
    return render(request, 'finance_update_emi.html', {'form': form})



def delete_emi(request, id):
    data = get_object_or_404(EMI, id=id)
    if data:
        data.delete()
        messages.success(request, 'EMI deleted successfully.')
    return redirect('/finance/emi_list')




@finance_required 
def emi_item_list(request, id):
    # Fetch the EMI object
    emi = get_object_or_404(EMI, id=id)
    remaining_days = (emi.next_due_date - date.today()).days

    # Fetch all EMI items related to the selected EMI
    emi_items = EMI_Item.objects.filter(emi=emi)

    # Calculate totals for outstanding principal, principal, and interest
    total_outstanding_principal = sum([emi_item.outstanding_principal for emi_item in emi_items])
    total_principal = sum([emi_item.principal for emi_item in emi_items])
    total_interest = sum([emi_item.interest for emi_item in emi_items])
    total_installment_amount = sum([emi_item.installment_amount for emi_item in emi_items])

    # Initialize the form for adding new EMI items
    form = EMIItemForm(request.POST or None)

    # Handle form submission
    if request.method == 'POST' and form.is_valid():
        # Create a new EMI item and associate it with the selected EMI
        next_due_date=form.cleaned_data['next_due_date']
        new_emi_item = form.save(commit=False)
        new_emi_item.emi = emi
        new_emi_item.emi.next_due_date=next_due_date
        new_emi_item.save()
        messages.success(request, 'Installment Added successfully.')
        return redirect(f'/finance/emi_item_list/{emi.id}')

    # Pass the data to the template context
    context = {
        'form': form,
        'emi_items': emi_items,
        'total_outstanding_principal': total_outstanding_principal,
        'total_principal': total_principal,
        'total_interest': total_interest,
        'total_installment_amount': total_installment_amount,
        'remaining_days': remaining_days,
        'emi': emi  # Optionally pass the EMI object if needed for display
    }

    return render(request, 'finance_emi_item_list.html', context)



def delete_emi_item(request, id):
    data = get_object_or_404(EMI_Item, id=id)
    id=data.emi.id
    if data:
        data.delete()
        messages.success(request, 'EMI Item deleted successfully.')
    return redirect(f'/finance/emi_item_list/{id}')

from datetime import datetime
from dateutil.relativedelta import relativedelta
from datetime import date

@finance_required
def emi_installments_list(request, id):
    emi = get_object_or_404(EMI, id=id)
    installments = EMI_Installment.objects.filter(emi=emi)
    last_installment=installments.last()
    emi_amount=emi.emi_amount
    if last_installment:
        due_date=last_installment.next_due_date
    else:
        due_date=None
    if emi.paid_installments:
        total_installment_amount_paid=emi.paid_installments*emi_amount
    if due_date:
        next_due_date = due_date + relativedelta(months=1)
    else:
        # Set a default value, e.g., today's date or any other fallback logic you prefer
        next_due_date = None    # Or set any default value   

    form = EMI_InstallmentForm(initial={
        'emi_amount': emi_amount,
        'next_due_date': next_due_date
    }) 

    if emi.next_due_date:
        remaining_days = (emi.next_due_date - date.today()).days
    else:
        remaining_days = 0

    if request.method == 'POST':
        form = EMI_InstallmentForm(request.POST)  # Bind form with request data
        if form.is_valid():
            fm = form.save(commit=False)
            next_due_date = form.cleaned_data.get('next_due_date') 
            fm.emi = emi
            emi.next_due_date=next_due_date
            emi.save()
            fm.save()

            messages.success(request, 'Installment Added successfully.')
            return redirect(request.path)  # Redirect to clear form on success
        else:
            print("Form is not valid")
            print("Errors:", form.errors)  # Print errors for debugging

    context = {
        'form': form,
        'installments': installments,
        'remaining_days': remaining_days,
        'emi': emi,
        'installment_number':int(emi.paid_installments)+1,
        'total_installment_amount_paid':total_installment_amount_paid,
    }

    return render(request, 'finance_emi_installments_list.html', context)



def delete_emi_installment(request, id):
    data = get_object_or_404(EMI_Installment, id=id)
    id=data.emi.id
    if data:
        data.delete()
        messages.success(request, 'EMI Installment deleted successfully.')
    return redirect(f'/finance/emi_installments_list/{id}')



 
def policy_list(request):
    policies = Policy.objects.select_related('vehicle').order_by('due_date')

    policy_data = []
    for policy in policies:
        remaining_days = (policy.due_date - date.today()).days
        policy_data.append({
            'policy': policy,
            'remaining_days': remaining_days,
        })

    form = PolicyForm()
    return render(request, 'finance_policy_list.html', {
        'form': form,
        'policies': policy_data,  # Pass the enriched data
    })


def delete_policy(request, id):
    data = get_object_or_404(Policy, id=id)
    if data:
        data.delete()
        messages.success(request, 'Policy deleted successfully.')
    return redirect('/finance/policy_list')


def create_policy(request):
    if request.method == 'POST':
        form = PolicyForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                form.save()
                messages.success(request,"Policy created successfully!")
                return JsonResponse({'success': True, 'message': 'Form Submited'}, status=200)
            except ValidationError as e:
                # Handle explicit model-level validation errors
                return JsonResponse({'success': False, 'errors': {'non_field_errors': str(e)}}, status=400)
        else:
            # Handle form errors, including unique constraint violations
            errors = {
                field: [str(error) for error in error_list]
                for field, error_list in form.errors.items()
            }
            return JsonResponse({'success': False, 'errors': errors}, status=400)
    return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=405)



def update_policy(request, id):
    policy = get_object_or_404(Policy, id=id)  # Safely retrieve the Driver instance or return a 404 error
    if request.method == 'POST':
        form = PolicyForm(request.POST, request.FILES, instance=policy)  # Populate the form with the instance data
        if form.is_valid():
            # print(form.cleaned_data['policy_file'])
            form.save() 
            messages.success(request, 'Policy Updated Successfully.')
    else:
        form = PolicyForm(instance=policy)  # Populate the form with the existing driver data on GET request
    return render(request, 'finance_update_policy.html', {'form': form,'policy':policy})


# View for the Reports section
@finance_required 
def reports_list(request):
    return render(request, 'finance_reports_list.html')




@finance_required 
def insurance_bank_list(request):
    rec = Insurance_Bank.objects.all()
    if request.method == 'POST':
        form = InsuranceBankForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Record Created Success.')
            return redirect('/finance/insurance_bank_list/')
    else: 
        form = InsuranceBankForm()
    return render(request, 'finance_insurance_bank_list.html', {'rec': rec,'form': form})
 
def insurance_bank_update(request, id):
    model_instance = get_object_or_404(Insurance_Bank, id=id)
    if request.method == 'POST':
        form = InsuranceBankForm(request.POST, instance=model_instance)
        if form.is_valid():
            form.save()
            messages.success(request, 'Record Updated Success.')
    else:
        form = InsuranceBankForm(instance=model_instance)
    return render(request, 'finance_insurance_bank_update.html', {'form': form})

def insurance_bank_delete(request, id):
    model_instance = get_object_or_404(Insurance_Bank, id=id)
    model_instance.delete()
    messages.success(request, 'Record Deleted Success.')
    return redirect('/finance/insurance_bank_list')



@finance_required 
def finance_bank_list(request):
    rec = Finance_Bank.objects.all()
    if request.method == 'POST':
        form = FinanceBankForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Record Created Success.')
            return redirect('/finance/finance_bank_list/')
    else: 
        form = FinanceBankForm()
    return render(request, 'finance_finance_bank_list.html', {'rec': rec,'form': form})
 
@finance_required 
def finance_bank_update(request, id):
    model_instance = get_object_or_404(Finance_Bank, id=id)
    if request.method == 'POST':
        form = FinanceBankForm(request.POST, instance=model_instance)
        if form.is_valid():
            form.save()
            messages.success(request, 'Record Updated Success.')
    else:
        form = FinanceBankForm(instance=model_instance)
    return render(request, 'finance_finance_bank_update.html', {'form': form})

@finance_required 
def finance_bank_delete(request, id): 
    model_instance = get_object_or_404(Finance_Bank, id=id)
    model_instance.delete()
    messages.success(request, 'Record Deleted Success.')
    return redirect('/finance/finance_bank_list')




@finance_required 
def purchase_list(request):
    queryset = Purchase.objects.all().order_by('-id') 
    filter = PurchaseFilter(request.GET, queryset=queryset)
    filtered_purchase = filter.qs  # Filtered queryset
    
    # Pagination
    paginator = Paginator(filtered_purchase, 10)  # Show 10 job cards per page.
    page_number = request.GET.get('page')  # Get the page number from the GET request
    page_obj = paginator.get_page(page_number)  # Get the corresponding page object
    
    # Include the filter parameters in the pagination context
    filter_params = request.GET.copy()  # Copy the GET parameters
    if 'page' in filter_params:
        del filter_params['page']  # Remove the page parameter if it exists
    
    return render(request, "finance_purchase_list.html", {
        'purchase': page_obj,  # Pass the paginated object to the template
        'filter': filter,  # Pass the filter object for displaying the form
        'filter_params': filter_params.urlencode(),  # Pass the filter parameters for pagination
    })


@finance_required 
def update_purchase(request, id):
    purchase = Purchase.objects.get(id=id)  # Retrieve the JobCard instance
    if request.method == 'POST':
        form = PurchaseUpdateForm(request.POST, request.FILES, instance=purchase)
        if form.is_valid():
            form.save()
            messages.success(request, 'Status Updated Successfully.')
    else:
        form = PurchaseUpdateForm(instance=purchase)
    return render(request, 'finance_update_purchase.html', {'form': form})


@finance_required 
def purchase_item_list(request,id):
    purchase=get_object_or_404(Purchase, id=id)
    product_data = list(Product.objects.select_related('model'))
    item=PurchaseItem.objects.filter(purchase=purchase).order_by('-id')
    total_amount = item.aggregate(Sum('total_amount'))['total_amount__sum']

    if request.method == 'POST':
        form = PurchaseUpdateForm(request.POST, request.FILES, instance=purchase)
        if form.is_valid():
            form.save()
            messages.success(request, 'Status Updated Successfully.')
    else:
        form = PurchaseUpdateForm(instance=purchase)
    return render(request, "finance_purchase_item_list.html",{'form':form,'item':item,'purchase':purchase,'product_data':product_data,'total_amount':total_amount})
