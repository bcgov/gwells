from django.db.models import Transform

"""
Exposes the 'abs' operator to query operations.
"""
class AbsoluteValue(Transform):
    lookup_name = 'abs'
    function = 'ABS'
