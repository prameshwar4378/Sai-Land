from django.shortcuts import render,redirect,get_object_or_404
from .forms import *
from django.http import JsonResponse
from ERP_Admin.models import Product,Model,Purchase,JobCard
import openpyxl
from django.contrib import messages
from django.core.cache import cache
from django.db.models import Sum
from .filters import *
from django.db.models import Count
from django.db.models import F
 
 #Rameshwar Pawar Updated


 #this is my second changes 
 
def dashboard(request):
    total_products = Product.objects.count()

    out_of_stock_count = Product.objects.filter(available_stock__lt=F('minimum_stock_alert')).count()

    # Count of Running Job Cards (Job cards where status is 'running')
    running_job_cards_count = JobCard.objects.exclude(status='completed').count()

    # Count of Completed Job Cards (Job cards where status is 'completed')
    completed_job_card_count = JobCard.objects.filter(status='completed').count()

    # Pass data to the template
    context = {
        'out_of_stock_count': out_of_stock_count,
        'running_job_cards_count': running_job_cards_count,
        'completed_job_card_count': completed_job_card_count,
        'total_products':total_products,
    }
    return render(request, "workshop_dashboard.html", context)


def breakdown_alerts(request):
    return render(request, "workshop_breakdown_alerts.html")


from django.core.paginator import Paginator

def job_card_list(request):
    form = JobCardForm()
    queryset = JobCard.objects.all().order_by('-id') 
    filter = JobCardFilter(request.GET, queryset=queryset)
    filtered_job_cards = filter.qs  # Filtered queryset
    
    # Pagination
    paginator = Paginator(filtered_job_cards, 10)  # Show 10 job cards per page.
    page_number = request.GET.get('page')  # Get the page number from the GET request
    page_obj = paginator.get_page(page_number)  # Get the corresponding page object
    
    # Include the filter parameters in the pagination context
    filter_params = request.GET.copy()  # Copy the GET parameters
    if 'page' in filter_params:
        del filter_params['page']  # Remove the page parameter if it exists
    
    return render(request, "workshop_job_card_list.html", {
        'form': form,
        'job_card': page_obj,  # Pass the paginated object to the template
        'filter': filter,  # Pass the filter object for displaying the form
        'filter_params': filter_params.urlencode(),  # Pass the filter parameters for pagination
    })


def create_job_card(request):
    if request.method == 'POST':
        form = JobCardForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                form.save()
                messages.success(request,"Job Card created successfully!")
                return JsonResponse({'success': True, 'message': 'Form Submited'}, status=200)
                # return redirect('/workshop/jobcard-list/')
            except ValidationError as e:
                # Handle explicit model-level validation errors
                print("SUcess 3")
                return JsonResponse({'success': False, 'errors': {'non_field_errors': str(e)}}, status=400)
        else:
            # Handle form errors, including unique constraint violations
            print("SUcess 4")
            errors = {
                field: [str(error) for error in error_list]
                for field, error_list in form.errors.items()
            }
            return JsonResponse({'success': False, 'errors': errors}, status=400)
    return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=405)


def update_job_card(request, id):
    job_card = JobCard.objects.get(id=id)  # Retrieve the JobCard instance
    if request.method == 'POST':
        form = JobCardForm(request.POST, instance=job_card)
        if form.is_valid():
            form.save()
            messages.success(request, 'Job Card Updated successfully.')
            return redirect(f'/workshop/update_job_card/{id}')  # Redirect to a list view or other desired page
    else:
        form = JobCardForm(instance=job_card)
    return render(request, 'workshop_update_job_card.html', {'form': form})

def delete_job_card(request, id):
    job_card = get_object_or_404(JobCard, id=id)
    if job_card.items.exists():
        messages.error(request, 'Job Card has associated items. Please remove all items before deleting it.')
        return redirect('/workshop/job_card_list')
    try:
        with transaction.atomic():
            job_card.delete()
            messages.success(request, 'Job Card deleted successfully.')
    except Exception as e:
        messages.error(request, f"Error deleting Job Card: {str(e)}")
    return redirect('/workshop/job_card_list')


