from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.html import format_html


User = get_user_model()
class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username','password')

class RegisterForm(forms.ModelForm):
    
    password = forms.CharField(widget=forms.PasswordInput(attrs={'required':''}),
                                min_length=8, max_length=50, error_messages={'required':'Please enter your new password.'})

    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'required':''}), max_length=50, error_messages={'required':'Please re-enter your new password for confirmation.'})
    confirm_email = forms.CharField(widget=forms.TextInput(attrs={'required':''}),error_messages={'required':'Please confirm your email.'})
    class Meta:
        model = User
        fields = ('email','first_name','last_name')
        widgets = {
            
            'email': forms.TextInput(attrs=({'required': ''})),
            'first_name': forms.TextInput(attrs=({'required': ''})),
        }
        error_messages = {
            'username': {'required': 'Please choose a username.'},
            'first_name': {'required': 'Please enter your first name.'}

        }

    def clean_email(self):
        email = self.cleaned_data['email']

        if not email:
            raise ValidationError('Please enter your email address.')

        if User.objects.filter(email__iexact=email).exists():
            message = format_html('User with this Email account already exists.Please click <a href="{}">here</a> if you forgot your password', reverse('account_forgot_password'))
            raise ValidationError(message)
        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        return username
    def clean_confirm_email(self):
        confirm_email = self.cleaned_data['confirm_email']
        if 'email' in self.cleaned_data and self.cleaned_data['email'] != confirm_email:
            raise forms.ValidationError("Emails do not match.")
        return confirm_email

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if not first_name:
            raise ValidationError('Please enter your first name.')
        return first_name
    def clean_confirm_password(self):
        confirm_password = self.cleaned_data['confirm_password']
        if 'password' in self.cleaned_data and self.cleaned_data['password'] != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return confirm_password

class PasswordResetForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'required':''}),
                                min_length=8, max_length=50, error_messages={'required':'Please enter your new password.'})
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'required':''}), max_length=50, error_messages={'required':'Please re-enter your new password for confirmation.'})

    def clean_confirm_password(self):
        confirm_password = self.cleaned_data['confirm_password']
        if 'password' in self.cleaned_data and self.cleaned_data['password'] != confirm_password:
            raise forms.ValidationError("Your new password and confirm password didn't matched.")
        return confirm_password

class ForgottenPasswordForm(forms.Form):
    email = forms.EmailField()

    def clean_email(self):
        email = self.cleaned_data['email']
        return email
        
class ResendActivationForm(forms.Form):
    email = forms.EmailField()

    def clean_email(self):
        email = self.cleaned_data['email']
        return email
