class CustomUpdateResult:
    success = False
    message = ""
    userData = None

    def __init__(self, success = False, message = "", userData = None) -> None:
        self.success = success
        self.message = message
        self.userData = userData

    def value(self):
        return {
            "success": self.success,
            "message": self.message,
            "userData": self.userData
        }

