# replace all these these are just placekeper
from django.urls import path, re_path
from .views import process_payment, payment_process_result


urlpatterns = [
    
    path('payment', process_payment,name='process_payment'),
    path('payment-result/<transaction_id>/<access_token>',payment_process_result,{'success':True}, name='payment_process_success'),
    path('payment-result/<transaction_id>/<access_token>',payment_process_result,{'success':True}, name='payment_process_cancel')
    
    
]