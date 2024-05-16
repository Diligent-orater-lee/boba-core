from utilities.app_validations import FrigateValidations
from utilities.http_responses import CustomUpdateResult
from device_manager.serializers import CameraSerializer

class CameraManager:
    def AddOnvifCamera(self, data):
        # FRIGATE CONFIGURATIONS ARE REQUIRED WHEN ADDING CAMERA
        frigateManager = FrigateValidations()
        frigateValidation = frigateManager.FrigateFilesValid()
        if (not frigateValidation["valid"]):
            return CustomUpdateResult(False, frigateValidation["error"])
        else:
            cameraData = CameraSerializer(data=data)
            if (cameraData.is_valid()):
                addInFrigate = frigateManager.AddFFMPEGCamera(cameraData)
                if (addInFrigate.success):
                    cameraData.save()
                    return CustomUpdateResult(True, "Data created")
                else:
                    return addInFrigate
            else:
                return CustomUpdateResult(False, "Invalid data")