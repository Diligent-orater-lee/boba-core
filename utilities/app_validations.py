from django.conf import settings
import os

class FrigateValidations:
    @staticmethod
    def FrigateFilesValid():
        env = settings.ENV
        frigateRoot = env.str("FRIGATE_PATH", default="/frigate")
        frigateConfigFolder = env.str("FRIGATE_CONFIG_FOLDER", default="config")
        frigateYmlFile = env.str("FRIGATE_YML_FILE", default="config.yml")

        if (os.path.isdir(f"{frigateRoot}/{frigateConfigFolder}") and os.path.isfile(f"{frigateRoot}/{frigateConfigFolder}/{frigateYmlFile}")):
            return {"valid": True, "error": ""}
        else:
            return {"valid": False, "error": f"Frigate configurations are not found. File does not exists in path: {frigateRoot}/{frigateConfigFolder}/{frigateYmlFile}"}
