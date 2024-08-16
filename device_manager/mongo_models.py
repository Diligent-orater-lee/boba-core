from djongo import models

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class SensorFullData(BaseModel):
    name = models.CharField(max_length=100)
    type = models.IntegerField()
    source = models.CharField(max_length=255)
    height = models.IntegerField()
    width = models.IntegerField()
    fps = models.IntegerField()

    class Meta:
        managed = False

    def save(self, *args, **kwargs):
        kwargs.pop("using")
        super().save(using="mongo", *args, **kwargs)

class Slave(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    ip = models.CharField(max_length=45)  # Using CharField instead of GenericIPAddressField
    name = models.CharField(max_length=100)
    description = models.TextField()
    component_type = models.CharField(max_length=100)

    objects = models.DjongoManager()

    def __str__(self):
        return f"{self.name} ({self.id})"

    class Meta:
        abstract = False