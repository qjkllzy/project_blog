import time
from django import template
register=template.Library()

@register.filter
def dtime(value):
    newtime=value.strftime('%Y/%m/%d')
    return ('发布于:%s'%newtime)