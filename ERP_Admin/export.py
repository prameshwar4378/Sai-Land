import openpyxl
from django.http import HttpResponse
from django.shortcuts import render
from .models import CustomUser, Vehicle, Driver, Technician, Party, Product, Purchase, JobCard
from .filters import *


def export_custom_user_to_excel(request):
    # Create a new Workbook and add a sheet
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Custom Users"

    # Define the header row for the Excel sheet
    headers = ['ID', 'Username', 'Email', 'First Name', 'Last Name', 'Is Admin', 'Is Account', 'Is Workshop', 'Is Driver', 'Employee ID']
    ws.append(headers)

    # Fetch the CustomUser objects from the database
    users = CustomUser.objects.all()

    # Add data rows to the Excel sheet
    for user in users:
        row = [
            user.id,
            user.username,
            user.email,
            user.first_name,
            user.last_name,
            user.is_admin,
            user.is_account,
            user.is_workshop,
            user.is_driver,
            user.emp_id.emp_id if user.emp_id else ""
        ]
        ws.append(row)

    # Create an HTTP response with the Excel file content
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=custom_users.xlsx'

    # Save the workbook to the response
    wb.save(response)

    return response



def export_vehicle_to_excel(request):
    # Create a new Workbook and add a sheet
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Vehicles"

    # Define the header row for the Excel sheet
    headers = ['ID', 'Vehicle Name', 'Vehicle Number']
    ws.append(headers)

    # Fetch the Vehicle objects from the database
    vehicles = Vehicle.objects.all()

    # Add data rows to the Excel sheet
    for vehicle in vehicles:
        row = [
            vehicle.id,
            vehicle.vehicle_name,
            vehicle.vehicle_number
        ]
        ws.append(row)

    # Create an HTTP response with the Excel file content
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=vehicles.xlsx'

    # Save the workbook to the response
    wb.save(response)

    return response




def export_driver_to_excel(request):
    # Create a new Workbook and add a sheet
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Drivers"

    # Define the header row for the Excel sheet
    headers = ['ID', 'Driver Name', 'License Number', 'Aadhaar Number', 'Mobile Number', 'Alternate Mobile', 'Date of Birth', 'Date Joined']
    ws.append(headers)

    # Fetch the Driver objects from the database
    drivers = Driver.objects.all()

    # Add data rows to the Excel sheet
    for driver in drivers:
        row = [
            driver.id,
            driver.driver_name,
            driver.license_number,
            driver.adhaar_number,
            driver.mobile_number,
            driver.alternate_mobile_number,
            driver.date_of_birth,
            driver.date_joined
        ]
        ws.append(row)

    # Create an HTTP response with the Excel file content
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=drivers.xlsx'

    # Save the workbook to the response
    wb.save(response)

    return response





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
    headers = ['Job Card Number', 'Technician', 'Driver', 'Date', 'Reported Defect', 'Completed Action', 'Vehicle', 'Status', 'Labour Cost']
    ws.append(headers)

    # Add data rows to the Excel sheet for each filtered job card
    for job_card in filtered_job_cards:
        row = [
            job_card.job_card_number,
            job_card.technician.technician_name if job_card.technician else "",
            job_card.driver.driver_name if job_card.driver else "",
            job_card.date,
            job_card.reported_defect,
            job_card.completed_action,
            job_card.vehicle.vehicle_name if job_card.vehicle else "",
            job_card.status,
            job_card.labour_cost
        ]
        ws.append(row)

    # Create an HTTP response with the Excel file content
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=filtered_job_cards.xlsx'

    # Save the workbook to the response
    wb.save(response)

    return response
