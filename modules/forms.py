from django import forms
from membership.models import Membership

class BuyForm(forms.Form):
    member_type = forms.CharField(label='member_type', max_length=100)

   