

 
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from ERP_Admin.models import *
from .serializers import *
from django.utils.timezone import now
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate
from django.utils import timezone
from SLD.settings import BASE_DIR
from rest_framework.exceptions import NotFound

from ERP_Admin.views import send_email_in_background
from django.conf import settings
import threading
from django.core.mail import EmailMessage
from django.template.loader import render_to_string


@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')  
    if not username or not password:
        raise AuthenticationFailed('Username and password are required')
    user = authenticate(username=username, password=password)
    if user is None:
        raise AuthenticationFailed('Invalid credentials')
    token, created = Token.objects.get_or_create(user=user)
    user_id=token.user.id
    custom_user=get_object_or_404(CustomUser,id=user_id)
    if custom_user.is_admin:
        role='admin'
        profile_image_url = custom_user.profile_photo.url if custom_user.profile_photo else None
        name=f'{custom_user.first_name} {custom_user.last_name}'
    elif custom_user.is_fuel:
        role='fuel'
        profile_image_url = custom_user.profile_photo.url if custom_user.profile_photo else None
        name=f'{custom_user.first_name} {custom_user.last_name}'
    elif custom_user.is_driver:
        role='driver' 
        driver=get_object_or_404(Driver,user=custom_user.id)
        profile_image_url = driver.profile_photo.url if driver.profile_photo else None

        allocated_vehicle=AllocateDriverToVehicle.objects.filter(driver=driver,is_active=True).last()

        allocated_vehicle_data=[]

        if allocated_vehicle:
            allocated_vehicle_data.append(
                {
                    'vehicle_number':allocated_vehicle.vehicle.vehicle_number,
                    'vehicle_id':allocated_vehicle.vehicle.id,
                    "joining_date_time": allocated_vehicle.joining_date_time,

                 }
                )

        name=f'{driver.driver_name}'

        response_data = {
            'token': token.key,
            'role': role,
            'name':name, 
            'emp_id':custom_user.emp_id.emp_id,
            'user_id':custom_user.id,
            'profile_image':profile_image_url,
            'allocated_vehicle_data':allocated_vehicle_data
        }
        return Response(response_data, status=status.HTTP_200_OK)

    elif custom_user.is_workshop:
        role='workshop'
        profile_image_url = custom_user.profile_photo.url if custom_user.profile_photo else None
        name=f'{custom_user.first_name} {custom_user.last_name}'
    else:
        raise AuthenticationFailed('Android Login not available for this role..!')
    
    response_data = {
        'token': token.key,
        'role': role,
        'name':name, 
        'emp_id':custom_user.emp_id.emp_id,
        'user_id':custom_user.id,
        'profile_image':profile_image_url,

    }
    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_vehicle_details(request):
    try:
        vehicle_number = request.query_params.get('vehicle_number')
        if not vehicle_number:
            return Response({'error': 'Vehicle number is required'}, status=status.HTTP_400_BAD_REQUEST)

        vehicle = Vehicle.objects.filter(vehicle_number=vehicle_number).first()
        if not vehicle:
            raise NotFound(f'Vehicle with number {vehicle_number} does not exist')

        response_data = {
            'vehicle_number': vehicle.vehicle_number,
            'vehicle_name': vehicle.model_name.model_name,  
            'vehicle_id': vehicle.id,  
        }
        return Response(response_data, status=status.HTTP_200_OK)
    
    except NotFound as e:
        return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': 'An unexpected error occurred', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

 

@api_view(['POST'])
def allocate_driver_to_vehicle(request):
    """
    This API allocates a vehicle to a driver based on the provided user token.
    """ 
    token = request.data.get('token')
    vehicle_id = request.data.get('vehicle_id') 

    # Retrieve the user associated with the token
    user = get_object_or_404(Token, key=token)
 
    if not token: 
        return Response({"detail": "Token is required."}, status=status.HTTP_400_BAD_REQUEST)
     
    if not vehicle_id: 
        return Response({"detail": "Vehicle ID is required."}, status=status.HTTP_400_BAD_REQUEST)
    
    # Check if the user is a driver
    if not user.user.is_driver: 
        return Response({"detail": "Not Valid Token For Driver."}, status=status.HTTP_400_BAD_REQUEST)
 
    user_id = user.user.id

    
  
    # Check if the vehicle and driver exist
    vehicle_exists = Vehicle.objects.filter(id=vehicle_id).last()
    driver_exists = Driver.objects.filter(user=user_id).last()

    if not vehicle_exists:
        return Response({"detail": "Vehicle does not exist."}, status=status.HTTP_400_BAD_REQUEST)
    if not driver_exists:
        return Response({"detail": "Driver does not exist."}, status=status.HTTP_400_BAD_REQUEST)

    is_alredy_allocated=AllocateDriverToVehicle.objects.filter(driver=driver_exists,is_active=True).last() 

    if is_alredy_allocated:
        return Response({"detail": f"You are already allocated to a vehicle {vehicle_exists.vehicle_number}"}, status=status.HTTP_400_BAD_REQUEST)

    if vehicle_exists and driver_exists:
        # Get the actual vehicle and driver objects
        vehicle_data=Vehicle.objects.filter(id=vehicle_id).last() 
        allocation_data=AllocateDriverToVehicle.objects.filter(vehicle=vehicle_data,is_active=True).last() 
        if allocation_data:
            return Response({"detail": f"Vehicle is already allocated to : {allocation_data.driver.driver_name} - {allocation_data.driver.user.emp_id.emp_id}"}, status=status.HTTP_400_BAD_REQUEST)

        vehicle = Vehicle.objects.get(id=vehicle_id)
        driver = Driver.objects.get(user=user_id)

        # Allocate the driver to the vehicle
        allocation = AllocateDriverToVehicle(
            vehicle=vehicle,
            driver=driver,
            is_active=True
        )
        allocation.save()

        # Prepare the response data
        response_data = {
            "vehicle_id": vehicle.id,
            "vehicle_number": vehicle.vehicle_number,
            "driver_name": allocation.driver.driver_name,
            "is_active": allocation.is_active
        }

        return Response(response_data, status=status.HTTP_201_CREATED)

    else:
        return Response({"detail": "Something Missing"}, status=status.HTTP_400_BAD_REQUEST)
    


