# shop/templatetags/custom_filters.py
from django import template

register = template.Library()

@register.filter(name='add')
def add(value, arg):
    """Adds the arg to the value."""
    return value + arg
