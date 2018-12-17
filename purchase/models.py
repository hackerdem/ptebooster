from django.db import models
from order.models import Order
# Create your models here.

class Gateway(models.Model):
    PAYPAL = 'PP'
    STRIPE = 'ST'
    AMAZON_PAYMENTS = 'AP'
    PAYMENT_CHOICES = (
                        (PAYPAL,'Paypal'),
                        (STRIPE,'Stripe'),
                        (AMAZON_PAYMENTS,'Amazon')

    )
    name = models.CharField(primary_key=True, max_length=15, choices=PAYMENT_CHOICES)
    account = models.CharField(max_length=100)
    is_active = models.BooleanField(default=False)
    is_sandbox = models.BooleanField(default=False)
    logo = models.ImageField(upload_to='ptebooster/media/icons')

    objects = models.Manager()
    
    def __str__(self):
        return '{} -- {}'.format(self.get_name_display(),self.account)

    @classmethod
    def get_options(cls):
        return list(cls.objects.filter(is_active=True))


class GatewayParameters(models.Model):
    gateway = models.ForeignKey(Gateway,on_delete=models.CASCADE, related_name='params')
    name = models.CharField(max_length=250)
    value = models.CharField(max_length=500)
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        
        verbose_name_plural = 'Payment Method Parameters'

    def __str__(self):
        return '{} -- {}'.format(self.name,self.value)

class Transaction(models.Model):
    STATUS_PENDING = 'PE'
    STATUS_PROCESSING = 'PR'
    STATUS_APPROVED = 'AP'
    STATUS_FAILED = 'FA'
    STATUS_REFUNDED = 'RE'
    STATUSES = ((STATUS_PENDING,'Pending'),
                (STATUS_PROCESSING,'Processing'),
                (STATUS_APPROVED,'Approved'),
                (STATUS_FAILED,'Failed'),
                (STATUS_REFUNDED,'Refunded')
                
                )

    gateway = models.ForeignKey(Gateway,on_delete=models.PROTECT)
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    description = models.CharField(max_length=250)
    error = models.CharField(max_length=1000)
    status = models.CharField(max_length=100, choices=STATUSES)
    amount = models.DecimalField(max_digits=4, decimal_places=2) # change this for larger numbers
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()
    
    def __str__(self):
        return str(self.id)

    def add_param(self, name, value):
        param = TransactionParam(name=name, value=value)
        self.params.add(param,bulk=False)
        return param

    def get_param(self,name):
        param = self.params.get(name=name)
        return param.value

class TransactionParam(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.PROTECT, related_name='params')
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=250)
    created_on = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    class Meta:
        
        verbose_name_plural= 'Transaction Params'
        unique_together = ('transaction', 'name',)

    def __str__(self):
        return self.value