from rest_framework import serializers
from ERP_Admin.models import AllocateDriverToVehicle


class AllocateDriverToVehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = AllocateDriverToVehicle
        fields = ['vehicle', 'driver']

    def validate(self, data):
        """
        Custom validation to ensure that both vehicle and driver are provided.
        """
        vehicle = data.get('vehicle')
        driver = data.get('driver')

        if not vehicle:
            raise serializers.ValidationError("Vehicle is required.")
        if not driver:
            raise serializers.ValidationError("Driver is required.")
        return data


