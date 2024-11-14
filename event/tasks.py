from celery import shared_task

from .documents import VehicleTelemetryDocument


@shared_task
def save_telemetry_data(data):
    telemetry = VehicleTelemetryDocument(
        plate_number=data["plate_number"],
        latitude=data["latitude"],
        longitude=data["longitude"],
        timestamp=data["timestamp"],
    )
    telemetry.save()
