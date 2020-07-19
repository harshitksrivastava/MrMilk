from django.contrib import admin
from .models import Product, SubCategory, Category, Brand, Subscription, Order

# Register your models here.
admin.site.register(Product)
admin.site.register(SubCategory)
admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Subscription)
admin.site.register(Order)
