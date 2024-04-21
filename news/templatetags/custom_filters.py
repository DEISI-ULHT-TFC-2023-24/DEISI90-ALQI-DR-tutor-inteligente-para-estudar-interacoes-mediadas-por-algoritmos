from django import template

register = template.Library()


@register.filter
def is_not_digit(value):
    return not value.isdigit()
