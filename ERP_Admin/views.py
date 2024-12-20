from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from django.contrib import messages
import openpyxl
from .forms import *
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth import login as authlogin, authenticate,logout as DeleteSession

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.db.models import Sum, Count, Q, F


from django.core.cache import cache

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.forms.models import model_to_dict
from django.core.cache import cache
from .models import *
from django.core.paginator import Paginator
from .filters import *
from django.db.models import Sum


@receiver(post_save, sender=Product)
def update_cache_on_save(sender, instance, **kwargs):
    products = [] 
    for product in Product.objects.select_related('model').all().order_by('-id'):
        product_data = model_to_dict(product)
        product_data['model'] = {
            'model_name': product.model.model_name,   
        }
        products.append(product_data)
    cache.set('cache_products', products, timeout=None)

@receiver(post_delete, sender=Product)
def update_cache_on_delete(sender, instance, **kwargs):
    update_cache_on_save(sender, instance)  #  




@receiver(post_save, sender=Driver)
def update_driver_cache_on_save(sender, instance, **kwargs):
    # Use select_related to fetch the related CustomUser data in one query
    drivers = Driver.objects.select_related('user').all().values(
        'id', 'profile_photo','driver_name', 'license_number','profile_photo',  'mobile_number','alternate_mobile_number', 'adhaar_number', 'address', 'date_of_birth', 'date_joined',
        'user__username', 'user__email', 'user__first_name', 'user__last_name', 'emp_id__emp_id'    # Add related fields from CustomUser
    )
    # Update the cache with the latest driver data, including CustomUser related fields
    cache.set('cache_drivers', list(drivers), timeout=None)
    print("Driver cache updated on save")

@receiver(post_delete, sender=Driver)
def update_driver_cache_on_delete(sender, instance, **kwargs):
    # Use select_related to fetch related CustomUser data after a delete
    drivers = Driver.objects.select_related('user').all().values(
        'id','profile_photo', 'driver_name', 'license_number','profile_photo',  'mobile_number','alternate_mobile_number', 'adhaar_number', 'address', 'date_of_birth', 'date_joined',
        'user__username', 'user__email', 'user__first_name', 'user__last_name', 'emp_id__emp_id'   
    )
    # Update the cache to reflect the deletion
    # Update the cache to reflect the deletion
    cache.set('cache_drivers', list(drivers), timeout=None)
    print("Driver cache updated on delete")

 
@receiver(post_save, sender=Technician)
def update_technician_cache_on_save(sender, instance, **kwargs):
    # Retrieve all technicians data and serialize it if needed
    technicians = Technician.objects.all().values(
        'id', 'technician_name', 'adhaar_number', 'mobile_number','alternate_mobile_number', 'email', 'address', 'date_of_birth', 'date_joined'
    )
    # Update cache with the latest technicians data
    cache.set('cache_technicians', list(technicians), timeout=None)
    print("Technician cache updated on save")

@receiver(post_delete, sender=Technician)
def update_technician_cache_on_delete(sender, instance, **kwargs):
    # Retrieve all technicians data after delete
    technicians = Technician.objects.all().values(
        'id', 'technician_name', 'adhaar_number', 'mobile_number','alternate_mobile_number', 'email', 'address', 'date_of_birth', 'date_joined'
    )
    # Update the cache to reflect the deletion
    cache.set('cache_technicians', list(technicians), timeout=None)
    print("Technician cache updated on delete")




@receiver(post_save, sender=Party)
def update_party_cache_on_save(sender, instance, **kwargs):
    # Retrieve all partys data and serialize it if needed
    partys = Party.objects.all() 
    # Update cache with the latest partys data
    cache.set('cache_partys', list(partys), timeout=None)
    print("Party cache updated on save")

@receiver(post_delete, sender=Party)
def update_party_cache_on_delete(sender, instance, **kwargs):
    # Retrieve all partys data after delete
    partys = Party.objects.all() 
    # Update the cache to reflect the deletion
    cache.set('cache_partys', list(partys), timeout=None)
    print("Party cache updated on delete")


