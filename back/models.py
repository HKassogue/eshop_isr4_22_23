from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=30, unique=True, null=False, blank=False)
    slug = models.CharField(max_length=50, unique=True, null=False, blank=False)
    price = models.FloatField(null=False, blank=False)
    description = models.TextField(max_length=255, null=True, blank=True)
    details = models.TextField(max_length=255, null=True, blank=True)
    