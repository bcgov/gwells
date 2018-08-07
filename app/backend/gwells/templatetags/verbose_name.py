from django import template
register = template.Library()

@register.filter
@register.simple_tag
def verbose_name(instance, field_name):
    """
    Returns verbose_name for a field.
    """
    return instance._meta.get_field(field_name).verbose_name