def login(request): 
    if request.user.is_authenticated:
        print(type(request.user))  # Debug print to check the model being used
        return redirect_user_based_on_role(request, request.user)

    if request.method == 'POST': 
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        user = authenticate(request, username=username, password=password)
        print(f'Authenticated user: {user}, User type: {type(user)}')  # Debug print
        if user is not None:
            auth_login(request, user)
            return redirect_user_based_on_role(request, user)
        else:
            messages.error(request, 'Oops...! User does not exist. Please try again.')

    return render(request, 'login.html')



def update_driver_password(request, id):
    driver = get_object_or_404(Driver, id=id)  # Retrieve the Driver instance safely
    user = get_object_or_404(CustomUser, id=driver.user.id)  # Retrieve the associated CustomUser safely
    if request.method == 'POST':
        form = UpdatePasswordForm(request.POST)
        if form.is_valid():
            # Set the new password for the user and save
            new_password = form.cleaned_data['new_password1']
            user.set_password(new_password)
            user.save()
            messages.success(request, 'Password updated successfully.')
    else:
        form = UpdatePasswordForm()
    return render(request, 'admin_update_driver_password.html', {'form': form, 'driver': driver})


def redirect_user_based_on_role(request, user):
    if user.is_superuser:
        print('Redirecting to Admin Dashboard')  # Debug print
        return redirect('/admin/dashboard')
    elif user.is_workshop:
        print('Redirecting to Workshop Dashboard')  # Debug print
        return redirect('/workshop/dashboard')
    elif user.is_account:
        print('Redirecting to Account Dashboard')  # Debug print
        return redirect('/account/dashboard')
    else:
        print('Unauthorized user role')  # Debug print
        messages.error(request, 'Unauthorized user role.')
        return redirect('login')

def logout(request):
    DeleteSession(request)
    return redirect('/login')


def dashboard(request):
    # Count users based on roles
    admin_count = CustomUser.objects.filter(is_admin=True).count()
    account_count = CustomUser.objects.filter(is_account=True).count()
    workshop_count = CustomUser.objects.filter(is_workshop=True).count()
    driver_count = CustomUser.objects.filter(is_driver=True).count()

    # Prepare data for the pie chart
    roles = ['Admin', 'Account', 'Workshop', 'Driver']
    counts = [admin_count, account_count, workshop_count, driver_count]
    user_count = CustomUser.objects.filter(
        Q(is_admin=True) | Q(is_account=True) | Q(is_workshop=True) | Q(is_driver=True)
    ).count()
    product_count=Product.objects.all().count()
    vehicle_count=Vehicle.objects.all().count()
    # Pass data to the template
    context = {
        'roles': roles,
        'counts': counts,
        'user_count': user_count,
        'product_count':product_count,
        'vehicle_count':vehicle_count
    }
    return render(request, "admin_dashboard.html", context)


def notifications(request):
    return render(request, "admin_notifications.html")

def financial_management(request):
    return render(request, "admin_financial_management.html")

def live_status(request):
    return render(request, "admin_live_status.html")

def job_card_list(request):
    queryset = JobCard.objects.all().order_by('-id') 
    filter = JobCardFilter(request.GET, queryset=queryset)
    filtered_job_cards = filter.qs  # Filtered queryset
    # Pagination
    paginator = Paginator(filtered_job_cards, 20)  # Show 10 job cards per page. 
    page_number = request.GET.get('page')  # Get the page number from the GET request
    page_obj = paginator.get_page(page_number)  # Get the corresponding page object
    
    # Include the filter parameters in the pagination context
    filter_params = request.GET.copy()  # Copy the GET parameters
    pending_count=filtered_job_cards.filter(status="pending").count()
    in_progress_count=filtered_job_cards.filter(status="in_progress").count()
    completed_count=filtered_job_cards.filter(status="completed").count()
    total_count=int(pending_count)+int(in_progress_count)+int(completed_count)
    if 'page' in filter_params:
        del filter_params['page']  # Remove the page parameter if it exists
    return render(request, "admin_job_card_list.html", {
        'job_card': page_obj,  # Pass the paginated object to the template
        'filter': filter,  # Pass the filter object for displaying the form
        'filter_params': filter_params.urlencode(),  # Pass the filter parameters for pagination
        'pending_count':pending_count,
        'in_progress_count':in_progress_count,
        'completed_count':completed_count,
        'total_count':total_count

    })



