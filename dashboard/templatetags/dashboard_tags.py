from django import template
from django.utils.safestring import mark_safe
register = template.Library()


@register.simple_tag
def pie():
    data = [
         ['Membership', 'Number of Question'],
         ['Basic',     21],
         ['Silver',      34],
         ['Gold',  45],
         ['Diamond', 100],
         
       ]
    img = '<input id="pie" onload="initiateChart()" value="{}" >'.format(str(data))
    
   