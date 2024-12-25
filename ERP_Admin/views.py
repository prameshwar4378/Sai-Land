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
from django.contrib.auth.hashers import make_password

from django.core.cache import cache

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.forms.models import model_to_dict
from django.core.cache import cache
from .models import *
from django.core.paginator import Paginator
from .filters import *


# @receiver(post_save, sender=Product)
# def update_cache_on_save(sender, instance, **kwargs):
#     products = [] 
#     for product in Product.objects.select_related('model').all().order_by('-id'):
#         product_data = model_to_dict(product)
#         product_data['model'] = {
#             'model_name': product.model.model_name,   
#         }
#         products.append(product_data)
#     cache.set('cache_products', products, timeout=None)

# @receiver(post_delete, sender=Product)
# def update_cache_on_delete(sender, instance, **kwargs):
#     update_cache_on_save(sender, instance)  #  


@receiver(post_save, sender=Driver)
def update_driver_cache_on_save(sender, instance, **kwargs):
    # Retrieve all drivers and include all fields
    drivers = Driver.objects.select_related('user').all()
    
    # Use model_to_dict to serialize the driver model and its related data
    from django.forms.models import model_to_dict
    driver_data = [model_to_dict(driver) for driver in drivers]

    # Update the cache with all driver data, including related CustomUser fields
    cache.set('cache_drivers', driver_data, timeout=None)
    print("Driver cache updated on save")

@receiver(post_delete, sender=Driver)
def update_driver_cache_on_delete(sender, instance, **kwargs):
    # Retrieve all drivers and include all fields
    drivers = Driver.objects.select_related('user').all()

    # Serialize the driver model data into dictionary format
    from django.forms.models import model_to_dict
    driver_data = [model_to_dict(driver) for driver in drivers]

    # Update the cache to reflect the deletion
    cache.set('cache_drivers', driver_data, timeout=None)
    print("Driver cache updated on delete")


@receiver(post_save, sender=Technician)
def update_technician_cache_on_save(sender, instance, **kwargs):
    # Retrieve all technicians and include all fields
    technicians = Technician.objects.all()
    
    # Use model_to_dict to serialize the technician model
    from django.forms.models import model_to_dict
    technician_data = [model_to_dict(technician) for technician in technicians]

    # Update cache with the latest technician data
    cache.set('cache_technicians', technician_data, timeout=None)
    print("Technician cache updated on save")

@receiver(post_delete, sender=Technician)
def update_technician_cache_on_delete(sender, instance, **kwargs):
    # Retrieve all technicians and include all fields
    technicians = Technician.objects.all()

    # Serialize the technician model data into dictionary format
    from django.forms.models import model_to_dict
    technician_data = [model_to_dict(technician) for technician in technicians]

    # Update the cache to reflect the deletion
    cache.set('cache_technicians', technician_data, timeout=None)
    print("Technician cache updated on delete")




@receiver(post_save, sender=Party)
def update_party_cache_on_save(sender, instance, **kwargs):
    # Retrieve all partys data and serialize it if needed
    party = Party.objects.all()
    # Serialize the technician model data into dictionary format
    from django.forms.models import model_to_dict
    party_data = [model_to_dict(party) for party in party]


    print("Party cache updated on save")

@receiver(post_delete, sender=Party)
def update_party_cache_on_delete(sender, instance, **kwargs):
    # Retrieve all partys data after delete
    partys = []
    for partys in Party.objects.all(): 
        party_data = model_to_dict(partys)  # Convert technician to dictionary
        partys.append(party_data)
    cache.set('cache_technicians', partys, timeout=None)


def reload_all_caches(request):
    # Reload Product cache (storing all data as dictionaries)
    products = []
    for product in Product.objects.all().order_by('-id'):
        product_data = model_to_dict(product)  # Convert product to dictionary
        products.append(product_data)
    cache.set('cache_products', products, timeout=None)
    print("Product cache reloaded")

    # Reload Driver cache (storing all data as dictionaries)
    drivers = []
    for driver in Driver.objects.select_related('user').all():  # Add related fields
        driver_data = model_to_dict(driver)  # Convert driver to dictionary
        # If you want to include related fields more explicitly, you can manually add them here
        driver_data['user'] = model_to_dict(driver.user)  # Include related user data
        drivers.append(driver_data)
    cache.set('cache_drivers', drivers, timeout=None)
    print("Driver cache reloaded")

    # Reload Technician cache (storing all data as dictionaries)
    technicians = []
    for technician in Technician.objects.all():
        technician_data = model_to_dict(technician)  # Convert technician to dictionary
        technicians.append(technician_data)
    cache.set('cache_technicians', technicians, timeout=None)
    print("Technician cache reloaded")

    # Reload Party cache (storing all data as dictionaries)
    partys = []
    for party in Party.objects.all():
        party_data = model_to_dict(party)  # Convert party to dictionary
        partys.append(party_data)
    cache.set('cache_partys', partys, timeout=None)
    print("Party cache reloaded")
    return redirect('/admin/dashboard')




