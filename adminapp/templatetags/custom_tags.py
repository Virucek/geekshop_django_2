from datetime import datetime

from django import template

register = template.Library()


@register.filter(name='curr_datetime')
def _current_datetime(date):
    if not date:
        date = datetime.now()
    return date
