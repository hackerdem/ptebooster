
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.html import format_html




class ForgottenPasswordForm(forms.Form):
    email = forms.EmailField()

    def clean_email(self):
        email = self.cleaned_data['email']
        return email