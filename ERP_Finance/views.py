from django.shortcuts import render,get_object_or_404,redirect
from ERP_Admin.models import Policy
from .forms import *
from django.http import JsonResponse
from django.contrib import messages
from django.core.paginator import Paginator

# Create your views here.
def dashboard(request):
    return render(request, 'finance_dashboard.html')

# View for the EMI section
def emi_list(request):
    return render(request, 'finance_emi_list.html')

# View for the Policy section

def policy_list(request):
    # Fetch policies and prefetch related vehicle information
    policy = Policy.objects.select_related('vehicle')
    # Pagination
    # paginator = Paginator(policy, 4)  # Show 10 policies per page
    # page_number = request.GET.get('page')  # Get the page number from the GET request
    # page_obj = paginator.get_page(page_number)  # Get the corresponding page object

    # filter_params = request.GET.copy()  
    # if 'page' in filter_params:
    #     del filter_params['page']  # Remove the page parameter if it exists

    form = PolicyForm()
    return render(request, 'finance_policy_list.html', {
        'form': form,
        'policy': policy,
        # 'filter_params': filter_params.urlencode(),  # Ensure the filter params are included in the pagination links
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

# View for the Reports section
def reports_list(request):
    return render(request, 'finance_reports_list.html')