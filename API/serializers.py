from rest_framework import serializers, filters
from ERP_Admin.models import *
from rest_framework.authtoken.models import Token

# class AllocateDriverToVehicleSerializerAndroid(serializers.ModelSerializer):
#     class Meta:
#         model = AllocateDriverToVehicle
#         fields = ['vehicle']  # Include 'driver_token' as part of the input, but not as a model field

 
class BreakdownTypeSerializerAndroid(serializers.ModelSerializer):
    class Meta:
        model = BreakdownType
        fields = ['id', 'type']  # Fields you want to expose in the response
 
class BreakdownSerializerAndroid(serializers.ModelSerializer):
    class Meta:
        model = Breakdown
        fields = ['description', 'audio', 'image1', 'image2', 'image3', 'image4']

   
class FuelRecordSerializerAndroid(serializers.ModelSerializer):
    class Meta:
        model = FuelRecord
        fields = ['fuel_amount', 'fuel_liters', 'current_km', 'dashboard_photo', 'dispenser_photo','receipt_photo' ]

 
class AllocateDriverToVehicleSerializerWeb(serializers.ModelSerializer):
    class Meta:
        model = AllocateDriverToVehicle
        fields = '__all__'

class BreakdownSerializerWeb(serializers.ModelSerializer):
    driver_name = serializers.CharField(source='driver.driver_name', read_only=True)
    vehicle_number = serializers.CharField(source='vehicle.vehicle_number', read_only=True)

    class Meta:
        model = Breakdown
        fields = '__all__'


class FuelRecordSerializerWeb(serializers.ModelSerializer):
    driver_name = serializers.CharField(source='driver.driver_name', read_only=True)
    vehicle_number = serializers.CharField(source='vehicle.vehicle_number', read_only=True)

    class Meta:
        model = FuelRecord
        fields = '__all__'

class BreakdownTypeSerializerWeb(serializers.ModelSerializer):

    class Meta:
        model = BreakdownType
        fields = '__all__'