from django.db import models

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

# Create your models here.
class Sensor(BaseModel):
    name = models.CharField(max_length=100)
    type = models.IntegerField()
    source = models.CharField(max_length=255)
    
    # detect_width = models.IntegerField()
    # detect_height = models.IntegerField()
    # detect_fps = models.IntegerField()
    # motion_mask = models.JSONField()