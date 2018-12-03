from django.urls import path, re_path
from .views import DashboardView

urlpatterns = [
    
    path('dashboard', DashboardView.as_view(),name='dashboard'),
    
 ]