from django import template
from django.contrib.auth.models import Group

register = template.Library()

@register.filter(name='has_group')
def has_group(user, group_name):

    if Group.objects.filter(name=group_name).exists():
        group = Group.objects.get(name=group_name)
        user_groups = user.groups.all()
        authorized = group in user_groups
        return authorized
    else:
        authorized=False
        return authorized
