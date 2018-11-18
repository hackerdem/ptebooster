from django.shortcuts import render
from django.contrib.auth.views import LoginView as _LoginView
from django.views.generic import FormView
from django.views import View
from django.http import HttpResponseRedirect, HttpResponse
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.contrib.auth import get_user_model, login, logout, authenticate
from .forms import RegisterForm, PasswordResetForm, ForgottenPasswordForm
from .token import account_activation_token
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.template.loader import render_to_string
from django.views.generic import CreateView
from datetime import datetime, timedelta
from membership.models import Membership
import pytz
User = get_user_model()
class LoginView(_LoginView):
    template_name = 'account/login.html'


    def get_context_data(self, **kwargs):
        next_url = self.request.GET.get('next', '')
        return super(LoginView, self).get_context_data(next_url=next_url, **kwargs)

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        if '@' in username:
            try:
                user = User.objects.get(email__iexact=username)
                username = user.username
            except User.DoesNotExist:
                pass

        # Check user membership type and duration before autherntication
        if user.user_type != Membership.objects.get(member_type='Basic') and not user.is_staff:
            utc = pytz.UTC
            time_1 = user.membership_start_date+timedelta(days=91)
            time_2 = utc.localize(datetime.now())
            if time_1 <= time_2:
                user.user_type=Membership.objects.get(member_type='Basic')
                user.membership_start_date=datetime.now()
                user.save()
                # if this is the case send notification
        user = authenticate(username=username,password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                #return HttpResponseRedirect(request.POST.get('next', reverse('home')))
                return HttpResponseRedirect(reverse('home'))
            else:
                error = ('Aplogize we will update this message later')
        
        else:
            error = ('Username and password didn\'t matched, if you forgot your password ....')

        return super(LoginView, self).get(request, error=error)


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
                new_user = User.objects.register(datetime.now(),data['first_name'],data['username'],data['password'],data['email'],usertype, data['last_name'],token,verify_time_limit )
                
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

class ActivationView(CreateView):
    success_url = 'account:login'
    template_name = 'registration/activation.html'
    
    def get(self, request, uidb64, token): 
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and token==user.verify_code:
            user.is_active = True
            user.save()
            # delete this later login(request, user)
            # return redirect('home')
            return HttpResponse('Account has been activated!') #render(request,'account/activation-done.html')
        else:
            return HttpResponse('Activation link is invalid!')

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
            except(TypeError, ValueError, OverflowError, User.DoesNotExist):
                pass


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
                    return HttpResponse('Password reset successful!') #render(request,'account/activation-done.html')
                except:
                    return HttpResponse('Password reset is not successful')
            else:
                return HttpResponse('Activation link is invalid!')
        else:
            pass