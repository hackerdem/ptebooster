from django.contrib import admin
from .models import ContactData


@admin.register(ContactData)
class ContactDataAdmin(admin.ModelAdmin):
    list_display = ['request_number','email','created_on','is_registered','is_paid_member','name','subject','message']
    readonly_fields=('request_number','email','created_on')