@api_view(['GET'])
def leave_driver_from_vehicle(request): 
    if request.method == 'GET':  
        token=request.query_params.get('token') 

        # Retrieve the user associated with the token
        user = get_object_or_404(Token, key=token) 

        driver=get_object_or_404(Driver, user=user.user)

        allocated_vehicle=AllocateDriverToVehicle.objects.filter(driver=driver,is_active=True).last()

        if not token: 
            return Response({"detail": "Token is required."}, status=status.HTTP_400_BAD_REQUEST)
     
        if not allocated_vehicle: 
            return Response({"detail": "No any vehicle allocated."}, status=status.HTTP_400_BAD_REQUEST)
            
        # Check if the user is a driver
        if not user.user.is_driver: 
            return Response({"detail": "Not Valid Token For Driver."}, status=status.HTTP_400_BAD_REQUEST)
 
        # Extract vehicle and driver from the request
 
        # # Check if the same driver is already active for the same vehicle
        # vehicle=get_object_or_404(Vehicle,id=vehicle_id)
        # active_record = AllocateDriverToVehicle.objects.filter(vehicle=vehicle, is_active=True).first()

        if allocated_vehicle:
            # Set the 'is_active' field to False for the active record
            allocated_vehicle.is_active = False
            allocated_vehicle.leaving_date_time=now()
            allocated_vehicle.save()

            return Response(
                {"message": "Driver has been removed from the vehicle."},
                status=status.HTTP_200_OK
            )

        return Response(
            {"error": "No active driver found for this vehicle."},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['GET'])
def get_breakdown_type(request):
    """
    This API returns all available breakdown types.
    """
    breakdown_types = BreakdownType.objects.all()  # Fetch all breakdown types from the database
    serializer = BreakdownTypeSerializer(breakdown_types, many=True)  # Serialize the data
    return Response(serializer.data, status=status.HTTP_200_OK)
 


