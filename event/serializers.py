from rest_framework import serializers


class VehicleTelemetrySerializer(serializers.Serializer):
    plate_number = serializers.CharField()
    longitude = serializers.FloatField()
    latitude = serializers.FloatField()
    timestamp = serializers.CharField()
