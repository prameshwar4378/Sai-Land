from django.shortcuts import render,get_object_or_404,redirect
from ERP_Admin.models import Policy,EMI,EMI_Item,Vehicle,InsuranceTaxDue
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

def dashboard(request):
    today = date.today()
    thirty_days_date = today + timedelta(days=30)
    thirty_days_counts = Counter({
        "policy_dues": Policy.objects.filter(due_date__range=[today, thirty_days_date],due_date__isnull=False,vehicle__status='active').count(),
        "emi_dues": EMI.objects.filter(next_due_date__range=[today, thirty_days_date],next_due_date__isnull=False,vehicle__status='active').count(),
        "insurance_dues": InsuranceTaxDue.objects.filter(insurance_due_date__range=[today, thirty_days_date],insurance_due_date__isnull=False,vehicle__status='active').count(),
        "tax_dues": InsuranceTaxDue.objects.filter(tax_due_date__range=[today, thirty_days_date],tax_due_date__isnull=False,vehicle__status='active').count(),
        "fitness_dues": InsuranceTaxDue.objects.filter(fitness_due_date__range=[today, thirty_days_date],fitness_due_date__isnull=False,vehicle__status='active').count(),
        "permit_dues": InsuranceTaxDue.objects.filter(permit_due_date__range=[today, thirty_days_date],permit_due_date__isnull=False,vehicle__status='active').count(),
        "puc_dues": InsuranceTaxDue.objects.filter(puc_due_date__range=[today, thirty_days_date],puc_due_date__isnull=False,vehicle__status='active').count(),
    })
     
    
    # Count individual dues for upcoming and past
    expire_dues_counts = Counter({
        "policy_dues": Policy.objects.filter(due_date__lt=today,due_date__isnull=False,vehicle__status='active').count(),
        "emi_dues": EMI.objects.filter(next_due_date__lt=today,next_due_date__isnull=False,vehicle__status='active').count(),
        "insurance_dues": InsuranceTaxDue.objects.filter(insurance_due_date__lt=today,insurance_due_date__isnull=False,vehicle__status='active').count(),
        "tax_dues": InsuranceTaxDue.objects.filter(tax_due_date__lt=today,tax_due_date__isnull=False).count(),
        "fitness_dues": InsuranceTaxDue.objects.filter(fitness_due_date__lt=today,fitness_due_date__isnull=False,vehicle__status='active').count(),
        "permit_dues": InsuranceTaxDue.objects.filter(permit_due_date__lt=today,permit_due_date__isnull=False,vehicle__status='active').count(),
        "puc_dues": InsuranceTaxDue.objects.filter(puc_due_date__lt=today,puc_due_date__isnull=False,vehicle__status='active').count(),
    })

    two_days_later = today + timedelta(days=2)
    # Query the different dues in the next 2 days
    emi_dues = EMI.objects.filter(next_due_date__range=[today, two_days_later]).values('vehicle__id', 'vehicle__vehicle_number', 'next_due_date')
    policy_dues = Policy.objects.filter(due_date__range=[today, two_days_later]).values('vehicle__id', 'vehicle__vehicle_number', 'due_date')
    insurance_dues = InsuranceTaxDue.objects.filter(insurance_due_date__range=[today, two_days_later]).values('vehicle__id', 'vehicle__vehicle_number', 'insurance_due_date')
    tax_dues = InsuranceTaxDue.objects.filter(tax_due_date__range=[today, two_days_later]).values('vehicle__id', 'vehicle__vehicle_number', 'tax_due_date')
    fitness_dues = InsuranceTaxDue.objects.filter(fitness_due_date__range=[today, two_days_later]).values('vehicle__id', 'vehicle__vehicle_number', 'fitness_due_date')
    permit_dues = InsuranceTaxDue.objects.filter(permit_due_date__range=[today, two_days_later]).values('vehicle__id', 'vehicle__vehicle_number', 'permit_due_date')
    puc_dues = InsuranceTaxDue.objects.filter(puc_due_date__range=[today, two_days_later]).values('vehicle__id', 'vehicle__vehicle_number', 'puc_due_date')

    # Add the due type as a custom field for each query result
    emi_dues_2 = [{'vehicle_id': due['vehicle__id'], 'vehicle_number': due['vehicle__vehicle_number'], 'due_date': due['next_due_date'], 'due_name': 'EMI'} for due in emi_dues]
    policy_dues_2 = [{'vehicle_id': due['vehicle__id'], 'vehicle_number': due['vehicle__vehicle_number'], 'due_date': due['due_date'], 'due_name': 'Policy'} for due in policy_dues]
    insurance_dues_2 = [{'vehicle_id': due['vehicle__id'], 'vehicle_number': due['vehicle__vehicle_number'], 'due_date': due['insurance_due_date'], 'due_name': 'Insurance'} for due in insurance_dues]
    tax_dues_2 = [{'vehicle_id': due['vehicle__id'], 'vehicle_number': due['vehicle__vehicle_number'], 'due_date': due['tax_due_date'], 'due_name': 'Tax'} for due in tax_dues]
    fitness_dues_2 = [{'vehicle_id': due['vehicle__id'], 'vehicle_number': due['vehicle__vehicle_number'], 'due_date': due['fitness_due_date'], 'due_name': 'Fitness'} for due in fitness_dues]
    permit_dues_2 = [{'vehicle_id': due['vehicle__id'], 'vehicle_number': due['vehicle__vehicle_number'], 'due_date': due['permit_due_date'], 'due_name': 'Permit'} for due in permit_dues]
    puc_dues_2 = [{'vehicle_id': due['vehicle__id'], 'vehicle_number': due['vehicle__vehicle_number'], 'due_date': due['puc_due_date'], 'due_name': 'PUC'} for due in puc_dues]

    # Combine all dues data
    two_days_later_dues = emi_dues_2 + policy_dues_2 + insurance_dues_2 + tax_dues_2 + fitness_dues_2 + permit_dues_2 + puc_dues_2
 
    fifteen_days_ago = today - timedelta(days=15)
    one_days_ago = today - timedelta(days=1)

    emi_dues = EMI.objects.filter(next_due_date__range=[fifteen_days_ago, one_days_ago]).values('vehicle__id', 'vehicle__vehicle_number', 'next_due_date')
    policy_dues = Policy.objects.filter(due_date__range=[fifteen_days_ago, one_days_ago]).values('vehicle__id', 'vehicle__vehicle_number', 'due_date')
    insurance_dues = InsuranceTaxDue.objects.filter(insurance_due_date__range=[fifteen_days_ago, one_days_ago]).values('vehicle__id', 'vehicle__vehicle_number', 'insurance_due_date')
    tax_dues = InsuranceTaxDue.objects.filter(tax_due_date__range=[fifteen_days_ago, one_days_ago]).values('vehicle__id', 'vehicle__vehicle_number', 'tax_due_date')
    fitness_dues = InsuranceTaxDue.objects.filter(fitness_due_date__range=[fifteen_days_ago, one_days_ago]).values('vehicle__id', 'vehicle__vehicle_number', 'fitness_due_date')
    permit_dues = InsuranceTaxDue.objects.filter(permit_due_date__range=[fifteen_days_ago, one_days_ago]).values('vehicle__id', 'vehicle__vehicle_number', 'permit_due_date')
    puc_dues = InsuranceTaxDue.objects.filter(puc_due_date__range=[fifteen_days_ago, one_days_ago]).values('vehicle__id', 'vehicle__vehicle_number', 'puc_due_date')


    emi_dues = [{'vehicle_id': due['vehicle__id'], 'vehicle_number': due['vehicle__vehicle_number'], 'due_date': due['next_due_date'], 'due_name': 'EMI'} for due in emi_dues]
    policy_dues = [{'vehicle_id': due['vehicle__id'], 'vehicle_number': due['vehicle__vehicle_number'], 'due_date': due['due_date'], 'due_name': 'Policy'} for due in policy_dues]
    insurance_dues = [{'vehicle_id': due['vehicle__id'], 'vehicle_number': due['vehicle__vehicle_number'], 'due_date': due['insurance_due_date'], 'due_name': 'Insurance'} for due in insurance_dues]
    tax_dues = [{'vehicle_id': due['vehicle__id'], 'vehicle_number': due['vehicle__vehicle_number'], 'due_date': due['tax_due_date'], 'due_name': 'Tax'} for due in tax_dues]
    fitness_dues = [{'vehicle_id': due['vehicle__id'], 'vehicle_number': due['vehicle__vehicle_number'], 'due_date': due['fitness_due_date'], 'due_name': 'Fitness'} for due in fitness_dues]
    permit_dues = [{'vehicle_id': due['vehicle__id'], 'vehicle_number': due['vehicle__vehicle_number'], 'due_date': due['permit_due_date'], 'due_name': 'Permit'} for due in permit_dues]
    puc_dues = [{'vehicle_id': due['vehicle__id'], 'vehicle_number': due['vehicle__vehicle_number'], 'due_date': due['puc_due_date'], 'due_name': 'PUC'} for due in puc_dues]

    # Combine all dues data
    fifteen_days_ago_expire_dues = emi_dues + policy_dues + insurance_dues + tax_dues + fitness_dues + permit_dues + puc_dues
  
    # Pass data to template
    return render(request, 'finance_dashboard.html', { 
        'thirty_days_counts':thirty_days_counts,
        'expire_dues_counts':expire_dues_counts,
        'two_days_later_dues':two_days_later_dues,
        'fifteen_days_ago_expire_dues':fifteen_days_ago_expire_dues

    })

