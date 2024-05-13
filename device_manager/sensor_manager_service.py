from device_manager.camera_manager import CameraManager
from utilities.sensor_enums import SensorTypeEnum

class SensorManager:
    def __init__(self) -> None:
        pass

    def AddSensor(self, data):
        match data["type"]:
            case SensorTypeEnum.ONVIF_CAMERA:
                manager = CameraManager()
                res = manager.AddOnvifCamera(data).value()
                return res
        
        return None