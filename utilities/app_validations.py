from django.conf import settings
import os
from device_manager.serializers import CameraSerializer
import yaml

class FrigateValidations:

    FRIGATE_ROOT = None
    FRIGATE_CONFIG_FOLDER = None
    FRIGATE_YML_FILE = None
    
    def __init__(self) -> None:
        env = settings.ENV
        self.FRIGATE_ROOT = env.str("FRIGATE_PATH", default="/frigate")
        self.FRIGATE_CONFIG_FOLDER = env.str("FRIGATE_CONFIG_FOLDER", default="config")
        self.FRIGATE_YML_FILE = env.str("FRIGATE_YML_FILE", default="config.yml")

    def FrigateFilesValid(self):
        if (os.path.isfile(f"{self.FRIGATE_ROOT}/{self.FRIGATE_CONFIG_FOLDER}/{self.FRIGATE_YML_FILE}")):
            return {"valid": True, "error": ""}
        else:
            return {"valid": False, "error": f"Frigate configurations are not found. File does not exists in path: {self.FRIGATE_ROOT}/{self.FRIGATE_CONFIG_FOLDER}/{self.FRIGATE_YML_FILE}"}
        
    def AddFFMPEGCamera(self, item: CameraSerializer):
        file_path = f"{self.FRIGATE_ROOT}/{self.FRIGATE_CONFIG_FOLDER}/{self.FRIGATE_YML_FILE}"
        parent_key = "cameras"
        newEntry = {
            item.initial_data["name"]: {
                "detect": {
                    "width": item.initial_data["height"],
                    "height": item.initial_data["width"],
                    "fps": item.initial_data["fps"],
                },
                "ffmpeg": {
                    "inputs": [
                        {
                            "path": item.initial_data["source"],
                            "roles": ["detect"]
                        }
                    ]
                },
                "mqtt": {
                    "timestamp": False,
                    "bounding_box": False,
                    "crop": True,
                    "quality": 100,
                    "height": 500,
                },
                # "motion": {
                #     "mask": [
                #         "0, 461, 3, 0, 1919, 0, 1919, 843, 1699, 492, 1344, 458, 1346, 336, 973, 317, 869, 375, 866, 432"
                #     ]
                # }
            }
        }

        with open(file_path, 'r') as file:
            data = yaml.safe_load(file)

        if parent_key not in data:
            data[parent_key] = {}

        if (data[parent_key] == None):
            data[parent_key] = newEntry
        else:
            data[parent_key] = {
                **data[parent_key],
                **newEntry
            }

        with open(file_path, 'w') as file:
            yaml.safe_dump(data, file, default_flow_style=False)