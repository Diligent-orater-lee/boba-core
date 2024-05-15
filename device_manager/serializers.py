from rest_framework import serializers
from device_manager.sqlmodels import Sensor
from device_manager.mongo_models import SensorFullData

class CameraSerializer(serializers.Serializer):

    mongoModel: SensorFullData = None
    sqlEntities = [
        "name",
        "type",
        "source"
    ]

    class Meta:
        model = Sensor
        fields = ['name', 'type', 'source', "height", "width", "fps"]

    def create(self, validated_data):
        self.mongoModel = SensorFullData.objects.create(**self.initial_data)
        sqlData = {}
        for field in self.sqlEntities:
            sqlData[field] = self.initial_data[field]

        item = Sensor.objects.create(**sqlData)
        return item