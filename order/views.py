from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, View
from .forms import OrderForm
from membership.models import Membership
from .models import Order
# Create your views here.

class OrderSummaryView(ListView):
    model = Membership
    page_title = 'New Order'
    template_name = 'order/new_order.html'

    def get_queryset(self):
        return Membership.objects.filter(member_type__iexact=self.kwargs['type'])

class OrderCreateView(ListView):
    model = Order 
    template_name = 'purchase/checkout.html'

    def get_context_data(self, **kwargs):
        obj = Membership.objects.get(member_type=self.kwargs['type'])
        Order.objects.order(self.request.user,obj.price,obj)
        
        order_details = Order.objects.get(customer=self.request.user)
        return super(OrderCreateView, self).get_context_data(order=order_details, **kwargs)
        
    def get(self,request,type):
        
        
        
        return super(OrderCreateView,self).get(request)