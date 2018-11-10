# replace all these these are just placekeper
from django.urls import path, re_path
from account.views import LoginView, RegisterView, LogoutView, ActivationView, \
                        ForgottenPasswordView, PasswordResetView


urlpatterns = [
    
    path('login', LoginView.as_view(),name='account_login'),
    
]