def job_card_item_list(request, id):
    job_card = get_object_or_404(JobCard, id=id)
    close_job_card_form=CloseJobCardForm(instance=job_card)
    items = JobCardItem.objects.filter(job_card=job_card).order_by('-id')
    total_cost = items.aggregate(Sum('cost'))['cost__sum']
    total_cost = int(total_cost) if total_cost is not None else 0

    total_cost=None
    labour_cost=None
    grand_total_cost=None

    product_data = cache.get('product_data')
    if not product_data:
        product_data = list(Product.objects.all())
        cache.set('product_data', product_data, timeout=300)

    if request.method == 'POST':
        form = JobCardItemForm(request.POST)
        product_id = request.POST.get('product_id')
        if form.is_valid():
            item = form.save(commit=False)
            item.job_card = job_card
            item.product = Product.objects.get(id=product_id)
            item.save()

            items = JobCardItem.objects.filter(job_card=job_card).order_by('-id')
            total_cost = items.aggregate(Sum('total_cost'))['total_cost__sum']
            total_cost = int(total_cost) if total_cost is not None else 0
            labour_cost=int(job_card.labour_cost) if job_card.labour_cost is not None else 0
            grand_total_cost=int(total_cost+labour_cost)

        else:
            print("Form errors:", form.errors)
    else:
        items = JobCardItem.objects.filter(job_card=job_card).order_by('-id')
        total_cost = items.aggregate(Sum('total_cost'))['total_cost__sum']
        total_cost = int(total_cost) if total_cost is not None else 0
        labour_cost=int(job_card.labour_cost) if job_card.labour_cost is not None else 0
        grand_total_cost=int(total_cost+labour_cost)

    form = JobCardItemForm()

    return render(request, "workshop_job_card_item_list.html", {
        'form': form,
        'close_job_card_form':close_job_card_form,
        'items': items,
        'job_card': job_card,
        'product_data': product_data,
        'total_cost': total_cost,
        'labour_cost':labour_cost,
        'grand_total_cost':grand_total_cost
    })


def delete_job_card_item(request, id):
    item = get_object_or_404(JobCardItem, id=id)
    job_card_id=item.job_card.id
    if item:
        item.delete()
        messages.success(request, 'Item deleted successfully.')
    return redirect(f'/workshop/job_card_item_list/{job_card_id}')


def close_job_card(request):
    if request.method == 'POST':
        job_card_id=request.POST.get('job_card_id')
        job_card = JobCard.objects.get(id=job_card_id)  # Retrieve the JobCard instance
        form = CloseJobCardForm(request.POST,instance=job_card)
        if form.is_valid():
                form.save()
                messages.success(request, 'Job Card Closed successfully.')
                return redirect(f'/workshop/job_card_item_list/{job_card_id}')
        else: 
                messages.error(request, 'Error occur.')
                return redirect(f'/workshop/job_card_item_list/{job_card_id}')
    return redirect('/workshop/job_card_list/')

def print_job_card(request, id):
    job_card = JobCard.objects.get(id=id)
    items = JobCardItem.objects.filter(job_card=job_card).order_by('-id')

    # Calculating total cost
    total_cost = items.aggregate(Sum('total_cost'))['total_cost__sum']
    total_cost = int(total_cost) if total_cost is not None else 0

    # Calculating total quantity, total rate (cost), and taxable amount
    total_quantity = items.aggregate(Sum('quantity'))['quantity__sum'] or 0
    total_rate = items.aggregate(Sum('cost'))['cost__sum'] or 0
    total_taxable_amount = total_cost

    # Labour cost and grand total
    labour_cost = int(job_card.labour_cost) if job_card.labour_cost else 0
    grand_total_cost = int(total_cost + labour_cost)  

    return render(request, "workshop_print_job_card.html", {
        'job_card': job_card,
        'items': items,
        'total_cost': total_cost,
        'total_quantity': total_quantity,
        'total_rate': total_rate,
        'total_taxable_amount': total_taxable_amount,
        'labour_cost': labour_cost,
        'grand_total_cost': grand_total_cost
    })

def maintenance_logs(request):
    return render(request, "workshop_maintenance_logs.html")

def maintenance_schedule(request):
    return render(request, "workshop_maintenance_schedule.html")

