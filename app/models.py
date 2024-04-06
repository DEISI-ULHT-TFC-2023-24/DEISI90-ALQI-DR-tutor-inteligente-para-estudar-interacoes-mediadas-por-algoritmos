from django.db import models


# Create your models here.
class News1(models.Model):
    name = models.TextField()
    des = models.TextField()
    data = models.TextField()
    category = models.TextField()
    def __str__(self):
        return self.name
