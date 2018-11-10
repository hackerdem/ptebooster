from django.db import models

# Create your models here.

class PaymentGateways(models.Model):

    PAYMENT_CHOICES = (
                        ('PP','Paypal'),
                        ('ST','Stripe'),
                        ('AM','Amazon')

    )
    name = models.CharField(primary_key=True, max_length=15, choices=PAYMENT_CHOICES)
    account = models.CharField(max_length=100)
    is_active = models.BooleanField(default=False)
    is_sandbox = models.BooleanField(default=False)

    def __str__(self):
        return '{} -- {}'.format(self.get_name_display(),self.account)

    @classmethod
    def get_options(cls):
        return list(cls.objects.filter(is_active=True))


class OptionParameters(models.Model):
    payment_option = models.ForeignKey(PaymentGateways,on_delete='CASCADE', related_name='payment_opt')
    name = models.CharField(max_length=250)
    value = models.CharField(max_length=500)
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'payment_method_parameters'
        verbose_name_plural = 'Payment Method Parameters'

    def __str__(self):
        return '{} -- {}'.format(self.name,self.value)
