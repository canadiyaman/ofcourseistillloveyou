from django.conf import settings
from elasticsearch_dsl import Document, Text, Float, Date
from elasticsearch_dsl.connections import connections

connections.create_connection(hosts=[settings.ELASTICSEARCH_HOST])


class VehicleTelemetryDocument(Document):
    plate_number = Text()
    latitude = Float()
    longitude = Float()
    timestamp = Date()

    class Index:
        name = "vehicle_telemetry"
        settings = {
            "number_of_shards": 1,
        }

    def save(self, **kwargs):
        return super().save(**kwargs)
