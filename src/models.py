from django.db import models
from django.db.models.expressions import F

# Create your models here.
class Coffee(models.Model):
    name = models.CharField(max_length=100)
    amount = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    order_id = models.CharField(max_length=100)
    paid = models.BooleanField(default=False)