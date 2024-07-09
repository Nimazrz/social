from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    date_of_birth= models.DateField(null=True, blank=True)
    bio= models.TextField(null=True, blank=True)
    photo=models.ImageField(upload_to='account-image',null=True, blank=True)
    job=models.CharField(max_length=250, null=True, blank=True)
    phone=models.CharField(max_length=11, null=True, blank=True)