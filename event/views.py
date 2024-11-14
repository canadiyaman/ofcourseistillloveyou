from datetime import datetime
from elasticsearch_dsl import Search

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .documents import VehicleTelemetryDocument
from .serializers import VehicleTelemetrySerializer
from .tasks import save_telemetry_data


class VehicleTelemetryView(APIView):
    def post(self, request):
        serializer = VehicleTelemetrySerializer(data=request.data)
        if serializer.is_valid():
            save_telemetry_data.delay(serializer.data)
            return Response(
                {"message": "Telemetry data is being processed"},
                status=status.HTTP_202_ACCEPTED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")

        try:
            start_date = datetime.strptime(start_date, "%Y-%m-%d")
            end_date = datetime.strptime(end_date, "%Y-%m-%d")
        except (TypeError, ValueError):
            return Response(
                {
                    "error": "Please provide start_date and end_date in 'YYYY-MM-DD' format."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        search = Search(index="vehicle_telemetry").using(
            VehicleTelemetryDocument._get_connection()
        )
        search = search.filter("range", timestamp={"gte": start_date, "lte": end_date})

        response = search.execute()
        results = [
            {
                "plate_number": hit.plate_number,
                "latitude": hit.latitude,
                "longitude": hit.longitude,
                "timestamp": hit.timestamp,
            }
            for hit in response
        ]

        return Response(results, status=status.HTTP_200_OK)
