from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=30, unique=True, null=False, blank=False)
    slug = models.CharField(max_length=50, unique=True, null=False, blank=False)
    price = models.FloatField(null=False, blank=False)
    description = models.TextField(max_length=255, null=True, blank=True)
    details = models.TextField(max_length=255, null=True, blank=True)
    stock = models.IntegerField(default=1, null=True, blank=True)
    active = models.BooleanField(default=True, null=False, blank=True)
    likes = models.IntegerField(default=0, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=False, blank=True)
    
    class Meta:
        ordering = ['name']
	
    def __str__(self):
        return f"{self.id} : {self.name}"