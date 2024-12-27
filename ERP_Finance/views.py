from django.shortcuts import render,get_object_or_404,redirect
from ERP_Admin.models import Policy,EMI,EMI_Item
from .forms import *
from django.http import JsonResponse
from django.contrib import messages
from django.core.paginator import Paginator
from datetime import date
from ERP_Admin.filters import EMIFilter
# Create your views here.
def dashboard(request):
    return render(request, 'finance_dashboard.html')

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