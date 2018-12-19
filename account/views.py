from django.shortcuts import render
from django.contrib.auth.views import LoginView as _LoginView
from django.views.generic import FormView, CreateView
from django.views import View
from django.http import HttpResponseRedirect, HttpResponse
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.contrib.auth import get_user_model, login, logout, authenticate
from .forms import RegisterForm, PasswordResetForm, ForgottenPasswordForm, ResendActivationForm, LoginForm
from .token import account_activation_token
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.template.loader import render_to_string
from datetime import datetime, timedelta
from membership.models import Membership
from contact.models import Notification
import pytz
from django.core.exceptions import ObjectDoesNotExist
from contact.notification_texts import MEMBERSHIP_ACNOWLEGEMENT, MEMBERSHIP_EXPIRED
utc = pytz.UTC
User = get_user_model()
class LoginView(FormView):
    form_class = LoginForm
    template_name = 'account/login.html'

    def get_context_data(self, **kwargs):
        next_url = self.request.GET.get('next', '')
        return super(LoginView, self).get_context_data(next_url=next_url, **kwargs)

    def get(self, request, *args, **kwargs):
        form = LoginForm()
        return super(LoginView, self).get(request,form=form)

    def post(self, request,*args, **kwargs):
        username = request.POST['username']
        password = request.POST['password']
        if username or password is None:
            if '@' in username:
                try:
                    user = User.objects.get(email__iexact=username)
                    username = user.username
                    # Check user membership type and duration before autherntication
                    if user.user_type != Membership.objects.get(member_type='Basic'):
                        
                        time_1 = user.membership_end_date
                        time_2 = utc.localize(datetime.now())
                        delta = (time_1-time_2).days
                        notification_count = Notification.objects.filter(created_on__contains=datetime.now().date()).count()
                        if time_1 <= time_2:
                            user.user_type=Membership.objects.get(member_type='Basic')
                            user.membership_start_date = datetime.now()
                            user.membership_end_date = datetime.now() + timedelta(days=91)
                            user.save()
                            # if this is the case send notification
                            
                            if notification_count==0:
                                Notification.create(subject='{} membership expiary'.format(user.user_type),
                                                body=MEMBERSHIP_EXPIRED,
                                                receiver_id=user.id,
                                                created_by=User.objects.filter(is_staff=True)[0])
                        elif delta in [15,10,5,1] and notification_count==0:
                            Notification.create(subject='{} membership expiary'.format(user.user_type),
                                                body=MEMBERSHIP_ACNOWLEGEMENT,
                                                receiver_id=user.id,
                                                created_by=User.objects.filter(is_staff=True)[0])
                    
                    if user.is_active:
                        try:
                            user = authenticate(username=username,password=password)
                            login(request, user)
                            return HttpResponseRedirect(reverse('dashboard'))
                        except:
                            error = ('Username and password have not matched.')
                            pass
                    else:
                        error = ('Account for this email address has not been activated. \
                                If you haven\'t received activation mail, please use the \
                                link below to receive another activation link.')
                except User.DoesNotExist:
                    error = ('User with this email does not exist.')
                    pass
            else:
                error = ('Username should be an email.')
        else:
            error = ('Both username and password should be provided.')
        return render(request,'account/login.html',{'error':error})


class LogoutView(View):

    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('home'))

class RegisterView(FormView):
    form_class = RegisterForm
    page_title = 'Register'
    template_name = 'account/register.html'

    def get_context_data(self, **kwargs):
        next_url = self.request.GET.get('next', '')
        return super(RegisterView, self).get_context_data(next_url=next_url, **kwargs)

    def get(self, request):
        form = RegisterForm()
        return super(RegisterView, self).get(request, form=form)

    def post(self, request, *args, **kwargs):
        error = None
        success = None
        form = RegisterForm(request.POST)
        if form.is_valid():
            try:
                data = form.cleaned_data
                token = account_activation_token.make_token(data)
                verify_time_limit = datetime.now() + timedelta(days=1)
                usertype = Membership.objects.get(member_type='Basic')
                new_user = User.objects.register(datetime.now(),data['first_name'],data['email'],data['password'],data['email'],usertype, data['last_name'],token,verify_time_limit )
                
                # send activation mail to non-active user
                uid=urlsafe_base64_encode(force_bytes(new_user.pk)).decode()
                current_site = get_current_site(request)
                mail_subject = 'Activate your keypte account.'
                message = render_to_string('account/confirmation_mail.html', {
                                            'user': new_user,
                                            'domain': current_site.domain,
                                            'uid':uid,
                                            'token':token,
                                            })
                to_email = form.cleaned_data.get('email')
                email = EmailMessage(
                        mail_subject, message, to=[to_email]
                         )
                email.send()

                next_url = request.POST.get('next',None)
                if next_url:
                    return HttpResponseRedirect(next_url)
                else:
                    return render(request, 'account/register_done.html',{'user':new_user})
                
            except ValidationError as e:
                error = e.message
        
        return super(RegisterView, self).get(request, form=form, error=error, success=success)


