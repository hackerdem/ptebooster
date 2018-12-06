from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from order.models import Order
from modules.models import Module, QuestionSection
from membership.models import Membership
from django.contrib.auth import get_user_model
import pytz
from datetime import timedelta, datetime
from recommendation.models import Video

User = get_user_model()
class DashboardView(LoginRequiredMixin,ListView):
    model = Order
    page_title = 'Dashboard'
    template_name = 'dashboard/dashboard.html'


    def get_context_data(self, **kwargs):
        user = User.objects.get(email__iexact=self.request.user)
        utc = pytz.UTC
        time_1 = user.membership_end_date
        time_2 = utc.localize(datetime.now())
        delta = time_1 - time_2
        profile = {
            'type' : user.user_type,
            'expiary' : time_1,
            'remaining_days' : delta.days
        }
        context = super(DashboardView, self).get_context_data(**kwargs)
        context.update({
            'modules' : Module.objects.filter(active=True),
            'section' : QuestionSection.objects.all(),
            'listening' : Module.objects.filter(active=True,question_type='Listening'),
            'reading' : Module.objects.filter(active=True,question_type='Reading'),
            'speaking' : Module.objects.filter(active=True,question_type='Speaking'),
            'writing' : Module.objects.filter(active=True,question_type='Writing'),
            'profile' : profile,
            'membership_list' : Membership.objects.all(),
            'video' : Video.objects.all(),



        })
        return context
    def get_queryset(self):
        return Order.objects.all()