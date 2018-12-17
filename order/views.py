from django.shortcuts import render, get_object_or_404
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import redirect
from django.views.generic import ListView, View
from .forms import OrderForm, InitialOrderForm
from modules.forms import BuyForm
from membership.models import Membership
from .models import Order
from purchase.models import Gateway
from contact.notification_texts import ORDER_ERROR_1
from  stats.models import QuestionStatistics
# Create your views here.

class OrderSummaryView(ListView):
    model = Membership
    page_title = 'New Order'
    template_name = 'order/new_order.html'

    def get_context_data(self, **kwargs):
        member_type = self.request.GET.get('member_type','')
        membership = Membership.objects.get(member_type=member_type)
        print('ah',QuestionStatistics.objects.filter(membership_type=member_type, is_active=True, question_section='Listening').count())     
        context = super(OrderSummaryView, self).get_context_data( **kwargs)
        context.update({
            'object' : membership,
            'listening' : QuestionStatistics.objects.filter(membership_type__presedence__lte=membership.presedence, is_active=True, question_section='Listening').count(),
            'reading' : QuestionStatistics.objects.filter(membership_type__presedence__lte=membership.presedence, is_active=True, question_section='Reading').count(),
            'speaking' : QuestionStatistics.objects.filter(membership_type__presedence__lte=membership.presedence, is_active=True, question_section='Speaking').count(),
            'writing' : QuestionStatistics.objects.filter(membership_type__presedence__lte=membership.presedence, is_active=True, question_section='Writing').count(),
        })
        return context
    def get(self,request):
        return super(OrderSummaryView,self).get(request) 

    def post(self, request, *args, **kwargs):
        error = None      
        form = BuyForm(request.POST)
        if form.is_valid():
            try:
                data = form.cleaned_data
                obj= Membership.objects.get(member_type=data['member_type'])
                try:
                    Order.objects.order(self.request.user,obj.price,obj)
                    
            
                    return redirect('order_create')
                except Exception:
                    error = ORDER_ERROR_1
            except Exception:
                error = ORDER_ERROR_1 
        else:
            error = ORDER_ERROR_1
        return render(request,'order/new_order.html', {'error':error})
class OrderCreateView(ListView):
    # revise this class later
    model = Order 
    template_name = 'purchase/checkout.html'

    def get_context_data(self, **kwargs):
        order = Order.objects.filter(customer=self.request.user).order_by('-created_on')[0]
        gateways = Gateway.objects.filter(is_active=True)
        return super(OrderCreateView, self).get_context_data(gateways=gateways, order=order, **kwargs)
        
    def get(self,request):
        return super(OrderCreateView,self).get(request)

   
        