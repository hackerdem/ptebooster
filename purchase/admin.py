from django.contrib import admin
from .models import Gateway,GatewayParameters,Transaction, TransactionParam

@admin.register(Gateway)
class GatewayAdmin(admin.ModelAdmin):
    list_display = ('name', 'account', 'is_active','logo')
    list_filter = ('account',)
    search_fields = ('name', 'account',)
    

@admin.register(GatewayParameters)
class GatewayParametersAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'value', 'gateway')
    list_filter = ('gateway__name', 'name',)
    search_fields = ('gateway', 'name',)
    

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('gateway', 'order', 'description','error','status','amount','updated_on','created_on')

@admin.register(TransactionParam)
class TransactionParamAdmin(admin.ModelAdmin):
    list_display = ('transaction', 'name', 'value','created_on')
  