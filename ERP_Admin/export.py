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


from django.conf import settings
def export_driver_data(request):
    # Fetch all drivers from the database
    queryset = Driver.objects.all().order_by('id')
    # Create a new Workbook and add a sheet
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Driver Data"

    # Define the header row for the Excel sheet
    headers = [
        'ID','EMP ID', 'Driver Name', 'License Number', 'Adhaar Number', 
        'Mobile Number', 'Alternate Mobile Number', 'Address', 
        'Date of Birth', 'Date Joined', 'Adhaar Card Photo', 
        'PAN Card Photo', 'Driving License Photo', 'Profile Photo'
    ]

    ws.append(headers)
    # Add data rows to the Excel sheet for each driver
    for driver in queryset:
        row = [
            driver.id,
            str(driver.user.emp_id) if str(driver.user.emp_id) else "",
            driver.driver_name,
            driver.license_number if driver.license_number else "",
            driver.adhaar_number if driver.adhaar_number else "",
            driver.mobile_number if driver.mobile_number else "",
            driver.alternate_mobile_number if driver.alternate_mobile_number else "",
            driver.address if driver.address else "",
            driver.date_of_birth if driver.date_of_birth else "",
            driver.date_joined if driver.date_joined else "",
            request.build_absolute_uri(driver.adhaar_card_photo.url) if driver.adhaar_card_photo else "",
            request.build_absolute_uri(driver.pan_card_photo.url) if driver.pan_card_photo else "",
            request.build_absolute_uri(driver.driving_license_photo.url) if driver.driving_license_photo else "",
            request.build_absolute_uri(driver.profile_photo.url) if driver.profile_photo else "",
        ]
        ws.append(row)

    # Create an HTTP response with the Excel file content
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=DriverData.xlsx'

    # Save the workbook to the response
    wb.save(response)

    return response




def export_technician_data(request):
    # Fetch all technicians from the database
    queryset = Technician.objects.all().order_by('id')

    # Create a new Workbook and add a sheet
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Technician Data"

    # Define the header row for the Excel sheet
    headers = [
        'EMP ID', 'Technician Name', 'Aadhaar Number', 'Mobile Number', 
        'Alternate Mobile Number', 'Email Address', 'Address', 
        'Date of Birth', 'Date Joined', 'PAN Card', 'Aadhaar Card', 
        'Profile Photo', 'Additional Docs'
    ]
    ws.append(headers)

    # Add data rows to the Excel sheet for each technician
    for technician in queryset:
        row = [
            str(technician.emp_id)  if str(technician.email) else "",
            technician.technician_name,
            technician.adhaar_number,
            technician.mobile_number,
            technician.alternate_mobile_number if technician.alternate_mobile_number else "",
            technician.email if technician.email else "",
            technician.address if technician.address else "",
            technician.date_of_birth if technician.date_of_birth else "",
            technician.date_joined if technician.date_joined else "",
            request.build_absolute_uri(technician.pan_card.url) if technician.pan_card else "",
            request.build_absolute_uri(technician.adhaar_card.url) if technician.adhaar_card else "",
            request.build_absolute_uri(technician.profile_photo.url) if technician.profile_photo else "",
            request.build_absolute_uri(technician.additional_docs.url) if technician.additional_docs else "",
        ]
        ws.append(row)

    # Create an HTTP response with the Excel file content
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=TechnicianData.xlsx'

    # Save the workbook to the response
    wb.save(response)

    return response




def export_party_data(request):
    # Fetch all parties from the database
    queryset = Party.objects.all().order_by('id')

    # Create a new Workbook and add a sheet
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Party Data"

    # Define the header row for the Excel sheet
    headers = [
        'ID', 'Business Name', 'Customer Name', 'GST Number', 
        'Mobile Number', 'Alternate Mobile Number', 'Address', 
        'Document 1', 'Document 2', 'Document 3'
    ]
    ws.append(headers)

    # Add data rows to the Excel sheet for each party
    for party in queryset:
        row = [
            party.id,
            party.business_name,
            party.customer_name,
            party.gst_number if party.gst_number else "",
            party.mobile_number,
            party.alternate_mobile_number if party.alternate_mobile_number else "",
            party.address if party.address else "",
            request.build_absolute_uri(party.document1.url) if party.document1 else "",
            request.build_absolute_uri(party.document2.url) if party.document2 else "",
            request.build_absolute_uri(party.document3.url) if party.document3 else "",
        ]
        ws.append(row)

    # Create an HTTP response with the Excel file content
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=PartyData.xlsx'

    # Save the workbook to the response
    wb.save(response)

    return response