from django.db import models
from ptebooster import settings
from membership.models import Membership
from django.utils.crypto import get_random_string

class OrderManager(models.Manager):
    def order(self,user,total,membership_type):
        order_number = get_random_string(12)

        order = self.create(
            customer=user,
            total=total,
            membership_type=membership_type,
            order_status='PE',
            payment_status='PE',
            order_number=order_number
        )
class Order(models.Model):
    
    ORDER_PENDING = 'PE'
    ORDER_PROCESSING = 'PR'
    ORDER_COMPLETE = 'CO'
    ORDER_CANCELLED = 'CA'
    ORDER_STATUSES = ((ORDER_PENDING, 'Pending'),
                      (ORDER_PROCESSING, 'Processing'),
                      (ORDER_COMPLETE, 'Complete'),
                      (ORDER_CANCELLED, 'Cancelled'))

    # Payment statuses
    PAYMENT_PENDING = 'PE'
    PAYMENT_AUTHORIZED = 'AU'
    PAYMENT_PAID = 'PA'
    PAYMENT_PARTIALLY_REFUNDED = 'PR'
    PAYMENT_REFUNDED = 'RE'
    PAYMENT_VOID = 'VO'
    PAYMENT_STATUSES = ((PAYMENT_PENDING, 'Pending'),
                        (PAYMENT_AUTHORIZED, 'Authorized'),
                        (PAYMENT_PAID, 'Paid'),
                        (PAYMENT_PARTIALLY_REFUNDED, 'Partially Refunded'),
                        (PAYMENT_REFUNDED, 'Refunded'),
                        (PAYMENT_VOID, 'Void'))

    customer = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,unique=False)
    total = models.DecimalField(max_digits=9, decimal_places=2)
    membership_type = models.ForeignKey(Membership,on_delete=models.PROTECT, null=True, blank=True)
    order_status = models.CharField(max_length=15, choices=ORDER_STATUSES)
    payment_status = models.CharField(max_length=15, choices=PAYMENT_STATUSES)
    order_number = models.CharField(max_length=100)
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)

    objects = OrderManager()
    class Meta:
        indexes = [
            models.Index(fields=['customer'], name='order_idx'),
            models.Index(fields=['created_on'], name='order_created_on_idx'),
        ]
    def __str__(self):
        return self.order_number
    
    