@api_view(['POST'])
def create_breakdown(request):
    if request.method == 'POST': 
        # Directly access data from the request
        vehicle_id = request.data.get('vehicle_id')
        breakdown_type_id = request.data.get('type')

        # Retrieve the user associated with the token
        token=request.data.get('token')
        user = get_object_or_404(Token, key=token)
        driver=Driver.objects.filter(user=user).last()

        if not token: 
            return Response({"Required": "Token is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        if not user.user.is_driver: 
            return Response({"detail": "Only Driver can generate breakdown alert."}, status=status.HTTP_400_BAD_REQUEST)
                 
        # Initialize the serializer with incoming data
        serializer = BreakdownSerializer(data=request.data)
        
        if serializer.is_valid():
            try:
                vehicle = Vehicle.objects.get(id=vehicle_id)
                breakdown_type = BreakdownType.objects.get(id=breakdown_type_id)
            except Vehicle.DoesNotExist:
                return Response({"error": "Vehicle not found"}, status=status.HTTP_400_BAD_REQUEST)
            except BreakdownType.DoesNotExist:
                return Response({"error": "Breakdown type not found"}, status=status.HTTP_400_BAD_REQUEST)
            
            # Create and save the breakdown instance
            breakdown_instance = Breakdown(**serializer.validated_data)
            breakdown_instance.vehicle = vehicle
            breakdown_instance.type = breakdown_type
            breakdown_instance.driver=driver
            breakdown_instance.save()
            
            # Prepare the email body using HTML template
            email_body = render_to_string('breakdown_alert_email.html', {
                'vehicle': breakdown_instance.vehicle,
                'Breakdown_Type': breakdown_instance.type,
                'Description': breakdown_instance.description,
                'date_time': breakdown_instance.date_time,
                'audio': breakdown_instance.audio,
                'image1': breakdown_instance.image1,
                'image2': breakdown_instance.image2,
                'image3': breakdown_instance.image3,
                'image4': breakdown_instance.image4,
            })
            
            # Configure the email
            email_message = EmailMessage(
                subject="Notification - Breakdown Alert",
                body=email_body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=['prameshwar4378@gmail.com'],  # Replace with the appropriate recipient email
            )

            # Set the email content type to HTML
            email_message.content_subtype = 'html'

            # Attach images if they exist
            if breakdown_instance.image1:
                email_message.attach(
                    os.path.basename(breakdown_instance.image1.name),  # Get the file name
                    breakdown_instance.image1.read(),  # Read the image file content
                    breakdown_instance.image1.url  # The content type of the file
                )
            if breakdown_instance.image2:
                email_message.attach(
                    os.path.basename(breakdown_instance.image2.name),
                    breakdown_instance.image2.read(),
                    breakdown_instance.image2.url
                )
            if breakdown_instance.image3:
                email_message.attach(
                    os.path.basename(breakdown_instance.image3.name),
                    breakdown_instance.image3.read(),
                    breakdown_instance.image3.url
                )
            if breakdown_instance.image4:
                email_message.attach(
                    os.path.basename(breakdown_instance.image4.name),
                    breakdown_instance.image4.read(),
                    breakdown_instance.image4.url
                )
            if breakdown_instance.audio:
                email_message.attach(
                    os.path.basename(breakdown_instance.audio.name),
                    breakdown_instance.audio.read(),
                    breakdown_instance.audio.url
                )
             
            # Print to confirm
            print("Email body prepared, attaching files...")

            # Send the email in a background thread to avoid blocking the request
            email_thread = threading.Thread(target=send_email_in_background, args=(email_message,))
            email_thread.start()

            return Response({"message": "Breakdown alert sent!"}, status=status.HTTP_201_CREATED)
        


@api_view(['GET'])
def get_driver_allocation_history(request):
    # Fetch all active vehicle-driver allocations
    
    token = request.query_params.get('token')
    user = get_object_or_404(Token, key=token)

    if not token: 
        return Response({"detail": "Token is required."}, status=status.HTTP_400_BAD_REQUEST)
     
    # Check if the user is a driver
    if not user.user.is_driver: 
        return Response({"detail": "Not Valid Token For Driver."}, status=status.HTTP_400_BAD_REQUEST)
    
    allocations = AllocateDriverToVehicle.objects.filter(driver__user=user.user).order_by('-id')
    
    # Create a list to store the result
    allocation_history = []

    for allocation in allocations:
        # Calculate working hours
        if allocation.leaving_date_time:
            working_hours = (allocation.leaving_date_time - allocation.joining_date_time).total_seconds() / 3600
        else:
            # If the leaving date is not set, use the current time for the working hour calculation
            working_hours = (timezone.now() - allocation.joining_date_time).total_seconds() / 3600
        
        # Prepare the data for this allocation
        allocation_history.append({
            'vehicle_number': allocation.vehicle.vehicle_number,  # Assuming `vehicle_number` is a field in the `Vehicle` model
            'joining_time': allocation.joining_date_time,
            'leaving_time': allocation.leaving_date_time or "Still Active",  # Set leaving time as 'Still Active' if None
            'working_hours': round(working_hours, 2),  # Round the working hours to 2 decimal places
        })

    return Response(allocation_history, status=status.HTTP_200_OK)



@api_view([ 'POST'])
def create_fuel_record(request): 
    if request.method == 'POST':
        serializer = FuelRecordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_last_fuel_record(request):
    """
    This API returns the last fuel record for a vehicle using query parameters.
    Example: /api/get-last-fuel-record/?vehicle_id=10
    """
    vehicle_id = request.query_params.get('vehicle_id')

    if not vehicle_id:
        return Response({"detail": "Vehicle ID is required."}, status=status.HTTP_400_BAD_REQUEST)

    # Retrieve the vehicle object
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)

    # Fetch the last fuel record for the vehicle
    last_record = FuelRecord.objects.filter(vehicle=vehicle).last()

    if not last_record:
        return Response({"detail": "No fuel records found for this vehicle."}, status=status.HTTP_404_NOT_FOUND)

    data = {
         'last_km': last_record.current_km,
        'last_fuel_date': last_record.created_at,
        'last_driver_name': last_record.driver.driver_name,
        # 'emi_id':last_record.driver.user.emp_id.emp_id 
    }

    return Response(data, status=status.HTTP_200_OK)



@api_view(['GET'])
def get_fuel_history(request):
    # Fetch all active vehicle-driver allocations

    fuel = FuelRecord.objects.order_by('-id')[:100]
    
    # Create a list to store the result
    fuel_data_history = []

    for f in fuel: 
        # Prepare the data for this allocation
        fuel_data_history.append({
            'vehicle_number': f.vehicle.vehicle_number,  # Assuming `vehicle_number` is a field in the `Vehicle` model
            'fuel_fill_date': f.created_at,
            'fuel_liters': f.fuel_liters ,  # Set leaving time as 'Still Active' if None
            'driver': f.driver.driver_name,  # Round the working hours to 2 decimal places
        })

    return Response(fuel_data_history, status=status.HTTP_200_OK)
