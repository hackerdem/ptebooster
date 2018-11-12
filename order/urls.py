from django.urls import path, re_path
from .views import OrderCreateView

urlpatterns = [
    
    path('new_order', OrderCreateView.as_view(),name='new_order'),

]