from camera_manager import RegularCameraManager

class SensorManager:
    def __init__(self) -> None:
        pass

    def AddSensor(data):
        match data["type"]:
            case "REGULAR_CAMERA":
                manager = RegularCameraManager()
                