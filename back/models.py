from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=45, null=False, blank=False, unique=True)
    slug = models.CharField(max_length=35, null=False, blank=False, unique=True)
    active = models.BooleanField(default=True, null=False, blank=False)
    created_at = models.DateTimeField(null=False, blank=False, auto_now_add=True)
    image = models.ImageField(null=True, blank=True, upload_to='images/categories/')
    parent = models.ForeignKey('Category', null=True, blank=True, 
            related_name='subcategories', on_delete=models.SET_NULL)

    class Meta:
        verbose_name_plural = "categories"
        ordering = ["-created_at", "name"]

    def __str__(self):
        return f"{self.name}"

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
    category = models.ForeignKey('Category', null=True, blank=False, on_delete=models.SET_NULL, related_name='products')
    
    class Meta:
        ordering = ["-created_at", 'name']
	
    def __str__(self):
        return f"{self.id} : {self.name}"
    

class Image(models.Model):
    name = models.CharField(max_length=30, null=False, blank=False)
    file = models.ImageField(null=False, blank=True, upload_to="images/products/")
    product = models.ForeignKey("Product", on_delete=models.CASCADE, 
            related_name="images")
    
    def __str__(self):
        return f"{self.name} de {self.product.name}"
    

class Order(models.Model):
    reference = models.CharField(max_length=30, null=False, blank=False, unique=True)
    created_at = models.DateTimeField(null=False, blank=False, auto_now_add=True)
    completed = models.BooleanField(default=False, null=True, blank=False)
    products = models.ManyToManyField("Product", through="Order_details", related_name="orders")

    class Meta:
        ordering = ["-created_at", "reference"]

    def __str__(self):
        return f"{self.reference}"
    

class Order_details(models.Model):
    order = models.ForeignKey('Order', null=True, blank=False, on_delete=models.SET_NULL)
    product = models.ForeignKey('Product', null=True, blank=False, on_delete=models.SET_NULL)
    quantity = models.SmallIntegerField(default=1, null=True, blank=False)
    price = models.FloatField(default=1, null=True, blank=False)

    class Meta:
        verbose_name = "Order details"
        verbose_name_plural = "Orders details"


class Arrival(models.Model):
    created_at = models.DateTimeField(null=False, blank=False, auto_now_add=True)
    closed_at = models.DateTimeField(null=True, blank=True, default=False)
    closed = models.BooleanField(default=False, null=True, blank=True)
    products = models.ManyToManyField("Product", through="Arrival_details", related_name="arrivals")

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.id}"
    

class Arrival_details(models.Model):
    arrival = models.ForeignKey('Arrival', null=True, blank=False, on_delete=models.SET_NULL)
    product = models.ForeignKey('Product', null=True, blank=False, on_delete=models.SET_NULL)
    quantity = models.SmallIntegerField(default=1, null=True, blank=False)

    class Meta:
        verbose_name = "Arrival details"
        verbose_name_plural = "Arrivals details"


class Payment(models.Model):
    reference = models.CharField(max_length=30, null=False, blank=False, unique=True)
    order = models.OneToOneField("Order", null=True, blank=False, on_delete=models.PROTECT, related_name="payment")
    payed_at = models.DateTimeField(null=False, blank=False, auto_now_add=True)
    mode = models.CharField(max_length=30, null=False, blank=False, default="CASH")
    details = models.TextField(max_length=255, null=True, blank=True)
