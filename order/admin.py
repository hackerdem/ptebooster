from django.contrib import admin
from .models import Order
# Register your models here.

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['customer','total','membership_type','order_status','payment_status','created_on','order_number',]

