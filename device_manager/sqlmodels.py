from django.db import models

# Create your models here.
class Sensor(models.Model):
    name = models.CharField(max_length=100)
    type = models.IntegerField()
    source = models.CharField(max_length=255)
    
    # detect_width = models.IntegerField()
    # detect_height = models.IntegerField()
    # detect_fps = models.IntegerField()
    # motion_mask = models.JSONField()

class OnvifCamera(Sensor):
    pass