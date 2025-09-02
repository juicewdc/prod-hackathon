from django.db import models
from firstapp.models import ProjectUser

class Blog(models.Model):
    user = models.ForeignKey(ProjectUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
