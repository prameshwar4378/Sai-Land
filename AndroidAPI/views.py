

from rest_framework.permissions import AllowAny
from rest_framework.authtoken.views import ObtainAuthToken

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from ERP_Admin.models import *
from .serializers import AllocateDriverToVehicleSerializer
from django.utils.timezone import now
 

class CustomAuthToken(ObtainAuthToken):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        return response
 

@api_view(['POST'])
def allocate_driver_to_vehicle(request): 
    print("Current Date Time is : ",now)
    if request.method == 'POST': 
        vehicle_id = request.data.get('vehicle')
        driver_id = request.data.get('driver')

        if not vehicle_id or not driver_id:
            return Response(
                {"error": "Both vehicle and driver are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if the same driver is already active for the same vehicle
        active_record_exists = AllocateDriverToVehicle.objects.filter( vehicle=vehicle_id,  driver=driver_id,   is_active=True  ).exists()

        if active_record_exists:
            return Response( {"error": "You are already allocated this vehicle."},  status=status.HTTP_400_BAD_REQUEST )

        # Optimize queries by combining filters and using bulk updates
        # Deactivate the current active driver, if any
        AllocateDriverToVehicle.objects.filter(driver=driver_id, is_active=True).update(is_active=False, leaving_date_time=now())

        # Deactivate the current active vehicle, if any
        AllocateDriverToVehicle.objects.filter(vehicle=vehicle_id, is_active=True ).update(is_active=False, leaving_date_time=now())
        # Create a new record
        serializer = AllocateDriverToVehicleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # AllocateDriverToVehicle.objects.all().delete()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def leave_driver_from_vehicle(request): 
    if request.method == 'POST': 
        # Extract vehicle and driver from the request
        vehicle_id = request.data.get('vehicle')

        # Check if required fields are provided
        if not vehicle_id:
            return Response(
                {"error": "Vehicle is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if the same driver is already active for the same vehicle
        active_record = AllocateDriverToVehicle.objects.filter(vehicle=vehicle_id, is_active=True).first()

        if active_record:
            # Set the 'is_active' field to False for the active record
            active_record.is_active = False
            active_record.save()

            return Response(
                {"message": "Driver has been removed from the vehicle."},
                status=status.HTTP_200_OK
            )

        return Response(
            {"error": "No active driver found for this vehicle."},
            status=status.HTTP_404_NOT_FOUND
        )
