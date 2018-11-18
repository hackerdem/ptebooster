# replace all these these are just placekeper
from django.urls import path, re_path
from .views import process_payment


urlpatterns = [
    
    path('payment', process_payment,name='process_payment'),
    
    
]