from django.views.generic import ListView,TemplateView
import re
from .models import Membership

class MembershipListView(ListView):
    model = Membership
    template_name='membership/membership.html'
    def get_queryset(self):    
        qs = super().get_queryset() 
        queryset = qs.filter(is_active=True)
        return queryset
   