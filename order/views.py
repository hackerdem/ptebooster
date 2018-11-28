from django.shortcuts import render, get_object_or_404
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import redirect
from django.views.generic import ListView, View
from .forms import OrderForm, InitialOrderForm
from modules.forms import BuyForm
from membership.models import Membership
from .models import Order
from purchase.models import Gateway
# Create your views here.

class OrderSummaryView(ListView):
    model = Membership
    page_title = 'New Order'
    template_name = 'order/new_order.html'

    def get_context_data(self, **kwargs):
        member_type = self.request.GET.get('member_type','') 
        member_obj =  Membership.objects.get(member_type=member_type)    
        return super(OrderSummaryView, self).get_context_data(object=member_obj, **kwargs)
        
    def get(self,request):
        return super(OrderSummaryView,self).get(request) 

    def post(self, request, *args, **kwargs):       
        form = BuyForm(request.POST)
        if form.is_valid():
            try:
                data = form.cleaned_data
                print(data)
                obj= Membership.objects.get(member_type=data['member_type'])
                try:
                    Order.objects.order(self.request.user,obj.price,obj)
                    
            
                    return redirect('order_create')
                except Exception as e:
                    print(e)
            except Exception as e :
                print(e) # chages this prints later 
        else:
            print(form)
class OrderCreateView(ListView):
    model = Order 
    template_name = 'purchase/checkout.html'

    def get_context_data(self, **kwargs):
        order = Order.objects.filter(customer=self.request.user).order_by('-created_on')[0]
        gateways = Gateway.objects.filter(is_active=True)
        return super(OrderCreateView, self).get_context_data(gateways=gateways, order=order, **kwargs)
        
    def get(self,request):
        return super(OrderCreateView,self).get(request)

    def post(self,request):

        

        if form.is_valid():
            print('calid')
        else:
            print('invalid')
        