from rest_framework.test import APITestCase
from rest_framework import status
from elasticsearch_dsl import Document, Date, Keyword, Float, connections

connections.create_connection(hosts=["http://localhost:9200"])


class VehicleTelemetryDocument(Document):
    plate_number = Keyword()
    latitude = Float()
    longitude = Float()
    timestamp = Date()

    class Index:
        name = "vehicle_telemetry"


class VehicleTelemetryDateRangeTestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):
        doc1 = VehicleTelemetryDocument(
            plate_number="ABC-1234",
            latitude=40.7128,
            longitude=-74.0060,
            timestamp="2024-01-01T12:00:00Z",
        )
        doc2 = VehicleTelemetryDocument(
            plate_number="XYZ-9876",
            latitude=34.0522,
            longitude=-118.2437,
            timestamp="2024-02-01T12:00:00Z",
        )
        doc3 = VehicleTelemetryDocument(
            plate_number="LMN-4567",
            latitude=41.8781,
            longitude=-87.6298,
            timestamp="2024-03-01T12:00:00Z",
        )

        doc1.save()
        doc2.save()
        doc3.save()

    def test_valid_date_range(self):
        response = self.client.get(
            "/api/v1/vehicle-telemetry?start_date=2024-01-01&end_date=2024-02-01"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_no_results_for_date_range(self):
        response = self.client.get(
            "/api/v1/vehicle-telemetry?start_date=2025-01-01&end_date=2025-02-01"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_invalid_date_format(self):
        response = self.client.get(
            "/api/v1/vehicle-telemetry?start_date=01-01-2024&end_date=01-02-2024"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class VehicleTelemetryCreateTestCase(APITestCase):

    def test_create_vehicle_telemetry_success(self):
        data = {
            "latitude": 32.32,
            "longitude": 32.32,
            "plate_number": "00 ABC 99",
            "timestamp": "2024-12-12T13:27:32Z",  # ISO 8601 formatında bir tarih
        }

        response = self.client.post("/api/v1/vehicle-telemetry", data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(response.data["latitude"], data["latitude"])
        self.assertEqual(response.data["longitude"], data["longitude"])
        self.assertEqual(response.data["plate_number"], data["plate_number"])
        self.assertEqual(response.data["timestamp"], data["timestamp"])

    def test_create_vehicle_telemetry_missing_field(self):
        data = {
            "longitude": 32.32,
            "plate_number": "00 ABC 99",
            "timestamp": "2024-12-12T13:27:32Z",
        }

        response = self.client.post("/api/v1/vehicle-telemetry", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("latitude", response.data)

    def test_create_vehicle_telemetry_invalid_timestamp_format(self):
        data = {
            "latitude": 32.32,
            "longitude": 32.32,
            "plate_number": "00 ABC 99",
            "timestamp": "12.12.2024 13:27:32",
        }

        response = self.client.post("/api/v1/vehicle-telemetry", data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertIn("timestamp", response.data)
