from django.contrib import admin
from .models  import Customer, Farmer, Product, Review, Discount, Cart, CartItem, Order, OrderItem
# Register your models here.
admin.site.register(Customer)
admin.site.register(Farmer)
admin.site.register(Product)
admin.site.register(Review)
admin.site.register(Discount)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)