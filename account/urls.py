from django.urls import path, re_path
from account.views import LoginView, RegisterView, LogoutView, ActivationView, \
                        ForgottenPasswordView, PasswordResetView, ResendActivationView


urlpatterns = [
    
    path('login', LoginView.as_view(),name='account_login'),
    path('logout', LogoutView.as_view(),name='account_logout'),
    path('register', RegisterView.as_view(),name='account_register'),
    path('forgotten-password', ForgottenPasswordView.as_view(),name='account_forgot_password'),
    path('resend-activation', ResendActivationView.as_view(),name='resend_activation_link'),
    path('password-reset/<uidb64>/<token>/', PasswordResetView.as_view(),name='account_password_reset'),
    path('activate/<uidb64>/<token>/',ActivationView.as_view(), name='activation'),
]