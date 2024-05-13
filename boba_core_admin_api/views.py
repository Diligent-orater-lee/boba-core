from django.http import JsonResponse
from rest_framework.decorators import api_view
from device_manager.sensor_manager_service import SensorManager


# Create your views here.
def test(request):
    return JsonResponse(None)

# Add a camera device
@api_view(['POST'])
def AddSensor(request):   
    sensorManager = SensorManager()
    res = sensorManager.AddSensor(request.data)
    return JsonResponse(res)
        