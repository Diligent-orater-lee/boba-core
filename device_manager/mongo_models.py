from djongo import models

class Sensor(models.Model):
    name = models.CharField(max_length=100)
    type = models.IntegerField()
    source = models.CharField(max_length=255)