from djongo import models

class SensorFullData(models.Model):
    name = models.CharField(max_length=100)
    type = models.IntegerField()
    source = models.CharField(max_length=255)
    others = models.CharField(max_length=255)

    class Meta:
        managed = False

    def save(self, *args, **kwargs):
        kwargs.pop("using")
        super().save(using="mongo", *args, **kwargs)