def job_card_item_list(request, id):
    job_card = get_object_or_404(JobCard, id=id)
    items = JobCardItem.objects.filter(job_card=job_card).order_by('-id')
    total_cost = items.aggregate(Sum('total_cost'))['total_cost__sum']
    total_cost = int(total_cost) if total_cost is not None else 0
    labour_cost=int(job_card.labour_cost) if job_card.labour_cost is not None else 0
    grand_total_cost=int(total_cost+labour_cost)

   
    return render(request, "admin_job_card_item_list.html", {
        'items': items,
        'job_card': job_card,
        'total_cost': total_cost,
        'labour_cost':labour_cost,
        'grand_total_cost':grand_total_cost
    })



def purchase_list(request):
    queryset = Purchase.objects.all().order_by('-id') 
    filter = PurchaseFilter(request.GET, queryset=queryset)
    filtered_purchase = filter.qs  # Filtered queryset
    
    # Pagination
    paginator = Paginator(filtered_purchase, 20)  # Show 10 job cards per page.
    page_number = request.GET.get('page')  # Get the page number from the GET request
    page_obj = paginator.get_page(page_number)  # Get the corresponding page object
    
    # Include the filter parameters in the pagination context
    filter_params = request.GET.copy()  # Copy the GET parameters
    if 'page' in filter_params:
        del filter_params['page']  # Remove the page parameter if it exists
    total_bill_count=filtered_purchase.count()
    total_amount = filtered_purchase.aggregate(Sum('total_cost'))['total_cost__sum'] or 0.0
    return render(request, "admin_purchase_list.html", {
        'purchase': page_obj,  # Pass the paginated object to the template
        'filter': filter,  # Pass the filter object for displaying the form
        'filter_params': filter_params.urlencode(),  # Pass the filter parameters for pagination
        'total_bill_count':total_bill_count,
        'total_amount':total_amount
    })



def purchase_item_list(request,id):
    purchase=get_object_or_404(Purchase, id=id)
    item=PurchaseItem.objects.filter(purchase=purchase).order_by('-id')
    total_amount = item.aggregate(Sum('total_amount'))['total_amount__sum']
    total_amount = int(total_amount) if total_amount is not None else 0  # In case there are no items, set total_amount to 0
    return render(request, "admin_purchase_item_list.html",{'item':item,'purchase':purchase,'total_amount':total_amount})



def product_list(request):
    # Retrieve products from cache
    products = cache.get('cache_products')
 
    # Variables for counts
    out_of_stock = 0
    minimum_stock_alert_count = 0
    total_available_stock = 0

    if not products:
        # Query all products and store in cache
        products = list(Product.objects.all().order_by('-id').values())
        cache.set('cache_products', products, timeout=None)

    # Perform calculations
    out_of_stock = Product.objects.filter(available_stock__lte=0).count()  # Count products with no stock
    minimum_stock_alert_count = Product.objects.filter(available_stock__lte=F('minimum_stock_alert')).count()  # Count products below minimum stock
    total_available_stock = Product.objects.aggregate(total=Sum('available_stock'))['total'] or 0  # Sum of all available stock

    # Context for rendering
    context = {
        'product': products,
        'out_of_stock': out_of_stock,
        'minimum_stock_alert_count': minimum_stock_alert_count,
        'total_available_stock': total_available_stock,
    }
    return render(request, "admin_product_list.html", context)


def report(request):
    return render(request, "admin_report.html")