def login(request): 
    if request.user.is_authenticated:
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
    if user.is_superuser or user.is_admin:
        print('Redirecting to Admin Dashboard')  # Debug print
        return redirect('/admin/dashboard')
    elif user.is_workshop:
        print('Redirecting to Workshop Dashboard')  # Debug print
        return redirect('/workshop/dashboard')
    elif user.is_account:
        print('Redirecting to Account Dashboard')  # Debug print
        return redirect('/account/dashboard')
    elif user.is_driver:
        print('Redirecting to Account Dashboard')  # Debug print
        return redirect('/driver/dashboard')
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
    products = Product.objects.select_related("model").order_by("-id")
    # products = cache.get('cache_products')
 
    # Variables for counts
    out_of_stock = 0
    minimum_stock_alert_count = 0
    total_available_stock = 0

    # if not products:
    #     # Query all products and store in cache
    #     products = list(Product.objects.all().order_by('-id').values())
    #     # cache.set('cache_products', products, timeout=None)

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
    return render(request, "admin_user_management.html",{'form':form,'users':users})

def create_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            try:
                fm=form.save(commit=False)
                last_emp_id = EMP_ID.objects.order_by('-id').first()

                if last_emp_id:
                    last_number = int(last_emp_id.emp_id.split('-')[1])
                    new_emp_id = EMP_ID.objects.create(emp_id=f"SLD-{last_number + 1}")
                else:
                    new_emp_id = EMP_ID.objects.create(emp_id="SLD-1")
                fm.emp_id=new_emp_id
                fm.save()
                messages.success(request, "User Added successfully.")
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
        user.delete()
        messages.success(request, 'User deleted successfully.')

def drivers_list(request):
    drivers = Driver.objects.select_related('user').all()
    form = DriverRegistrationForm()
    incomplete_profile = CustomUser.objects.filter(driver__isnull=True, is_driver=True).delete()[0]
    return render(request, "admin_drivers_list.html", {'form': form, 'drivers': drivers})


def create_driver(request):
    if request.method == 'POST':
        form = DriverRegistrationForm(request.POST, request.FILES)
        
        if form.is_valid():
            try:
                with transaction.atomic():

                    form.save()
                    return JsonResponse({'success': True, 'message': 'Driver created successfully!'})
            except ValidationError as e:
                # Handle explicit model-level validation errors
                return JsonResponse({'success': False, 'errors': {'non_field_errors': str(e)}}, status=400)
            except Exception as e:
                # Catch any unexpected errors and return a 500 response
                return JsonResponse({'success': False, 'message': str(e)}, status=500)
        else:
            # Handle form errors
            errors = {
                field: [str(error) for error in error_list]
                for field, error_list in form.errors.items()
            }
            return JsonResponse({'success': False, 'errors': errors}, status=400)
    
    # If the request method is not POST, return a method not allowed response
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


