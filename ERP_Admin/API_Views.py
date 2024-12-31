from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import AllocateDriverToVehicle
from .serializers import AllocateDriverToVehicleSerializer

@api_view(['POST'])
def allocate_driver_to_vehicle(request):
    if request.method == 'POST': 
        serializer = AllocateDriverToVehicleSerializer(data=request.data)
        
        # Print serializer for debugging
        print("Serializer object:", serializer)

        # Check if serializer is valid
        if serializer.is_valid():
            # Save the instance if the serializer is valid
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            # If serializer is not valid, print detailed error information
            print("Serializer Errors:", serializer.errors)
            
            # Loop through the errors and print them field by field
            for field, error in serializer.errors.items():
                print(f"Error in field '{field}': {error}")
            
            # Return the error response
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
