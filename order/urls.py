from django.urls import path, re_path
from .views import OrderSummaryView, OrderCreateView

urlpatterns = [
    
    path('new_order', OrderSummaryView.as_view(),name='new_order'),
    path('order_create', OrderCreateView.as_view(),name='order_create'),

]