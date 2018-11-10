from django.db import models
from ptebooster import settings
from membership.models import Membership
from django.utils.crypto import get_random_string

class OrderManager(models.Manager):
    def order(self,user,total,membership_type):
        receipt_number = get_random_string(12)

        order = self.create(
            customer=user,
            total=total,
            membership_type=membership_type,
            order_status='PE',
            payment_status='PE',
            receipt_number=receipt_number
        )
class Order(models.Model):
    ORDER_STATUS = (
        ('PE','Pending'),
        ('PR', 'Processing'),
        ('CO','Completed'),
        ('CA','Camceled')
    )

    PAYMENT_STATUS = (
        ('PE','Pending'),
        ('AU','Authorized'),
        ('PA','Paid'),
        ('VO','Void')
    )

    customer = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete='PROTECT', null=True, blank=True)
    total = models.DecimalField(max_digits=9, decimal_places=2)
    membership_type = models.ForeignKey(Membership,on_delete='PROTECT', null=True, blank=True)
    order_status = models.CharField(max_length=15, choices=ORDER_STATUS)
    payment_status = models.CharField(max_length=15, choices=PAYMENT_STATUS)
    receipt_number = models.CharField(max_length=100)
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)

    objects = OrderManager()

    def __str__(self):
        return self.id
    
    