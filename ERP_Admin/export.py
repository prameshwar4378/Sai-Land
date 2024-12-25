import openpyxl
from django.http import HttpResponse
from django.shortcuts import render
from .models import CustomUser, Vehicle, Driver, Technician, Party, Product, Purchase, JobCard
from .filters import *
 


from django.utils.timezone import localtime
from django.db.models import Sum, Count, Q, F


def export_filtered_job_cards(request):
    # Apply the same filter as in the job_card_list view
    queryset = JobCard.objects.all().order_by('id') 
    filter = JobCardFilter(request.GET, queryset=queryset)
    filtered_job_cards = filter.qs  # Filtered queryset

    # Create a new Workbook and add a sheet
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Job Cards"

    # Define the header row for the Excel sheet
    headers = ['Job Card Number', 'Technician', 'Driver', 'Created Date',  'Reported Defect', 'Completed Action', 'Completed Date', 'Vehicle', 'Status',  'Total Product Amount', "Labour Amount","Grand Total Amount" ]
    ws.append(headers)

    # Add data rows to the Excel sheet for each filtered job card
    for job_card in filtered_job_cards:
        # Convert the `date` field to naive datetime
        create_datetime = localtime(job_card.date).replace(tzinfo=None) if job_card.date else ""
        completed_datetime = localtime(job_card.completed_date).replace(tzinfo=None) if job_card.completed_date else ""
        
        items = JobCardItem.objects.filter(job_card=job_card).order_by('-id')
        total_cost = items.aggregate(Sum('total_cost'))['total_cost__sum']
        total_cost = int(total_cost) if total_cost is not None else 0
        labour_cost=int(job_card.labour_cost) if job_card.labour_cost is not None else 0
        grand_total_cost=int(total_cost+labour_cost)
        row = [
            job_card.job_card_number,
            job_card.technician.technician_name if job_card.technician else "",
            job_card.driver.driver_name if job_card.driver else "",
            create_datetime,  
            job_card.reported_defect,
            job_card.completed_action,
            completed_datetime,
            job_card.vehicle.vehicle_name if job_card.vehicle else "",
            job_card.status,
            total_cost,
            labour_cost,
            grand_total_cost,
        ]
        ws.append(row)

    # Create an HTTP response with the Excel file content
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=job_cards.xlsx'

    # Save the workbook to the response
    wb.save(response)

    return response


def export_purchase_data(request):
    # Apply the same filter as in the job_card_list view
    queryset = Purchase.objects.all().order_by('id') 
    filter = PurchaseFilter(request.GET, queryset=queryset)
    filtered_data = filter.qs  # Filtered queryset

    # Create a new Workbook and add a sheet
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Purchase Data"

    # Define the header row for the Excel sheet
    headers = ['Bill Number', 'Supplier Name', 'Bill Type', 'Bill Date',  'Total Amount']
    ws.append(headers)

    # Add data rows to the Excel sheet for each filtered job card
    for data in filtered_data:
        # Convert the `date` field to naive datetime
        # date = localtime(data.bill_date).replace(tzinfo=None) if data.bill_date else ""
 
        row = [
            data.bill_no,
            data.supplier_name if data.supplier_name else "",
            data.bill_type,
            data.bill_date,
            data.total_cost,
        ]
        ws.append(row)

    # Create an HTTP response with the Excel file content
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=Purchase.xlsx'

    # Save the workbook to the response
    wb.save(response)

    return response




def export_product_data(request):
    # Fetch all products or apply filters if needed
    queryset = Product.objects.all().order_by('id')

    # Create a new Workbook and add a sheet
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Product Data"

    # Define the header row for the Excel sheet
    headers = [
        'Product Code', 'Product Name', 'Model', 'Description', 
        'Sale Price', 'Minimum Stock Alert', 'Available Stock'
    ]
    ws.append(headers)

    # Add data rows to the Excel sheet for each product
    for product in queryset:
        row = [
            product.product_code,
            product.product_name,
            product.model.model_name if product.model else "N/A",  # Access related `model_name`
            product.description if product.description else "",
            product.sale_price if product.sale_price else 0.00,
            product.minimum_stock_alert,
            product.available_stock,
        ]
        ws.append(row)

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=ProductData.xlsx'
    wb.save(response)
    return response





def export_vehicle_data(request):
    # Fetch all vehicles from the database
    queryset = Vehicle.objects.all().order_by('id')

    # Create a new Workbook and add a sheet
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Vehicle Data"

    # Define the header row for the Excel sheet
    headers = ['ID', 'Vehicle Name', 'Vehicle Number']
    ws.append(headers)

    # Add data rows to the Excel sheet for each vehicle
    for vehicle in queryset:
        row = [
            vehicle.id,
            vehicle.vehicle_name,
            vehicle.vehicle_number,
        ]
        ws.append(row)

    # Create an HTTP response with the Excel file content
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=VehicleData.xlsx'

    # Save the workbook to the response
    wb.save(response)

    return response