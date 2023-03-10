from django.contrib import admin
from .models import Product, ProductAttribute, Banner, UserAddressBook, CartOrder, CartOrderItems, Category, Brand, Size, Color
# Register your models here.

admin.site.register([Product, ProductAttribute, Banner, UserAddressBook, CartOrder, CartOrderItems, Category, Brand, Size, Color])