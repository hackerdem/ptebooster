import stripe
import paypalrestsdk
import logging


class Paypal:

    def __init__(self,paypal):
        self.paypal = paypal
        self.mode = 'sandbox'