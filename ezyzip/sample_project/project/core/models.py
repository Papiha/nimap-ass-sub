from django.db import models
from django.contrib.auth.models import User


class BaseModel(models.Model):
    class Meta:
        abstract = True
    created_by = models.CharField(max_length=256)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_by = models.CharField(max_length=256, blank=True)
    modified_on = models.DateTimeField(auto_now_add=True)


class Client(BaseModel):
    class Meta:
        db_table = "client"
    name = models.CharField(max_length=256)
    project = models.CharField(max_length=256, blank=True)
    users = models.ManyToManyField(User, blank=True)
