from django import template

register = template.Library()


@register.filter(name='split')
def split(value, sep):
    """ Return the string split by step """
    return value.split(sep)

@register.filter(name="get_path")
def get_path(value, step):
    return value[step:]