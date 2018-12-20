from django import template
register = template.Library()


@register.filter
@register.simple_tag
def exclude_zero_decimals(value):
    """
    Returns removes trailing zeros from decimal numbers if all numbers after
    the decimal are zeros.
    """
    if value is None:
        return value

    str_value = str(value)

    if '.' in str_value:
        value_length = len(str_value)
        decimal_index = str_value.index('.')

        str_decimals = str_value[decimal_index+1:value_length]

        if str_decimals.count(str_decimals[0]) == len(str_decimals) and str_decimals[0] == '0':
            str_value = str_value[0:decimal_index]

    return str_value
