from django import template
from random import shuffle
from membership.models import Membership
from modules.models import Module,QuestionSection
from stats.models import QuestionStatistics
from django.contrib.auth import get_user_model
from django.utils.safestring import mark_safe
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
    current_user = User.objects.get(email__exact=user.email)
    user_type = current_user.user_type
    user_membership = Membership.objects.get(member_type__exact=user_type)
    return int(user_membership.presedence)

@register.simple_tag
def count_question(section, user_type, presedence):
    objects = Membership.objects.filter(presedence__lte=int(presedence))
    number_of_question = QuestionStatistics.objects.filter(is_active=True, question_section=section, membership_type__in=objects).count()
    return number_of_question


@register.simple_tag
def highlight(word1, word2, sentence):
    word_together = word1+' '+word2
    sentence_modified = sentence.replace('{}'.format(word_together),'<span class="text-danger">{}</span>'.format(word_together))
    return mark_safe(sentence_modified)