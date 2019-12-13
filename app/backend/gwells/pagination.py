from collections import OrderedDict
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response


def apiLimitedPagination(limit):
    class C(LimitOffsetPagination):
        """
        Provides LimitOffsetPagination with custom parameters.
        """

        default_limit = limit
        max_limit = limit

        def get_paginated_response(self, data):
            return Response(OrderedDict([
                ('count', self.count),
                ('next', self.get_next_link()),
                ('previous', self.get_previous_link()),
                ('offset', self.offset),
                ('results', data)
            ]))
    return C

APILimitOffsetPagination = apiLimitedPagination(100)
