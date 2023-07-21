from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Customers)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAdd)
admin.site.register(ForgetPass)