def product_list(request):
    # products = Product.objects.all().delete()
    form = ProductForm()
    # products = cache.get('cache_products')
    products = Product.objects.select_related("model").order_by("-id")

    # if not products: 
    #     products = list(Product.objects.all().order_by('-id').values())
    #     cache.set('cache_products', products, timeout=None)
    
    return render(request, "workshop_product_list.html", {'form': form, 'product': products})


def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST,request.FILES)
        if form.is_valid():
            try:
                product_instance = form.save()
                if product_instance.product_image:
                    file_path = product_instance.product_image.path
                    print(f"Received file path: {file_path}")
                    
                return JsonResponse({'success': True, 'message': 'Product created successfully!'})
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


def update_product(request, id):
    product = Product.objects.get(id=id)  # Retrieve the JobCard instance
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product Updated Successfully.')
    else:
        form = ProductForm(instance=product)
    return render(request, 'workshop_update_product.html', {'form': form})



def import_products(request):
    if request.method == "POST":
        excel_file = request.FILES.get('product_file')
        if excel_file:
            try:
                # Load the Excel workbook
                workbook = openpyxl.load_workbook(excel_file)
                worksheet = workbook.active
                
                data_to_insert = []
                model_cache = {}  # Cache to avoid repeated DB queries
                
                for row in worksheet.iter_rows(min_row=2, values_only=True):
                    product_code = row[0]
                    product_name = row[1]
                    model_name = row[2]  # Assuming the model name is provided in the Excel file
                    description = row[3] or ""
                    sale_price = row[4] or 0.0
                    minimum_stock_alert = row[5] or 0
                    available_stock = row[6] or 0

                    # Check if the product_code already exists
                    if Product.objects.filter(product_code=product_code).exists():
                        messages.error(request, f"Product with code {product_code} already exists")
                        return redirect('/workshop/product-list')
                    # Retrieve or create the model instance
                    if model_name not in model_cache:
                        model_instance, created = Model.objects.get_or_create(model_name=model_name)
                        model_cache[model_name] = model_instance
                    else:
                        model_instance = model_cache[model_name]

                    # Add the product data to the batch insert list
                    data_to_insert.append(
                        Product(
                            product_code=product_code,
                            product_name=product_name,
                            model=model_instance,
                            description=description,
                            sale_price=sale_price,
                            minimum_stock_alert=minimum_stock_alert,
                            available_stock=available_stock,
                        )
                    )

                # Bulk insert all the valid products
                Product.objects.bulk_create(data_to_insert)
                messages.success(request, 'Products imported successfully.')

            except Exception as e:
                messages.error(request, f"Error occurred during import: {str(e)}")
        else:
            messages.error(request, 'No file selected.')

        return redirect('/workshop/product-list')
    return redirect('/workshop/product-list')

def delete_product(request, id):
    product = get_object_or_404(Product, id=id)
    if product:
        product.delete()
        messages.success(request, 'Product deleted successfully.')
    return redirect('/workshop/product-list')


def purchase_list(request):
    form= PurchaseForm()
    purchase=Purchase.objects.all().order_by('-id')
    return render(request, "workshop_purchase_list.html",{'form':form,'purchase':purchase})

def purchase_list(request):
    form = PurchaseForm()
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
    
    return render(request, "workshop_purchase_list.html", {
        'form': form,
        'purchase': page_obj,  # Pass the paginated object to the template
        'filter': filter,  # Pass the filter object for displaying the form
        'filter_params': filter_params.urlencode(),  # Pass the filter parameters for pagination
    })


def create_purchase(request):
    if request.method == 'POST':
        form = PurchaseForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                form.save()
                messages.success(request,"Purchase created successfully!")
                return JsonResponse({'success': True, 'message': 'Form Submited'}, status=200)
                # return redirect('/workshop/purchase-list/')
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



def update_purchase(request, id):
    purchase = Purchase.objects.get(id=id)  # Retrieve the JobCard instance
    if request.method == 'POST':
        form = PurchaseForm(request.POST, request.FILES, instance=purchase)
        if form.is_valid():
            form.save()
            messages.success(request, 'Purchase Updated Successfully.')
    else:
        form = PurchaseForm(instance=purchase)
    return render(request, 'workshop_update_purchase.html', {'form': form})


