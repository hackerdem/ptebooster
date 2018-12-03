from django.shortcuts import render,get_object_or_404
from .payment_options import Paypal
import logging,sysconfig
from django.http import Http404, HttpResponseRedirect
from purchase.models import Gateway, Transaction, TransactionParam
from django.utils.crypto import get_random_string
from django.core.exceptions import ImproperlyConfigured
import paypalrestsdk
from order.models import Order

logger = logging.getLogger('django.request')
def process_payment(request):
    print('a')
    try:
        
        gateway = Gateway.objects.get(name='PP')
        mode = 'sandbox' if gateway.is_sandbox else 'live'
        params= dict((param.name,param.value) for param in gateway.params.all())
        if 'client_id' in params and params['client_id']:
            client_id = params['client_id']
            print('d')
        else:
            raise ImproperlyConfigured('"client_id" parameter not configured for Paypal gateway{}'.format(self.gateway.account))

        if 'client_secret' in params and params['client_secret']:
            client_secret = params['client_secret']
        else:
            raise ImproperlyConfigured('"client_secret" parameter not configured for PayPal gateway {}.'.format(self.gateway.account))
        print('f')  
        try:
            print('api start')
            api = paypalrestsdk.Api({
                    'mode':mode,
                    'client_id':client_id,
                    'client_secret':client_secret
                    })
            print('api done')
        except Exception as e:
            print ('api',e)

        access_token = get_random_string(20)
        order = Order.objects.get(customer=request.user)
        try:
            payment = {
                'intent':'sale',
                'redirect_urls':{
                'return_url':'http://127.0.0.1/modules',
                'cancel_url':'http://127.0.0.1/purchase/cancel',
                },
                'payer':{'payment_method':'paypal',
                },
                'transactions':[{
                    'item_list':{
                        'items':[{
                            'name':str(order.membership_type),
                            'sku':str(order.membership_type),
                            'currency': 'AUD',
                            'quantity':1,
                            'price':str(order.total)
                            }]
                    },
                    'amount':{
                        'total':str(order.total),
                        'currency':'AUD',
                        'details':{
                            'subtotal':str(order.total),
                            'tax':str(0),
                            
                        }
                    },
                    'description':'Payment for order #{}'.format(order.id)
                }],
            }
            logger.info('Processing PayPal account.', extra=payment)
            payment = paypalrestsdk.Payment(payment, api=api)
            payment_created = payment.create()
        except Exception as e:
            logger.error('Failed to process PayPal account(transaction_id:)')
            logger.exception(e)
        if payment_created:
            for link in payment.links:
                if link.rel == "approval_url":
                # Convert to str to avoid Google App Engine Unicode issue
                # https://github.com/paypal/rest-api-sdk-python/pull/58
                    approval_url = str(link.href)
                    print("Redirect for approval: %s" % (approval_url))
        return HttpResponseRedirect(approval_url) 
    except Exception as e:
        print (e)