def vehicle_list(request):
    # Apply the filter to the queryset
    queryset=Vehicle.objects.all()
    # Get the filtered vehicles

    # Prepare the context with the filtered vehicles
    context = []
    for vehicle in queryset:
        # Get related data for each vehicle
        policies = vehicle.policies.all()
        emis = vehicle.emis.all()
        insurance_tax = vehicle.insurancetaxdue_set.first()  # Assuming one insurance/tax record
        
        # Extract relevant due dates
        policy_due_date = policies[0].due_date if policies else None
        emi_due_date = emis[0].next_due_date if emis else None
        insurance_due_date = insurance_tax.insurance_due_date if insurance_tax else None
        tax_due_date = insurance_tax.tax_due_date if insurance_tax else None
        fitness_due_date = insurance_tax.fitness_due_date if insurance_tax else None
        permit_due_date = insurance_tax.permit_due_date if insurance_tax else None
        puc_due_date = insurance_tax.puc_due_date if insurance_tax else None

        # Add vehicle info to the context
        context.append({
            'id': vehicle.id,
            'vehicle_number': vehicle.vehicle_number,
            'policy_due_date': policy_due_date,
            'emi_due_date': emi_due_date,
            'insurance_due_date': insurance_due_date,
            'tax_due_date': tax_due_date,
            'fitness_due_date': fitness_due_date,
            'permit_due_date': permit_due_date,
            'puc_due_date': puc_due_date,
        })

    # Pass the filter and the context to the template
    return render(request, 'finance_vehicle_list.html', {
        'context': context
    })