class ResendActivationView(FormView):
    form_class = ResendActivationForm
    page_title = 'Resend Link'
    template_name = 'account/activation_resent.html'
    def get_context_data(self, **kwargs):
        next_url = self.request.GET.get('next', '')
        return super(ResendActivationView, self).get_context_data(next_url=next_url, **kwargs)

    def get(self, request):
        form = ResendActivationForm()
        return super(ResendActivationView, self).get(request, form=form)

    def post(self, request, *args, **kwargs):
        error = None
        success = None
        form = ResendActivationForm(request.POST)
        if  form.is_valid():
            data = form.cleaned_data
            try:
                user = User.objects.get(email=data['email'])
                data['first_name'] = user.first_name
                
                token = account_activation_token.make_token(data)
                verify_time_limit = datetime.now() + timedelta(days=1)
                
                user.verify_code, user.verify_time_limit = token, verify_time_limit
                user.save()

                uid=urlsafe_base64_encode(force_bytes(user.pk)).decode()
                current_site = get_current_site(request)
                mail_subject = 'Activate your keypte account.'
                message = render_to_string('account/confirmation_mail.html', {
                                            'user': user,
                                            'domain': current_site.domain,
                                            'uid':uid,
                                            'token':token,
                                            })
                to_email = form.cleaned_data.get('email')
                email = EmailMessage(
                        mail_subject, message, to=[to_email]
                         )
                email.send()
                next_url = request.POST.get('next',None)
                if next_url:
                    return HttpResponseRedirect(next_url)
                else:
                    return render(request, 'account/register_done.html',{'user':user})
                
            except ValidationError as e:
                error = e.message
                pass
            except ObjectDoesNotExist:
                pass
        return super(ResendActivationView, self).get(request, form=form, error=error, success=success)

class ActivationView(CreateView):
    
    success_url = 'account:login'
    template_name = 'registration/activation.html'
    def get(self, request, uidb64, token): 
        error = None
        success = None
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
            error = 'A user with this email has not been found. Please contact with us if you believe there is a mistake.'
        if user is not None:
            if token==user.verify_code and utc.localize(datetime.now())<= user.verify_time_limit:
                user.is_active = True
                user.save()
                success = 'Activation is successfully completed.'
            
            else:
                error = 'Invalid activation token has been provided.'
        return render(request, 'account/activation-done.html',{'user':user, 'success':success, 'error':error})


class ForgottenPasswordView(FormView):
    # Password Recovery
    form_class= ForgottenPasswordForm
    template_name = 'account/forgotten_password.html'
    page_title = 'Forgotten Password'

    def get_context_data(self, **kwargs):
        next_url = self.request.GET.get('next', '')
        return super(ForgottenPasswordView, self).get_context_data(next_url=next_url, **kwargs)

    def get(self,request):
        form = ForgottenPasswordForm()
        return super(ForgottenPasswordView, self).get(request, form=form)
    def post(self, request, *args, **kwargs):
        error = None
        success = None
        data={}
        forgot_form = ForgottenPasswordForm(request.POST)
        if forgot_form.is_valid():
            email = forgot_form.cleaned_data['email']
        if email:
            email = email.strip()
            try:
                user = User.objects.get(email__iexact=email)
                data['email'], data['first_name'] = user.email, user.first_name
                token = account_activation_token.make_token(data)
                user.reset_code = token
                user.save()
                # send activation mail to non-active user
                uid=urlsafe_base64_encode(force_bytes(user.pk)).decode()
                current_site = get_current_site(request)
                mail_subject = 'Password reset instructions.'
                message = render_to_string('account/password_reset_mail.html', {
                                            'user': user,
                                            'domain': current_site.domain,
                                            'uid':uid,
                                            'token':token,
                                            })
                to_email = data['email']
                email = EmailMessage(
                        mail_subject, message, to=[to_email]
                         )
                email.send()
                success = ('A password reset email has been sent to your email address, \
                        check your email in 5 minutes.')
            except User.DoesNotExist:
                error = ('User with this email does not exist.')
                pass
            except( TypeError, ValueError, OverflowError):
                error = ('There has been an error, activation code \
                         could not be sent, please try later. If this error persists please contact with us.')
                pass

        return render(request,'account/forgotten_password.html',{'error':error, 'success':success})

class PasswordResetView(FormView):
    form_class = PasswordResetForm
    success_url = 'account:login'
    template_name = 'registration/password_reset.html'
    
    def get_context_data(self, **kwargs):
        next_url = self.request.GET.get('next', '')
        return super(PasswordResetView, self).get_context_data(next_url=next_url, **kwargs)

    def get(self, request, uidb64, token): 
        form = PasswordResetForm()
        return super(PasswordResetView, self).get(request, form=form, uidb64=uidb64, token=token)
        
    def post(self, request, uidb64, token):
        error = None
        success = None
        form = PasswordResetForm(request.POST)

        if form.is_valid():
            try:
                uid = force_text(urlsafe_base64_decode(uidb64))
                user = User.objects.get(pk=uid)
            except(TypeError, ValueError, OverflowError, User.DoesNotExist):
                user = None
            if user is not None and user.is_active and token==user.reset_code:
               
                data = form.cleaned_data
                try:
                    user.set_password(data['password'])
                    user.save()
                    success = ('Password reset is successful.')
                except:
                    error = ('Password reset has not been successful.')
            else:
                error = ('Activation link is invalid.')
        else:
            error = ('There has been an error, please try again later')

        return render(request,'registration/password_reset.html', {'error':error,'success':success})