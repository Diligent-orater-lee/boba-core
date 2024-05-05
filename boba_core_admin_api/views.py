from django.http import JsonResponse
from utilities.app_validations import FrigateValidations
from django.views.decorators.http import require_POST
from device_manager.sensor_manager_service import SensorManager


# Create your views here.
def test(request):
    return JsonResponse(None)

# Add a camera device
@require_POST
def AddDevice(request):
    frigateValidation = FrigateValidations.FrigateFilesValid()
    if (not frigateValidation["valid"]):
        return JsonResponse({"status": False, "error": frigateValidation["error"]})
    
    sensorManager = SensorManager(request)
    return JsonResponse({"error": "COnfigurations are valid"})
        