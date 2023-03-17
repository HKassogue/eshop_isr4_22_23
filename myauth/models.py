from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class MyUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="+", 
                                null=False, blank=False)
    avatar = models.ImageField(null=True, blank=True, upload_to="images/users/")


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="+", 
                                null=False, blank=False)
    avatar = models.ImageField(null=True, blank=True, upload_to="images/customers/")
    address = models.CharField(max_length=20, null=True, blank=True)
    city = models.CharField(max_length=20, null=True, blank=True)
    country = models.CharField(max_length=20, null=True, blank=True)
    zipcode = models.CharField(max_length=20, null=True, blank=True)
    tel = models.CharField(max_length=20, null=True, blank=True)
    