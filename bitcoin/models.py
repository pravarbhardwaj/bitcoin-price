from django.db import models

class Bitcoin(models.Model):
    timestamp = models.TimeField(primary_key=True, max_length=264, unique=True)
    price = models.FloatField()

    def __timestamp__(self) -> timestamp:
        return self.timestamp