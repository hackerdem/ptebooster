
from django import forms
from .models import ContactData




class ContactDataForm(forms.ModelForm):
    class Meta:
        model = ContactData
        fields = (
            'name',
            'email',
            'subject',
            'message',
        )
        widgets ={
            'name' : forms.TextInput(attrs=({'required':''})),
            'email' : forms.TextInput(attrs=({'required':''})),
            'subject' : forms.TextInput(attrs=({'required':''})),
            'message' : forms.TextInput(attrs=({'required':''})),
        }
    def clean_name(self):
        name = self.cleaned_data['name']
        return name

    def clean_email(self):
        email = self.cleaned_data['email']
        return email

    def clean_subject(self):
        subject = self.cleaned_data['subject']
        return subject

    def clean_message(self):
        message = self.cleaned_data['message']
        return message