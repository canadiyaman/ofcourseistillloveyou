"""
URL configuration for I Still Love You project.
"""

from django.urls import path

from event.views import VehicleTelemetryView

urlpatterns = [
    path(
        "api/v1/vehicle-telemetry",
        VehicleTelemetryView.as_view(),
        name="vehicle-telemetry",
    ),
]
