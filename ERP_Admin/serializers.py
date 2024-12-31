from rest_framework import serializers
from .models import AllocateDriverToVehicle

class AllocateDriverToVehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = AllocateDriverToVehicle
        fields = ['vahicle', 'driver', 'joining_date_time', 'leaving_date_time', 'is_active']
