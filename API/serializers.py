from rest_framework import serializers, filters
from ERP_Admin.models import *
from rest_framework.authtoken.models import Token

class AllocateDriverToVehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = AllocateDriverToVehicle
        fields = ['vehicle']  # Include 'driver_token' as part of the input, but not as a model field

 
class BreakdownTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BreakdownType
        fields = ['id', 'type']  # Fields you want to expose in the response

 
class BreakdownSerializer(serializers.ModelSerializer):
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