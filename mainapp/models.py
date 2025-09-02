from django.db import models
from firstapp.models import ProjectUser

class Tickets(models.Model):
    user = models.ForeignKey(ProjectUser, on_delete=models.CASCADE)
    date_start = models.DateField(null=True)
    date_end = models.DateField(null=True)
    trip_plan = models.TextField(null=True)
    country = models.CharField(max_length=50)
    price = models.IntegerField(default=0)
    ticket = models.BinaryField(null=True)
