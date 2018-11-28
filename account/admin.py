from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username','email','user_type','membership_end_date','membership_start_date','first_name','is_active','is_staff','verify_code','verify_time_limit','reset_code','reset_time_limit','created_on']
    readonly_fields=('password',)