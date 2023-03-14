from django.contrib import admin
from .models import *

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Image)
admin.site.register(Order)
admin.site.register(Order_details)
admin.site.register(Arrival)
admin.site.register(Arrival_details)