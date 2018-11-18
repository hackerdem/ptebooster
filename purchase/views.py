from django.shortcuts import render,get_object_or_404
from .payment_options import Paypal
from django.http import Http404, HttpResponseRedirect
from purchase.models import Gateway, Transaction, TransactionParam

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