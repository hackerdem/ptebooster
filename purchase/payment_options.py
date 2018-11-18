import stripe
import paypalrestsdk
from django.shortcuts import redirect, HttpResponseRedirect
import logging,sysconfig
from django.core.exceptions import ImproperlyConfigured
from django.utils.crypto import get_random_string
from django.contrib.auth import get_user_model
from django.db import transaction
from .models import GatewayParameters,Transaction
from order.models import Order
from membership.models import Membership
logger = logging.getLogger('django.request')

class Paypal:

    def __init__(self,gateway):
        self.gateway = gateway
        self.mode = 'sandbox' if gateway.is_sandbox else 'live'
       
        params= dict((param.name,param.value) for param in self.gateway.params.all())
    
        if 'client_id' in params and params['client_id']:
            client_id = params['client_id']
       
        else:
            raise ImproperlyConfigured('"client_id" parameter not configured for Paypal gateway{}'.format(self.gateway.account))

        if 'client_secret' in params and params['client_secret']:
            client_secret = params['client_secret']
        else:
            raise ImproperlyConfigured('"client_secret" parameter not configured for PayPal gateway {}.'.format(self.gateway.account))

        try:
        
            self.api = paypalrestsdk.Api({
                    'mode':self.mode,
                    'client_id':client_id,
                    'client_secret':client_secret
                    })
         
        except Exception as e:
            print(e)
     
    def create_account_payment(self,user):
        access_token = get_random_string(20)
        order = Order.objects.get(customer=user)

        """with transaction.atomic():
            payment_txn = Transaction.objects.create(gateway=self.gateway,
                                                     order=order,
                                                     description='Transaction for order {}'.format(order.id),
                                                     amount=order.total,
                                                     status=Transaction.STATUS_PROCESSING
                                                        )
            payment_txn.add_param('access_token',access_token)
            payment_txn.save()
            print('gqqqq')"""
        try:
            payment = {
                'intent':'sale',
                'redirect_urls':{
                'return_url':'http://192.168.0.16:8000/purchase/payment',
                'cancel_url':'http://192.168.0.16/purchase/cancel',
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
            payment = paypalrestsdk.Payment(payment, api=self.api)
            payment_created = payment.create()
        except Exception as e:
            logger.error('Failed to process PayPal account(transaction_id: {})'.format(payment_txn.id))
            logger.exception(e)
            raise('upps failed')
       
        if payment_created:
            for link in payment.links:
                if link.rel == "approval_url":
                # Convert to str to avoid Google App Engine Unicode issue
                # https://github.com/paypal/rest-api-sdk-python/pull/58
                    approval_url = str(link.href)
                    print("Redirect for approval: %s" % (approval_url))
            try:
                order.order_status = Order.ORDER_COMPLETE
                order.payment_status = Order.PAYMENT_AUTHORIZED
                order.save()
                User = get_user_model()
                user = User.objects.get(email__iexact=user)
                user.user_type = Membership.objects.get(member_type=order.membership_type)
                user.save()
            except Exception as e:
                print(e)
                    
           
        else:
            logger.error('Failed to process payment(transaction_id:{})'.format('payment_txn.id'),extra={'error':'payment.error'})
            """with transaction.atomic():
                payment_txn.status = Transaction.STATUS_FAILED
                payment_txn.error_message = payment.error['message']"""
            raise('upps')
        return approval_url      

            
    