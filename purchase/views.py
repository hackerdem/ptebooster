from django.shortcuts import render,get_object_or_404,redirect
from .payment_options import Paypal, Stripe
from django.http import Http404, HttpResponseRedirect, HttpResponse
from purchase.models import Gateway, Transaction, TransactionParam
from django.urls import reverse
import json
from contact import notification_texts
def process_payment(request):

    if request.method == "POST" and request.is_ajax():
        selected_gateway = request.POST['payment_gateway']
        gateway_name=selected_gateway
        gateway = Gateway.objects.get(name=gateway_name)
       
        try:
            if selected_gateway == 'PP':
                processor = Paypal(gateway)
                url = processor.create_account_payment(request.user)
                return HttpResponse(url)
            
        except Exception:
            return HttpResponse('error')
    elif request.method == "POST":
        selected_gateway = request.POST.get('gateway')
        print(selected_gateway)
        gateway = Gateway.objects.get(name=selected_gateway)
        if selected_gateway == 'ST':
                token = request.POST.get('stripeToken')
                if token:
                    processor = Stripe(gateway)
                    res = processor.create_payment(request.user, token )
                    if res == 'success':
                        return render(request,'purchase/checkout.html',{'success': notification_texts.PAYMENT_SUCCESS})
            
                    else:
                        return render(request,'purchase/checkout.html',{'error':notification_texts.PAYMENT_ERROR_1})
        else:
            return render(request,'purchase/checkout.html',{'error':notification_texts.STRIPE_CODE_ERROR_1})
    else:
        return HttpResponseRedirect(reverse('dashboard')) 
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
                    return render(request,'purchase/checkout.html',{'success': notification_texts.PAYMENT_SUCCESS})
                else:
                    return render(request,'purchase/checkout.html',{'error':notification_texts.PAYMENT_ERROR_1})
            else:
                return render(request,'purchase/checkout.html',{'error':notification_texts.PAYPAL_GATEWAY_ERROR_1})

        except Exception:
            return HttpResponseRedirect(reverse('dashboard'))