def user_management(request):
    form=UserRegistrationForm()
    users=CustomUser.objects.filter(is_driver=False,is_superuser=False)
    for i in users:
        print(i.emp_id)
    return render(request, "admin_user_management.html",{'form':form,'users':users})

def create_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return JsonResponse({'success': True, 'message': 'User created successfully!'})
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

def update_user(request, id):
    user = get_object_or_404(CustomUser, id=id)
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, instance=user)  # Pre-populate the form with the user data
        if form.is_valid():
            form.save()  # Save the updated user data
            messages.success(request, "User details updated successfully.")
    else:
        form = UserRegistrationForm(instance=user)  # Pre-populate the form with existing data for GET request
    return render(request, 'admin_update_user.html', {'form': form, 'user': user})


def delete_user(request, id):
    user = get_object_or_404(CustomUser, id=id)
    if user:
        print(user.username)
        user.delete()
        messages.success(request, 'User deleted successfully.')


def drivers_list(request):
    drivers = cache.get('cache_drivers')
    if not drivers:
        drivers = Driver.objects.select_related('user').all().values(
            'id', 'driver_name','emp_id__emp_id', 'license_number', 'mobile_number', 'profile_photo', 'adhaar_number', 'address', 'date_of_birth', 'date_joined',
            'user__username', 'user__email', 'user__first_name', 'user__last_name' 
        )
        print("Cache Set Successfully...")
        print("Cache Set Successfully...")
        print("Cache Set Successfully...")
        cache.set('cache_drivers', list(drivers), timeout=None)
    for i in drivers:
        print(i)
    form=DriverRegistrationForm()
    incomplete_profile = CustomUser.objects.filter(driver__isnull=True,is_driver=True).delete()[0]
    return render(request, "admin_drivers_list.html",{'form':form,'drivers':drivers})


def create_driver(request):
    if request.method == 'POST':
        form = DriverRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                print("Form data is valid")
                print(form.cleaned_data)
                form.save()
                return JsonResponse({'success': True, 'message': 'Driver created successfully!'})
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



def update_driver(request, id):
    driver = get_object_or_404(Driver, id=id)  # Safely retrieve the Driver instance or return a 404 error
    if request.method == 'POST':
        form = DriverUpdateForm(request.POST, request.FILES, instance=driver)  # Populate the form with the instance data
        if form.is_valid():
            form.save()  # Save the updated driver instance
            messages.success(request, 'Driver Updated Successfully.')
    else:
        form = DriverUpdateForm(instance=driver)  # Populate the form with the existing driver data on GET request
    
    return render(request, 'admin_update_driver.html', {'form': form})


def delete_driver(request, id):
    driver = get_object_or_404(Driver, id=id)
    if driver:
        driver.delete()
        messages.success(request, 'Driver deleted successfully.')
    return redirect('/admin/drivers-list')


# vehical data start
def vehicle_list(request):
    vehicle = Vehicle.objects.select_related()
    form = VehicleForm()  # Pass the form for vehicle creation
    return render(request, "admin_vehicle_list.html", {'vehicle': vehicle, 'form': form})

def create_vehicle(request):
    if request.method == 'POST':
        form = VehicleForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                fm=form.save()
                messages.success(request,"Vehiccle created successfully!")
                return JsonResponse({'success': True, 'message': 'Vehiccle created successfully!'})
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
 

def update_vehicle(request, id):
    user = get_object_or_404(Vehicle, id=id)
    if request.method == 'POST':
        form = VehicleForm(request.POST, instance=user)  # Pre-populate the form with the user data
        if form.is_valid():
            form.save()  # Save the updated user data
            messages.success(request, "Vehicle updated successfully.")
    else:
        form = VehicleForm(instance=user)  # Pre-populate the form with existing data for GET request
    return render(request, 'admin_update_vehicle.html', {'form': form})