# View for the EMI section
def vehicle_dashboard(request,id):
    vehicle = Vehicle.objects.all() or None
    vehicle = Vehicle.objects.get(id=id)
    insurance_tax_due_data=InsuranceTaxDue.objects.filter(vehicle=vehicle) 

    insurance_tax_due=InsuranceTaxDue.objects.filter(vehicle=vehicle).first() 
    insurance_tax_due_id=0 
    if insurance_tax_due:
        insurance_tax_due_id=insurance_tax_due.id 

    is_data_exist=insurance_tax_due_data.exists()

    emi=EMI.objects.filter(vehicle=vehicle).first()
    emi_amount=None
    if emi:
        emi_amount=int(emi.loan_amount)/int(emi.total_installments)

    policy=Policy.objects.filter(vehicle=vehicle).first()
    insurance_tax_due=InsuranceTaxDue.objects.filter(vehicle=vehicle).first()


    form=InsuranceTaxDueForm() 
    context={
        'vehicle_id':id,
        'vehicle':vehicle,
        'form':form,
        'is_data_exist':is_data_exist,
        'emi':emi,
        'emi_amount':emi_amount,
        'policy':policy,
        'insurance_tax_due':insurance_tax_due,
        'insurance_tax_due_id':insurance_tax_due_id
    }
    return render(request, 'finance_vehicle_dashboard.html',context)



def create_insurance_tax_due(request):
    if request.method == 'POST':
        form = InsuranceTaxDueForm(request.POST, request.FILES)

        if form.is_valid():
            try:
                vehicle_id=request.POST.get('vehicle_id') 

                vehicle=Vehicle.objects.get(id=vehicle_id)
                if vehicle and InsuranceTaxDue.objects.filter(vehicle=vehicle).exists():
                    print("this is test")
                    print("this is test")
                    print("this is test")
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



def update_insurance_tax_due(request, id): 
    vehicle = get_object_or_404(InsuranceTaxDue, id=id)  # Safely retrieve the Driver instance or return a 404 error
    if request.method == 'POST':
        form = InsuranceTaxDueForm(request.POST, request.FILES, instance=vehicle)  # Populate the form with the instance data
        if form.is_valid():
            form.save() 
            messages.success(request, 'Record Updated Successfully.')
    else:
        form = InsuranceTaxDueForm(instance=vehicle)  # Populate the form with the existing driver data on GET request
    return render(request, 'finance_update_insurance_tax_due.html', {'form': form,'data':vehicle})


def update_policy(request, id):
    policy = get_object_or_404(Policy, id=id)  # Safely retrieve the Driver instance or return a 404 error
    if request.method == 'POST':
        form = PolicyForm(request.POST, request.FILES, instance=policy)  # Populate the form with the instance data
        if form.is_valid():
            print(form.cleaned_data['policy_file'])
            form.save() 
            messages.success(request, 'Policy Updated Successfully.')
    else:
        form = PolicyForm(instance=policy)  # Populate the form with the existing driver data on GET request
    return render(request, 'finance_update_policy.html', {'form': form,'policy':policy})



# View for the EMI section
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
        form = EMIForm(instance=emi)  # Populate the form with the existing driver data on GET request
    return render(request, 'finance_update_emi.html', {'form': form})



def delete_emi(request, id):
    data = get_object_or_404(EMI, id=id)
    if data:
        data.delete()
        messages.success(request, 'EMI deleted successfully.')
    return redirect('/finance/emi_list')




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
            print(form.cleaned_data['policy_file'])
            form.save() 
            messages.success(request, 'Policy Updated Successfully.')
    else:
        form = PolicyForm(instance=policy)  # Populate the form with the existing driver data on GET request
    return render(request, 'finance_update_policy.html', {'form': form,'policy':policy})


# View for the Reports section
def reports_list(request):
    return render(request, 'finance_reports_list.html')