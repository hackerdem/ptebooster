from django.shortcuts import render,get_object_or_404
from .payment_options import Paypal
from django.http import Http404, HttpResponseRedirect, HttpResponse
from purchase.models import Gateway, Transaction, TransactionParam
from django.urls import reverse
import json

def process_payment(request):
    if request.method == "POST" and request.is_ajax():
        selected_gateway = request.POST['payment_gateway']
        gateway_name=selected_gateway
        gateway = Gateway.objects.get(name=gateway_name)
        try:
            processor = Paypal(gateway)
            url = processor.create_account_payment(request.user)
            return HttpResponse(url)
        except Exception:
            return HttpResponse('error')
    
def payment_process_result(request, transaction_id, access_token, success):
  
    payment_txn = Transaction.objects.get(id=int(transaction_id))
    check_value = TransactionParam.objects.get(transaction=int(transaction_id))

    if str(check_value) != str(access_token):
            raise Http404
    
    if request.method == "GET":
        gateway = payment_txn.gateway

        try:
            if gateway.name == Gateway.PAYPAL:
                processor = Paypal(gateway)            
                if success:
                    payer_id = request.GET['PayerID']
                    payment_id = request.GET['paymentId']
                    processor.execute_account_payment(payment_id,payer_id, payment_txn, request.user)
                    return HttpResponseRedirect(reverse('dashboard'))
                else:
                    """ processor.cancel_account_payment(payment_txn, request.user)
                    request.session['processing_message'] = 'Your order has been cancelled.'"""
                    
                    return HttpResponseRedirect('pappyppy')
            else:
                print('add other gateways ')

        except Exception as e:
            print(e,'last error')