def import_vehicles(request):
    if request.method == "POST":
        excel_file = request.FILES.get('vehicle_file')
        if excel_file:
            try:
                workbook = openpyxl.load_workbook(excel_file)
                worksheet = workbook.active
                data_to_insert = []
                for row in worksheet.iter_rows(min_row=2, values_only=True):
                    vehicle_number = row[0]
                    vehicle_name = row[1]

                    if Vehicle.objects.filter(vehicle_number=vehicle_number).exists():
                        messages.error(request, f"Vehicle with number {vehicle_number} already exists")
                        return redirect('/admin/vehicle-list')
                    
                    if vehicle_number and vehicle_name:
                        data_to_insert.append(Vehicle(vehicle_number=vehicle_number,vehicle_name=vehicle_name))
                
                Vehicle.objects.bulk_create(data_to_insert)
                messages.success(request, 'Data Imported and Updated Successfully')
            except Exception as e:
                messages.error(request, f'Error occurred during import: {str(e)}')
        else:
            messages.error(request, 'No file selected.')
        
        return redirect('/admin/vehicle-list')
    return redirect('/admin/vehicle-list')

def delete_vehicle(request, id):
    vehicle = get_object_or_404(Vehicle, id=id)
    if vehicle:
        vehicle.delete()
        messages.success(request, 'Vehicle deleted successfully.')
    return redirect('/admin/vehicle-list')



def technician_list(request):
    technicians=cache.get('cache_technicians')
    if not technicians:
        technicians = Technician.objects.all().values(
            'id', 'technician_name', 'adhaar_number', 'mobile_number', 'email', 'address', 'date_of_birth', 'date_joined'
        )
        cache.set('cache_technicians', list(technicians), timeout=None)
    form = TechnicianRegistrationForm()
    return render(request, "admin_technician_list.html",{'form':form,'technicians':technicians})

def create_technician(request):
    if request.method == 'POST':
        form = TechnicianRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                fm=form.save()
                messages.success(request,"Technician created successfully!")
                return JsonResponse({'success': True, 'message': 'Technician created successfully!'})
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
 
 
def update_technician(request, id):
    data = get_object_or_404(Technician, id=id)
    if request.method == 'POST':
        form = TechnicianUpdateForm(request.POST, instance=data)  # Pre-populate the form with the user data
        if form.is_valid():
            form.save()  # Save the updated user data
            messages.success(request, "Technician updated successfully.")
    else:
        form = TechnicianUpdateForm(instance=data)  # Pre-populate the form with existing data for GET request
    return render(request, 'admin_update_technician.html', {'form': form})


def delete_technician(request, id):
    technician = get_object_or_404(Technician, id=id)
    if technician:
        technician.delete()
        messages.success(request, 'Technician deleted successfully.')
    return redirect('/admin/technician-list')






def party_list(request):
    partys=cache.get('cache_partys')
    if not partys:
        partys = Party.objects.all() 
        cache.set('cache_partys', list(partys), timeout=None)
    form = PartyForm()
    return render(request, "admin_party_list.html",{'form':form,'partys':partys})

def create_party(request):
    if request.method == 'POST':
        form = PartyForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                fm=form.save()
                messages.success(request,"Party created successfully!")
                return JsonResponse({'success': True, 'message': 'Party created successfully!'})
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
 



def update_party(request, id):
    data = get_object_or_404(Party, id=id)
    if request.method == 'POST':
        form = PartyForm(request.POST, instance=data)  # Pre-populate the form with the user data
        if form.is_valid():
            form.save()  # Save the updated user data
            messages.success(request, "Party updated successfully.")
    else:
        form = PartyForm(instance=data)  # Pre-populate the form with existing data for GET request
    return render(request, 'admin_update_party.html', {'form': form})



def delete_party(request, id):
    party = get_object_or_404(Party, id=id)
    if party:
        party.delete()
        messages.success(request, 'Party deleted successfully.')
    return redirect('/admin/party-list')



from rest_framework.permissions import AllowAny
from rest_framework.authtoken.views import ObtainAuthToken
 
# Create a view to handle login and return token
class CustomAuthToken(ObtainAuthToken):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        return response
 