def import_drivers(request):
    if request.method == "POST":
        excel_file = request.FILES.get('Driver_file')
        password=make_password('Pass@123')
        if excel_file:
            try:
                # Load the Excel file
                workbook = openpyxl.load_workbook(excel_file)
                worksheet = workbook.active
                
                # List to hold the data to insert into the database
                data_to_insert = []
                
                # Iterate over each row in the Excel sheet (skipping header row)
                for row in worksheet.iter_rows(min_row=2, values_only=True):
                    driver_name = row[1]  # Assuming driver_name is in the first column
                    adhaar_number = row[2] if row[2] else None  # Assuming adhaar_number is in the second column
                    license_number = row[3] if row[3] else None  # Assuming license_number is in the third column
                    date_of_birth = row[4] if row[4] else None  # Assuming date_of_birth is in the fourth column
                    mobile_number = row[5] if row[5] else None  # Assuming mobile_number is in the fifth column
                    date_joined = row[6] if row[6] else None  # Assuming date_joined is in the seventh column
                 
                    # Check if the Aadhaar number is already used as a username in CustomUser
                    if adhaar_number:
                        if CustomUser.objects.filter(username=adhaar_number).exists():
                            print(f"Aadhaar number {adhaar_number} is already registered.")  # Print the error
                            messages.error(request, f"Aadhaar number {adhaar_number} is already registered.")
                            continue  # Skip to the next row if Aadhaar number exists
                        username = adhaar_number  # Use Aadhaar number as the username
                    else:
                        # If Aadhaar number is not available, use mobile number as the username
                        if CustomUser.objects.filter(username=mobile_number).exists():
                            print(f"Mobile number {mobile_number} is already registered.")  # Print the error
                            messages.error(request, f"Mobile number {mobile_number} is already registered.")
                            continue  # Skip to the next row if mobile number exists
                        username = mobile_number  # Use mobile number as the username

                    # Create the EMP_ID instance if it doesn't exist
                    last_emp_id = EMP_ID.objects.order_by('-id').first()
                    if last_emp_id:
                        last_number = int(last_emp_id.emp_id.split('-')[1])
                        new_emp_id = EMP_ID.objects.create(emp_id=f"SLD-{last_number + 1}")
                    else:
                        new_emp_id = EMP_ID.objects.create(emp_id="SLD-1")


                    # Create or update the user (CustomUser)
                    user, created = CustomUser.objects.get_or_create(
                        username=username,  # Set the username to Aadhaar number or mobile number
                        # defaults={'is_driver': True, 'password': make_password('Pass@123')}  # Mark as driver if creating a new user
                        is_driver=True,
                        password=password,
                        emp_id=new_emp_id
                    )
                    
                    if not created:  # If user already exists, update is_driver to True
                        user.is_driver = True
                        user.save()

                    # Create the Driver instance
                    driver = Driver(
                        user=user,  # Set the user
                        driver_name=driver_name,  # Set driver name
                        license_number=license_number,  # Set driving license number
                        adhaar_number=adhaar_number,  # Set Adhaar number
                        mobile_number=mobile_number,  # Set mobile number
                        date_of_birth=date_of_birth,  # Set date of birth
                        date_joined=date_joined  # Set date joined
                    )
                    data_to_insert.append(driver)
 
                if data_to_insert:
                    Driver.objects.bulk_create(data_to_insert)
                    messages.success(request, 'Drivers data imported and updated successfully.')
                else:
                    messages.error(request, 'No data to import.')

            except Exception as e:
                print(f"Error occurred during import: {str(e)}")  # Print the exception error
                messages.error(request, f'Error occurred during import: {str(e)}')
        else:
            print("No file selected.")  # Print error if no file selected
            messages.error(request, 'No file selected.')

        return redirect('/admin/drivers-list')  # Redirect to the admin driver list page
    return redirect('/admin/drivers-list')  # Redirect if not a POST request



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
    technicians=Technician.objects.select_related('emp_id')
    form = TechnicianRegistrationForm()
    return render(request, "admin_technician_list.html",{'form':form,'technicians':technicians})

def create_technician(request):
    if request.method == 'POST':
        form = TechnicianRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                fm=form.save(commit=False)
                last_emp_id = EMP_ID.objects.order_by('-id').first()

                if last_emp_id:
                    last_number = int(last_emp_id.emp_id.split('-')[1])
                    new_emp_id = EMP_ID.objects.create(emp_id=f"SLD-{last_number + 1}")
                else:
                    new_emp_id = EMP_ID.objects.create(emp_id="SLD-1")
                fm.emp_id=new_emp_id
                fm.save()
                
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
    partys=Party.objects.all()
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
 

def vehicle_data(request):
    vehicle_data = Vehicle.objects.all()

    vehicle_number = request.GET.get('vehicle_number', '').strip()
    vehicle = None
    job_cards = []
    total_labour_cost = 0
    total_item_cost = 0
    grand_total_cost = 0

    try:
        if vehicle_number:
            # Get the vehicle by its vehicle_number
            vehicle = Vehicle.objects.filter(vehicle_number__iexact=vehicle_number).first()
            
            if vehicle:
                # Query job cards related to this vehicle
                job_cards = JobCard.objects.filter(vehicle=vehicle)
                
                for job_card in job_cards:
                    # Aggregate total item cost for the current job card
                    items = JobCardItem.objects.filter(job_card=job_card)
                    item_cost = items.aggregate(Sum('total_cost'))['total_cost__sum'] or 0
                    
                    # Labour cost for the current job card
                    labour_cost = job_card.labour_cost or 0
                    
                    # Update totals
                    total_labour_cost += labour_cost
                    total_item_cost += item_cost

                # Grand total cost (labour + items)
                grand_total_cost = total_labour_cost + total_item_cost

    except Exception as e:
        # Log the exception if needed (e.g., with logging)
        return render(request, '404.html', {})

    context = {
        'vehicle': vehicle,
        'job_card_count': len(job_cards),
        'total_labour_cost': int(total_labour_cost),
        'total_item_cost': int(total_item_cost),
        'grand_total_cost': int(grand_total_cost),
        'job_cards': job_cards,
        'vehicle_data' : vehicle_data,
        'is_vehicle_data' : vehicle_number
    }
    return render(request, 'admin_vehicle_dashboard.html', context)



