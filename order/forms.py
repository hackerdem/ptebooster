from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from membership.models import Membership

User = get_user_model()


class OrderForm(forms.ModelForm):
    member_type = forms.ModelChoiceField(queryset=Membership.objects.all().order_by('is_active'))
    class Meta:
        model = Membership
        fields = (
                  'price',
                  'duration',
                  'total_listening_question',
                  'total_reading_question',
                  'total_speaking_question',
                  'total_writing_question',
                  )
        widgets = {
            'price' : forms.TextInput(attrs=({'readonly':'readonly'})),
            'duration' : forms.TextInput(attrs=({'readonly':'readonly'})),
            'total_listening_question' : forms.TextInput(attrs=({'readonly':'readonly'})),
            'total_reading_question' : forms.TextInput(attrs=({'readonly':'readonly'})),
            'total_speaking_question' : forms.TextInput(attrs=({'readonly':'readonly'})),
            'total_writing_question' : forms.TextInput(attrs=({'readonly':'readonly'})),
        }

    def clean_member_type(self):
        member_type = self.cleaned_data['member_type']
        return member_type