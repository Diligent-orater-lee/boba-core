from django.conf import settings
import os
from device_manager.serializers import CameraSerializer
import yaml
import requests
from utilities.http_responses import CustomUpdateResult

class FrigateManager:

    FRIGATE_CONFIG_FOLDER = None
    FRIGATE_YML_FILE = None
    FRIGATE_HOST = None
    FRIGATE_PORT = None
    
    def __init__(self) -> None:
        env = settings.ENV
        self.FRIGATE_CONFIG_FOLDER = env.str("FRIGATE_CONFIG_FOLDER", default="config")
        self.FRIGATE_YML_FILE = env.str("FRIGATE_YML_FILE", default="config.yml")
        self.FRIGATE_HOST = env.str("FRIGATE_HOST", default="localhost")
        self.FRIGATE_PORT = env.str("FRIGATE_PORT", default="5000")

    def __frigateConfigPath(self):
        return f"{self.FRIGATE_CONFIG_FOLDER}/{self.FRIGATE_YML_FILE}"
    
    def __camEntryFromName(self, name: str):
        return name.lower().replace(" ", "_") # space is not allowed

    def FrigateFilesValid(self):
        if (os.path.isfile(self.__frigateConfigPath())):
            return {"valid": True, "error": ""}
        else:
            return {"valid": False, "error": f"Frigate configurations are not found. File does not exists in path: {self.__frigateConfigPath()}"}
        
    def AddFFMPEGCamera(self, item: CameraSerializer):
        file_path = self.__frigateConfigPath()
        parent_key = "cameras"
        with open(file_path, 'r') as file:
            data = yaml.safe_load(file)

        if parent_key not in data:
            data[parent_key] = {}
        
        newEntryName = self.__camEntryFromName(item.initial_data["name"])
        if (newEntryName in data[parent_key]):
            return CustomUpdateResult(False, "Camera already exists. Cannot add again")

        newEntry = {
            newEntryName: {
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

        if (data[parent_key] == None):
            data[parent_key] = newEntry
        else:
            data[parent_key] = {
                **data[parent_key],
                **newEntry
            }

        with open(file_path, 'w') as file:
            yaml.safe_dump(data, file, default_flow_style=False)

        return self.RestartFrigate()

    def RestartFrigate(self):
        try:
            restartUrl = f"http://{self.FRIGATE_HOST}:{self.FRIGATE_PORT}/api/restart"
            headers = {
            }

            response = requests.post(restartUrl, headers=headers)

            if response.status_code == 200:
                return CustomUpdateResult(True, "")
            else:
                return CustomUpdateResult(False, "Unable to restart frigate. Frigate API threw an error")
        except Exception as e:
            return CustomUpdateResult(False, "Connection to frigate failed")