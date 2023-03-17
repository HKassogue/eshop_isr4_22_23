from django.db import models
from django.contrib.auth.models import User


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
    customer = models.ForeignKey('myauth.Customer', null=True, blank=False, 
                                 on_delete=models.SET_NULL, related_name='orders')

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

    def __str__(self):
        return f"{self.order.reference} : {self.product.name} x {self.quantity}"


class Arrival(models.Model):
    created_at = models.DateTimeField(null=False, blank=False, auto_now_add=True)
    closed_at = models.DateTimeField(null=True, blank=True, default=False)
    closed = models.BooleanField(default=False, null=True, blank=True)
    products = models.ManyToManyField("Product", through="Arrival_details", related_name="arrivals")

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.id} on {self.created_at}"
    

class Arrival_details(models.Model):
    arrival = models.ForeignKey('Arrival', null=True, blank=False, on_delete=models.SET_NULL)
    product = models.ForeignKey('Product', null=True, blank=False, on_delete=models.SET_NULL)
    quantity = models.SmallIntegerField(default=1, null=True, blank=False)

    class Meta:
        verbose_name = "Arrival details"
        verbose_name_plural = "Arrivals details"

    def __str__(self):
        return f"{self.arrival.id} : {self.product.name} x {self.quantity}"


class Payment(models.Model):
    reference = models.CharField(max_length=30, null=False, blank=False, unique=True)
    order = models.OneToOneField("Order", null=True, blank=False, on_delete=models.PROTECT, related_name="payment")
    payed_at = models.DateTimeField(null=False, blank=False, auto_now_add=True)
    mode = models.CharField(max_length=30, null=False, blank=False, default="CASH")
    details = models.TextField(max_length=255, null=True, blank=True)

    class Meta:
        ordering = ["-payed_at", "reference"]

    def __str__(self):
        return f"Payment of {self.order} at {self.payed_at}"


class Review(models.Model):
    rate = models.FloatField(null=False, blank=False)
    comment = models.TextField(null=True, blank=True)
    name = models.CharField(max_length=30, null=False, blank=False)
    email = models.CharField(max_length=30, null=False, blank=False)
    product = models.ForeignKey('Product', null=False, blank=False, on_delete=models.CASCADE, related_name='reviews')
    created_at = models.DateTimeField(null=False, blank=False, auto_now_add=True)

    class Meta:
        ordering = ["-created_at", "-rate"]

    def __str__(self):
        return f"{self.product.name} rated {self.rate} at {self.created_at}"


class Like(models.Model):
    email = models.CharField(max_length=30, null=False, blank=False)
    liked = models.BooleanField(default=True, null=False, blank=False)
    product = models.ForeignKey('Product', null=False, blank=False, on_delete=models.CASCADE)
    created_at = models.DateTimeField(null=False, blank=False, auto_now_add=True)

    class Meta:
        ordering = ["-created_at", "-liked"]

    def __str__(self):
        return f"{self.product.name}" + ("liked" if self.liked else "unliked") + f" at {self.created_at}"


class Coupon(models.Model):
    code = models.CharField(max_length=30, null=False, blank=False, unique=True)
    description = models.TextField(max_length=255, null=True, blank=True)
    coupon_type = models.CharField(max_length=20, null=True, blank=True, default="Percent")
    discount = models.IntegerField(default=1, null=True, blank=False)
    max_usage = models.SmallIntegerField(default=1, null=True, blank=False)
    validity = models.DateTimeField(null=False, blank=False)
    is_valid = models.BooleanField(default=True, null=False, blank=False)
    created_at = models.DateTimeField(null=False, blank=False, auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.code}"
    

class Delivery(models.Model):
    address = models.CharField(max_length=30, null=False, blank=False)
    country = models.CharField(max_length=20, blank=True, null=True)
    zipcode = models.CharField(max_length=10, null=False, blank=False)
    city = models.CharField(max_length=30, null=False, blank=False)
    price = models.FloatField(default=0, null=False, blank=False)
    state = models.CharField(max_length=30, null=False, blank=False, default="Delivered")
    order = models.ForeignKey('Order', null=False, blank=False, on_delete=models.PROTECT, related_name='deliveries')
    delivered_by = models.ForeignKey('myauth.MyUser', null=False, blank=True, on_delete=models.PROTECT, related_name='+')
    delivered_at = models.DateTimeField(null=False, blank=False, auto_now_add=True)

    class Meta:
        ordering = ["-delivered_at", "-state"]
    
    def __str__(self):
        return f"Delivery of {self.order.reference} : {self.state}"
    

class Alert(models.Model):
    status = models.CharField(max_length=30, null=False, blank=False)
    type = models.CharField(max_length=30, null=False, blank=False)
    details = models.TextField(null=False, blank=False)
    created_at = models.DateTimeField(null=False, blank=False, auto_now_add=True)
    traited_at = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    
    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.id} at {self.created_at} : {self.status}"


class Faq(models.Model):
    type = models.CharField(max_length=30, null=False, blank=False)
    question = models.TextField(null=False, blank=False, max_length=255)
    answer = models.TextField(null=False, blank=False, max_length=255)
    created_at = models.DateTimeField(null=False, blank=False, auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.question}"