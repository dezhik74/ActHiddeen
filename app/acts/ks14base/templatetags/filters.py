from django import template
register = template.Library()


@register.filter
def verbose_name(value, arg):
    return value._meta.get_field(arg).verbose_name


@register.filter
def verbose_name_plural(obj):
    return obj._meta.verbose_name_plural