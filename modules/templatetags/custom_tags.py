from django import template
from random import shuffle
from membership.models import Membership
from django.contrib.auth import get_user_model
register = template.Library()
User = get_user_model()

@register.filter
def strip(value):
    return (value.strip(',.:; ')).lower()

@register.filter
def shuffle_list(answer):
    shuffle(answer)
    return answer 

@register.filter()
def to_int(value):
    return int(value)

@register.filter
def id_check(user):
    current_user = User.objects.get(email__iexact=user)
    user_type = current_user.user_type
    user_membership = Membership.objects.get(member_type__iexact=user_type)
    return int(user_membership.presedence)
    