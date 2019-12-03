# attribution https://thihara.github.io/Django-Req-Parsing/
import time
from random import randint
import logging

from django.http import HttpResponseBadRequest
from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponse

from gwells.settings.base import get_env_variable


logger = logging.getLogger(__name__)


class GWellsRequestParsingMiddleware(MiddlewareMixin):

    def get(self, request, **kwargs):
        pass

    def post(self, request, **kwargs):
        pass

    def put(self, request, **kwargs):
        request.PUT = request.POST

    def delete(self, request, **kwargs):
        pass

    def process_request(self, request, **kwargs):
        _method = request.POST.get('_method')

        if _method:
            if _method.upper() == 'GET':
                self.get(request)
            elif _method.upper() == 'PUT':
                self.put(request)
            elif _method.upper() == 'POST':
                self.post(request)
            elif _method.upper() == 'DELETE':
                self.delete(request)
            else:
                message = 'Unsupported _method: ' + _method
                return HttpResponse(message, status=500)
