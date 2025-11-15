from django import template

register = template.Library()

@register.filter
def subtract(value, arg):
    """Resta arg de value"""
    try:
        return float(value) - float(arg)
    except (ValueError, TypeError):
        return value

@register.filter
def multiply(value, arg):
    """Multiplica value por arg"""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return value

@register.filter(name='div')
def divide(value, arg):
    """Divide value por arg"""
    try:
        return int(value) // int(arg)
    except (ValueError, TypeError, ZeroDivisionError):
        return value