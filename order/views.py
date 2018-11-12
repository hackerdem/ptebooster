from django.shortcuts import render
from django.views.generic import FormView
from .forms import OrderForm
# Create your views here.

class OrderCreateView(FormView):
    form_class = OrderForm
    page_title = 'New Order'
    template_name = 'order/new_order.html'

    def get_context_data(self, **kwargs):
        next_url = self.request.GET.get('next','')
        return super(OrderCreateView, self).get_context_data(next_url=next_url, **kwargs)

    def get(self, request):
        form = OrderForm()
        return super(OrderCreateView, self).get(request, form=form)
