

 
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
        name=f'{driver.driver_name}'
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
        'profile_image':profile_image_url
    }
    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_vehicle_details(request):
    vehicle_number=request.query_params.get('vehicle_number')

    vehicle=Vehicle.objects.filter(vehicle_number=vehicle_number).first()
    if not vehicle: 
        raise AuthenticationFailed(f'Vehicle with {vehicle.vehicle_number} number not eixst')

    response_data = {
        'vehicle_number': vehicle_number,
        'vehicle_name':vehicle.model_name.model_name,  
        'vehicle_id':vehicle.id,  
    }
    return Response(response_data, status=status.HTTP_200_OK)


 

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
    vehicle_exists = Vehicle.objects.filter(id=vehicle_id)
    driver_exists = Driver.objects.filter(user=user_id).exists()

    if not vehicle_exists:
        return Response({"detail": "Vehicle does not exist."}, status=status.HTTP_400_BAD_REQUEST)
    if not driver_exists:
        return Response({"detail": "Driver does not exist."}, status=status.HTTP_400_BAD_REQUEST)

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
            "joining_date_time": allocation.joining_date_time,
            "is_active": allocation.is_active
        }

        return Response(response_data, status=status.HTTP_201_CREATED)

    else:
        return Response({"detail": "Something Missing"}, status=status.HTTP_400_BAD_REQUEST)
    


@api_view(['POST'])
def leave_driver_from_vehicle(request): 
    if request.method == 'POST':  
        token=request.query_params.get('token')
        vehicle_id=request.query_params.get('vehicle_id')

        # Retrieve the user associated with the token
        user = get_object_or_404(Token, key=token)
    
        if not token: 
            return Response({"detail": "Token is required."}, status=status.HTTP_400_BAD_REQUEST)
     
        if not vehicle_id: 
            return Response({"detail": "Vehicle ID is required."}, status=status.HTTP_400_BAD_REQUEST)
            
        # Check if the user is a driver
        if not user.user.is_driver: 
            return Response({"detail": "Not Valid Token For Driver."}, status=status.HTTP_400_BAD_REQUEST)
 
        # Extract vehicle and driver from the request
 
        # Check if the same driver is already active for the same vehicle
        vehicle=get_object_or_404(Vehicle,id=vehicle_id)
        active_record = AllocateDriverToVehicle.objects.filter(vehicle=vehicle, is_active=True).first()

        if active_record:
            # Set the 'is_active' field to False for the active record
            active_record.is_active = False
            active_record.leaving_date_time=now()
            active_record.save()

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
        vehicle_id = request.data.get('vehicle')  # Get 'vehicle' field from the request
        breakdown_type_id = request.data.get('type')  # Get 'type' field from the request
    
        # Initialize the serializer with incoming data
        serializer = BreakdownSerializer(data=request.data)
        
        if serializer.is_valid():
            # Fetch related instances from the database
            try:
                vehicle = Vehicle.objects.get(id=vehicle_id)  # Fetch the vehicle by ID
                breakdown_type = BreakdownType.objects.get(id=breakdown_type_id)  # Fetch breakdown type by ID
            except Vehicle.DoesNotExist:
                return Response({"error": "Vehicle not found"}, status=status.HTTP_400_BAD_REQUEST)
            except BreakdownType.DoesNotExist:
                return Response({"error": "Breakdown type not found"}, status=status.HTTP_400_BAD_REQUEST)
            
            # Create Breakdown instance from validated data (without saving yet)
            breakdown_instance = Breakdown(**serializer.validated_data)
            
            # Assign the fetched instances to the foreign key fields
            breakdown_instance.vehicle = vehicle
            breakdown_instance.type = breakdown_type
            
            # Save the instance to the database
            breakdown_instance.save()
            
            # Re-serialize the saved object to return the updated data
            response_serializer = BreakdownSerializer(breakdown_instance)
            
            # Return the serialized data in the response
            return Response("Request Submited Success", status=status.HTTP_201_CREATED)
        
        # If the serializer is not valid, return validation errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



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
    
    allocations = AllocateDriverToVehicle.objects.filter(is_active=True,driver__user=user.user)
    
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
