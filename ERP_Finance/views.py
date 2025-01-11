from django.shortcuts import render,get_object_or_404,redirect
from ERP_Admin.models import Policy,EMI,EMI_Item,Vehicle,Insurance_Bank,Finance_Bank
from .forms import *
from django.http import JsonResponse
from django.contrib import messages
from django.core.paginator import Paginator
from datetime import date
from ERP_Admin.filters import EMIFilter
from django.db.models import Sum, F, Q
from django.db.models import Count, Case, When, F, IntegerField,ExpressionWrapper
from django.utils import timezone
from datetime import timedelta 
from collections import Counter
from ERP_Admin.filters import VehicleFilterForFinance
from functools import wraps

def finance_required(function):
    @wraps(function)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/login')  # Redirect to login if not logged in
        if not request.user.is_finance:
            return redirect('/login')  # Redirect to login if user is not in Finance role
        return function(request, *args, **kwargs)
    return _wrapped_view

@finance_required 
def dashboard(request):
    today = date.today()
    thirty_days_date = today + timedelta(days=30)
    thirty_days_counts = Counter({
        "policy_dues": Policy.objects.filter(due_date__range=[today, thirty_days_date],due_date__isnull=False,vehicle__status='active').count(),
        "emi_dues": EMI.objects.filter(next_due_date__range=[today, thirty_days_date],next_due_date__isnull=False,vehicle__status='active').count(),
        "tax_dues": OtherDues.objects.filter(tax_due_date__range=[today, thirty_days_date],tax_due_date__isnull=False,vehicle__status='active').count(),
        "fitness_dues": OtherDues.objects.filter(fitness_due_date__range=[today, thirty_days_date],fitness_due_date__isnull=False,vehicle__status='active').count(),
        "permit_dues": OtherDues.objects.filter(permit_due_date__range=[today, thirty_days_date],permit_due_date__isnull=False,vehicle__status='active').count(),
        "puc_dues": OtherDues.objects.filter(puc_due_date__range=[today, thirty_days_date],puc_due_date__isnull=False,vehicle__status='active').count(),
    })
     
    
    # Count individual dues for upcoming and past
    expire_dues_counts = Counter({
        "policy_dues": Policy.objects.filter(due_date__lt=today,due_date__isnull=False,vehicle__status='active').count(),
        "emi_dues": EMI.objects.filter(next_due_date__lt=today,next_due_date__isnull=False,vehicle__status='active').count(),
        "tax_dues": OtherDues.objects.filter(tax_due_date__lt=today,tax_due_date__isnull=False).count(),
        "fitness_dues": OtherDues.objects.filter(fitness_due_date__lt=today,fitness_due_date__isnull=False,vehicle__status='active').count(),
        "permit_dues": OtherDues.objects.filter(permit_due_date__lt=today,permit_due_date__isnull=False,vehicle__status='active').count(),
        "puc_dues": OtherDues.objects.filter(puc_due_date__lt=today,puc_due_date__isnull=False,vehicle__status='active').count(),
    })

    two_days_later = today + timedelta(days=2)
    # Query the different dues in the next 2 days
    emi_dues = EMI.objects.filter(next_due_date__range=[today, two_days_later]).values('vehicle__id', 'vehicle__vehicle_number', 'next_due_date')
    policy_dues = Policy.objects.filter(due_date__range=[today, two_days_later]).values('vehicle__id', 'vehicle__vehicle_number', 'due_date')
    tax_dues = OtherDues.objects.filter(tax_due_date__range=[today, two_days_later]).values('vehicle__id', 'vehicle__vehicle_number', 'tax_due_date')
    fitness_dues = OtherDues.objects.filter(fitness_due_date__range=[today, two_days_later]).values('vehicle__id', 'vehicle__vehicle_number', 'fitness_due_date')
    permit_dues = OtherDues.objects.filter(permit_due_date__range=[today, two_days_later]).values('vehicle__id', 'vehicle__vehicle_number', 'permit_due_date')
    puc_dues = OtherDues.objects.filter(puc_due_date__range=[today, two_days_later]).values('vehicle__id', 'vehicle__vehicle_number', 'puc_due_date')

    # Add the due type as a custom field for each query result
    emi_dues_2 = [{'vehicle_id': due['vehicle__id'], 'vehicle_number': due['vehicle__vehicle_number'], 'due_date': due['next_due_date'], 'due_name': 'EMI'} for due in emi_dues]
    policy_dues_2 = [{'vehicle_id': due['vehicle__id'], 'vehicle_number': due['vehicle__vehicle_number'], 'due_date': due['due_date'], 'due_name': 'Policy'} for due in policy_dues]
    tax_dues_2 = [{'vehicle_id': due['vehicle__id'], 'vehicle_number': due['vehicle__vehicle_number'], 'due_date': due['tax_due_date'], 'due_name': 'Tax'} for due in tax_dues]
    fitness_dues_2 = [{'vehicle_id': due['vehicle__id'], 'vehicle_number': due['vehicle__vehicle_number'], 'due_date': due['fitness_due_date'], 'due_name': 'Fitness'} for due in fitness_dues]
    permit_dues_2 = [{'vehicle_id': due['vehicle__id'], 'vehicle_number': due['vehicle__vehicle_number'], 'due_date': due['permit_due_date'], 'due_name': 'Permit'} for due in permit_dues]
    puc_dues_2 = [{'vehicle_id': due['vehicle__id'], 'vehicle_number': due['vehicle__vehicle_number'], 'due_date': due['puc_due_date'], 'due_name': 'PUC'} for due in puc_dues]

    # Combine all dues data
    two_days_later_dues = emi_dues_2 + policy_dues_2 + tax_dues_2 + fitness_dues_2 + permit_dues_2 + puc_dues_2
 
    fifteen_days_ago = today - timedelta(days=15)
    one_days_ago = today - timedelta(days=1)

    emi_dues = EMI.objects.filter(next_due_date__range=[fifteen_days_ago, one_days_ago]).values('vehicle__id', 'vehicle__vehicle_number', 'next_due_date')
    policy_dues = Policy.objects.filter(due_date__range=[fifteen_days_ago, one_days_ago]).values('vehicle__id', 'vehicle__vehicle_number', 'due_date')
    tax_dues = OtherDues.objects.filter(tax_due_date__range=[fifteen_days_ago, one_days_ago]).values('vehicle__id', 'vehicle__vehicle_number', 'tax_due_date')
    fitness_dues = OtherDues.objects.filter(fitness_due_date__range=[fifteen_days_ago, one_days_ago]).values('vehicle__id', 'vehicle__vehicle_number', 'fitness_due_date')
    permit_dues = OtherDues.objects.filter(permit_due_date__range=[fifteen_days_ago, one_days_ago]).values('vehicle__id', 'vehicle__vehicle_number', 'permit_due_date')
    puc_dues = OtherDues.objects.filter(puc_due_date__range=[fifteen_days_ago, one_days_ago]).values('vehicle__id', 'vehicle__vehicle_number', 'puc_due_date')


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
        'expire_dues_counts':expire_dues_counts,
        'two_days_later_dues':two_days_later_dues,
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
    emi_amount=None
    if emi:
        emi_amount=int(emi.loan_amount)/int(emi.total_installments)

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
        'emi_amount':emi_amount,
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

def finance_bank_delete(request, id): 
    model_instance = get_object_or_404(Finance_Bank, id=id)
    model_instance.delete()
    messages.success(request, 'Record Deleted Success.')
    return redirect('/finance/finance_bank_list')
