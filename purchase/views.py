from django.shortcuts import render,get_object_or_404
from .payment_options import Paypal
from django.http import Http404, HttpResponseRedirect
from purchase.models import Gateway, Transaction, TransactionParam
from django.urls import reverse
def process_payment(request):
    try:
        try:
            gateway_name='PP'
            g = Gateway.objects.all()
           
            gateway = Gateway.objects.get(name=gateway_name)
            try:
                processor = Paypal(gateway)
            except Exception as e:
                print('proecssor',e)
        except Exception as e:
            print(e)
        return HttpResponseRedirect(processor.create_account_payment(request.user))
    except Exception as e:
        print(e)

def payment_process_result(request, transaction_id, access_token, success):
  
    payment_txn = Transaction.objects.get(id=int(transaction_id))
    check_value = TransactionParam.objects.get(transaction=int(transaction_id))

    if str(check_value) != str(access_token):
    
            raise Http404
    
   
    
    if request.method == "GET":
        order = payment_txn.order
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
                print('execution error')

        except Exception as e:
            print(e,'last error')
