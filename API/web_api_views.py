from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ERP_Admin.models import AllocateDriverToVehicle,Vehicle,Driver,Breakdown
from .serializers import *
from django.utils.timezone import now




@api_view(['GET']) 
def get_vehicle_numbers(request):
    try:
        vehicles = Vehicle.objects.only('vehicle_number')  # Query all vehicle numbers
        vehicle_numbers = [vehicle.vehicle_number for vehicle in vehicles]  # Extract vehicle numbers into a list
        
        if not vehicle_numbers:
            return Response({'error': 'No vehicle numbers found'}, status=status.HTTP_404_NOT_FOUND)
        
        response_data = {
            'vehicle_numbers': vehicle_numbers  # Returning the list of vehicle numbers
        }
        return Response(response_data, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({'error': 'An unexpected error occurred', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET']) 
def get_drivers(request):
    try:
        # Query all drivers (you can filter fields if necessary, but we'll use all fields here)
        drivers = Driver.objects.all()  # Retrieve all drivers
        
        # If no drivers are found, return an error
        if not drivers.exists():
            return Response({'error': 'No Drivers found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Prepare the response data with id and driver_name for each driver
        response_data = [
            {
                'id': driver.id,
                'driver_name': driver.driver_name
            }
            for driver in drivers
        ]
        
        return Response(response_data, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({'error': 'An unexpected error occurred', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET']) 
def get_vehicles(request):
    try:
        # Query all vehicles (you can filter fields if necessary)
        vehicles = Vehicle.objects.all()  # Retrieve all vehicles
        
        # If no vehicles are found, return an error
        if not vehicles.exists():
            return Response({'error': 'No Vehicles found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Prepare the response data with id and vehicle_name for each vehicle
        response_data = [
            {
                'id': vehicle.id,
                'vehicle_number': vehicle.vehicle_number  # Assuming vehicle_name is the field you want
            }
            for vehicle in vehicles
        ]
        
        return Response(response_data, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({'error': 'An unexpected error occurred', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# ✅ CREATE & LIST Allocations
@api_view(['GET', 'POST'])
def allocate_driver_list_create(request):
    try:
        if request.method == 'GET':
            allocations = AllocateDriverToVehicle.objects.all()
            serializer = AllocateDriverToVehicleSerializerWeb(allocations, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        elif request.method == 'POST':
            vehicle = request.data.get('vehicle') 
            driver = request.data.get('driver') 
            if not vehicle: 
                return Response({"detail": "Vehicle is required."}, status=status.HTTP_400_BAD_REQUEST)

            if not driver: 
                return Response({"detail": "Driver is required."}, status=status.HTTP_400_BAD_REQUEST)
        
            # Check if the vehicle and driver exist
            vehicle_exists = Vehicle.objects.select_related('model_name').filter(id=vehicle).first()

            driver_exists = Driver.objects.filter(id=driver).first()

            if not vehicle_exists:
                return Response({"detail": "Vehicle does not exist."}, status=status.HTTP_400_BAD_REQUEST)
            if not driver_exists:
                return Response({"detail": "Driver does not exist."}, status=status.HTTP_400_BAD_REQUEST)

            is_alredy_allocated=AllocateDriverToVehicle.objects.filter(driver=driver_exists,is_active=True).first() 

            if is_alredy_allocated:
                return Response({"detail": f"You are already allocated to a vehicle {vehicle_exists.vehicle_number}"}, status=status.HTTP_400_BAD_REQUEST)

            if vehicle_exists and driver_exists:
                # Get the actual vehicle and driver objects
                vehicle_data=Vehicle.objects.select_related('model_name').filter(id=vehicle).order_by('-id').first() 
                allocation_data=AllocateDriverToVehicle.objects.filter(vehicle=vehicle_data,is_active=True).order_by('-id').first() 
                
                if allocation_data:
                    return Response({"detail": f"Vehicle is already allocated to : {allocation_data.driver.driver_name} - {allocation_data.driver.user.emp_id.emp_id}"}, status=status.HTTP_400_BAD_REQUEST)

            serializer = AllocateDriverToVehicleSerializerWeb(data=request.data)
            if serializer.is_valid():
                fm=serializer.save(is_active=True,joining_date_time=now())
                fm.save()
                return Response(
                    {"message": "Driver allocated successfully", "data": serializer.data}, 
                    status=status.HTTP_201_CREATED
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



# ✅ RETRIEVE, UPDATE & DELETE a Single Allocation
@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def allocate_driver_detail(request, pk):
    try:
        allocation = AllocateDriverToVehicle.objects.get(pk=pk)
        

        if request.method == 'GET':
            serializer = AllocateDriverToVehicleSerializerWeb(allocation)
            return Response(serializer.data, status=status.HTTP_200_OK)

        elif request.method in ['PUT', 'PATCH']:
            serializer = AllocateDriverToVehicleSerializerWeb(allocation, data=request.data, partial=(request.method == 'PATCH'))
            if allocation:
                is_active=allocation.is_active
            else:
                is_active=False
            if serializer.is_valid():
                fm=serializer.save(is_active=is_active)
                fm.save()
                return Response(
                    {"message": "Driver allocation updated successfully", "data": serializer.data}, 
                    status=status.HTTP_200_OK
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            allocation.delete()
            return Response({"message": "Driver allocation deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    
    except AllocateDriverToVehicle.DoesNotExist:
        return Response({"error": "Allocation not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


 
 
# ✅ CREATE & LIST Breakdowns
@api_view(['GET', 'POST'])
def breakdown_list_create(request):
    try:
        if request.method == 'GET':
            breakdowns = Breakdown.objects.all().order_by('-date_time')  # Fetch latest first
            serializer = BreakdownSerializerWeb(breakdowns, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        elif request.method == 'POST':
            vehicle = request.data.get('vehicle') 
            driver = request.data.get('driver') 
            if not vehicle: 
                return Response({"detail": "Vehicle is required."}, status=status.HTTP_400_BAD_REQUEST)
            else:
                vehicle=Vehicle.objects.get(id=vehicle)
            if not driver: 
                return Response({"detail": "Driver is required."}, status=status.HTTP_400_BAD_REQUEST)
            else:
                driver=Driver.objects.get(id=driver)

        
            serializer = BreakdownSerializerWeb(data=request.data)

            if serializer.is_valid():
                fm=serializer.save(vehicle=vehicle,driver=driver)
                return Response(
                    {"message": "Breakdown reported successfully", "data": serializer.data}, 
                    status=status.HTTP_201_CREATED
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ✅ RETRIEVE, UPDATE & DELETE a Single Breakdown
@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def breakdown_detail(request, pk):
    try:
        breakdown = Breakdown.objects.get(pk=pk)
        
        if request.method == 'GET':
            serializer = BreakdownSerializerWeb(breakdown)
            return Response(serializer.data, status=status.HTTP_200_OK)

        elif request.method in ['PUT', 'PATCH']:
            serializer = BreakdownSerializerWeb(breakdown, data=request.data, partial=(request.method == 'PATCH'))
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"message": "Breakdown details updated successfully", "data": serializer.data}, 
                    status=status.HTTP_200_OK
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            breakdown.delete()
            return Response({"message": "Breakdown record deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    
    except Breakdown.DoesNotExist:
        return Response({"error": "Breakdown not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ✅ CREATE & LIST Fuel Records
@api_view(['GET', 'POST'])
def fuel_record_list_create(request):
    try:
        if request.method == 'GET':
            # Get query parameters for filtering
            vehicle_id = request.query_params.get('vehicle', None)
            driver_id = request.query_params.get('driver', None)
            start_date = request.query_params.get('start_date', None)
            end_date = request.query_params.get('end_date', None)

            # Start with all fuel records
            fuel_records = FuelRecord.objects.all()

            # Apply filtering based on available query parameters
            if vehicle_id:
                fuel_records = fuel_records.filter(vehicle__id=vehicle_id)

            if driver_id:
                fuel_records = fuel_records.filter(driver__id=driver_id)

            if start_date:
                fuel_records = fuel_records.filter(created_at__gte=start_date)

            if end_date:
                fuel_records = fuel_records.filter(created_at__lte=end_date)

            # Order by creation date descending
            fuel_records = fuel_records.order_by('-created_at')

            # Serialize the filtered data
            serializer = FuelRecordSerializerWeb(fuel_records, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        elif request.method == 'POST':
            vehicle = request.data.get('vehicle')
            driver = request.data.get('driver')
            if not vehicle:
                return Response({"detail": "Vehicle is required."}, status=status.HTTP_400_BAD_REQUEST)
            else:
                vehicle = Vehicle.objects.get(id=vehicle)
            if driver:
                driver = Driver.objects.get(id=driver)
            else:
                driver = None

            serializer = FuelRecordSerializerWeb(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"message": "Fuel record added successfully", "data": serializer.data},
                    status=status.HTTP_201_CREATED
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ✅ RETRIEVE, UPDATE & DELETE a Single Fuel Record
@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def fuel_record_detail(request, pk):
    try:
        fuel_record = FuelRecord.objects.get(pk=pk)
        
        if request.method == 'GET':
            serializer = FuelRecordSerializerWeb(fuel_record)
            return Response(serializer.data, status=status.HTTP_200_OK)

        elif request.method in ['PUT', 'PATCH']:
            serializer = FuelRecordSerializerWeb(fuel_record, data=request.data, partial=(request.method == 'PATCH'))
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"message": "Fuel record updated successfully", "data": serializer.data}, 
                    status=status.HTTP_200_OK
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            fuel_record.delete()
            return Response({"message": "Fuel record deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

    except FuelRecord.DoesNotExist:
        return Response({"error": "Fuel record not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


 
# ✅ CREATE & LIST Breakdown Types
@api_view(['GET', 'POST'])
def breakdown_type_list_create(request):
    try:
        if request.method == 'GET':
            breakdown_types = BreakdownType.objects.all().order_by('type')  # Fetch all breakdown types
            serializer = BreakdownTypeSerializerWeb(breakdown_types, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        elif request.method == 'POST':
            serializer = BreakdownTypeSerializerWeb(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"message": "Breakdown type added successfully", "data": serializer.data}, 
                    status=status.HTTP_201_CREATED
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ✅ RETRIEVE, UPDATE & DELETE a Single Breakdown Type
@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def breakdown_type_detail(request, pk):
    try:
        breakdown_type = BreakdownType.objects.get(pk=pk)
        
        if request.method == 'GET':
            serializer = BreakdownTypeSerializerWeb(breakdown_type)
            return Response(serializer.data, status=status.HTTP_200_OK)

        elif request.method in ['PUT', 'PATCH']:
            serializer = BreakdownTypeSerializerWeb(breakdown_type, data=request.data, partial=(request.method == 'PATCH'))
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"message": "Breakdown type updated successfully", "data": serializer.data}, 
                    status=status.HTTP_200_OK
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            breakdown_type.delete()
            return Response({"message": "Breakdown type deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

    except BreakdownType.DoesNotExist:
        return Response({"error": "Breakdown type not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
