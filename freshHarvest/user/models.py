from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime
from django.core.validators import MinValueValidator, MaxValueValidator

class Customer(AbstractUser):
    location = models.CharField(max_length=150, blank= True)

    def __str__(self):
        return self.first_name+ " " + self.last_name

class Farmer(models.Model):
    farmer_name = models.CharField(max_length=255)
    farm_name = models.CharField(max_length=100)
    location = models.CharField(max_length=150)
    description = models.TextField()

    def __str__(self):
        return self.farmer_name


class Product (models.Model):
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE, related_name="products")
    product_name = models.CharField(max_length=100)
    stock = models.IntegerField()
    price = models.FloatField(
        validators=[
            MinValueValidator(1.0)
        ]
    )
    harvest_date = models.DateField()
    label = models.CharField(max_length=50)

    def __str__(self):
        return self.product_name


class Review (models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="reviews")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    date = models.DateField(auto_now_add=True)
    content = models.TextField()
    stars = models.IntegerField(validators=[
        MinValueValidator(1),
        MaxValueValidator(5)
    ])

    def __str__(self):
        return self.stars

class Discount(models.Model):
    discount_code = models.CharField(max_length=50, unique=True)
    value = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return self.discount_code


class Cart(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="carts")
    status = models.CharField(max_length=20, default="active")
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE, related_name="carts")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="carts")
    quantity = models.IntegerField()

class Order(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="orders")
    cart = models.ForeignKey(Cart, on_delete=models.SET_NULL, null=True, blank=True) 
    total_amount = models.FloatField()
    mode_payment = models.CharField(max_length=50)
    delivery_date = models.DateField(null=True, blank=True)
    delivery_address = models.TextField(default="")
    order_date = models.DateField()

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    discount= models.ForeignKey(Discount, on_delete=models.SET_NULL, null=True, blank= True, related_name= 'orders')