def get_product_details(request):
    product_code = request.GET.get('product_code')  # Get the product code from the request
    if product_code:
            product = get_object_or_404(Product, product_code=product_code)  
            product_image_url = product.product_image.url if product.product_image else None
            data = {        
                'id': product.id,
                'product_name': product.product_name,
                'product_rate': product.sale_price,  # Ensure this field exists in your model
                'product_code': product.product_code, 
                'product_image_url':product_image_url          # Include any other necessary fields
            }    
            return JsonResponse(data, safe=False) 
    return JsonResponse({'error': 'Invalid Product Code'}, status=400)


def delete_purchase(request, id):
    purchase = get_object_or_404(Purchase, id=id)
    if purchase.items.exists():
        messages.error(request, 'Purchase has associated items. Please remove all items before deleting it.')
        return redirect('/workshop/purchase-list')
    try:
        with transaction.atomic():
            purchase.delete()
            messages.success(request, 'Purchase deleted successfully.')
    except Exception as e:
        messages.error(request, f"Error deleting Purchase: {str(e)}")
    return redirect('/workshop/purchase-list')


def purchase_item_list(request,id):
    purchase=get_object_or_404(Purchase, id=id)


    product_data = list(Product.objects.select_related('model'))
    cache.set('product_data', product_data, timeout=300)  # Store for 300 seconds
    product_data = cache.get('product_data')
    if request.method == 'POST':
        form = PurchaseItemForm(request.POST)
        product_id=request.POST.get('product_id') 
        if form.is_valid() and product_id: 
            fm=form.save(commit=False)
            fm.purchase=Purchase.objects.get(id=id)
            fm.product=Product.objects.get(id=product_id)
            fm.save()
            item=PurchaseItem.objects.filter(purchase=purchase).order_by('-id')
            total_amount = item.aggregate(Sum('total_amount'))['total_amount__sum']
            total_amount = int(total_amount) if total_amount is not None else 0  # In case there are no items, set total_amount to 0
            #update total_amount for Purchase
            purchase.total_cost = int(total_amount)
            purchase.save()
        else:
            print("Form errors:", form.errors)
    else:
            item=PurchaseItem.objects.filter(purchase=purchase).order_by('-id')
            total_amount = item.aggregate(Sum('total_amount'))['total_amount__sum']
            total_amount = int(total_amount) if total_amount is not None else 0  # In case there are no items, set total_amount to 0
            purchase.total_amount = total_amount
            purchase.save()

    form = PurchaseItemForm()
    return render(request, "workshop_purchase_item_list.html",{'form':form,'item':item,'purchase':purchase,'product_data':product_data,'total_amount':total_amount})

# def create_purchase_item(request):

#     if request.method == 'POST':
#         product_id = request.POST.get('product_id')
#         purchase_id = request.POST.get('purchase_id')
#         product_code = request.POST.get('product_code')
#         product_name = request.POST.get('product_name')
#         quantity = request.POST.get('quantity')
#         rate = request.POST.get('rate')
#         total_amount = request.POST.get('total_amount')
 
#         if not (product_code and product_name and quantity and rate and total_amount):
#             return JsonResponse({'error': 'All fields are required.'}, status=400)

#         try:
#             # Fetch the product
#             print("Enter in login")
#             product = Product.objects.get(id=product_id)
#             purchase = Purchase.objects.get(id=purchase_id)
#             # Save the purchase item
#             purchase_item = PurchaseItem.objects.create(
#                 product=product,
#                 purchase=purchase,
#                 quantity=int(quantity),
#                 cost_per_unit=float(rate),
#                 total_amount=float(total_amount)
#             )

#             return JsonResponse({'message': 'Purchase item successfully created.'}, status=201)
#         except Product.DoesNotExist:
#             return JsonResponse({'error': 'Product not found.'}, status=404)
#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=500)

#     return JsonResponse({'error': 'Invalid request method.'}, status=405)


def delete_purchase_item(request, id):
    item = get_object_or_404(PurchaseItem, id=id)
    purchase_id=item.purchase.id
    if item:
        item.delete()
        messages.success(request, 'Item deleted successfully.')
    return redirect(f'/workshop/purchase-item-list/{purchase_id}')


def reports(request):
    return render(request, "workshop_reports.html")
