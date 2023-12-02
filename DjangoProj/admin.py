from django.contrib import admin

from myapp.models import Product, Order, User

admin.site.register(Product)
admin.site.register(Order)
admin.site.register(User)
