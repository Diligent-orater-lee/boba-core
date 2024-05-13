from rest_framework import serializers
from device_manager.sqlmodels import OnvifCamera
from device_manager.mongo_models import Sensor as MongoSensor

class CameraSerializer(serializers.Serializer):

    mongoModel: MongoSensor = None

    class Meta:
        model = OnvifCamera
        fields = ['name', 'type', 'source', "others"]

    def create(self, validated_data):
        self.mongoModel = MongoSensor.objects.create(**validated_data)
        return super().create(validated_data)
    
    def saveAllFields(self):
        self.mongoModel.save(using="mongo")