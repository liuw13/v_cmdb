from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class User(AbstractUser):
    nick_name = models.TextField(max_length=64, blank=True)
    location = models.CharField(max_length=32, blank=True)
    birth_date = models.DateField(null=True, blank=True)