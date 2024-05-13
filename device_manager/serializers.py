from rest_framework import serializers
from device_manager.sqlmodels import Sensor
from device_manager.mongo_models import SensorFullData

class CameraSerializer(serializers.Serializer):

    mongoModel: SensorFullData = None

    class Meta:
        model = Sensor
        fields = ['name', 'type', 'source', "others"]

    def create(self, validated_data):
        self.mongoModel = SensorFullData.objects.create(**self.initial_data)
        copy: dict[str] = self.initial_data.copy()
        copy.pop("others")
        item = Sensor.objects.create(**copy)
        return item
    
    def saveAllFields(self):
        # self.mongoModel.save(using="mongo")
        pass