# attribution https://thihara.github.io/Django-Req-Parsing/
import time
from random import randint
import logging
import threading

from django.http import HttpResponseBadRequest
from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponse
from markupsafe import Markup

from gwells.settings.base import get_env_variable

_thread_local = threading.local()

logger = logging.getLogger(__name__)

def get_current_user():
    return getattr(_thread_local, 'user', None)

class GWellsRequestParsingMiddleware(MiddlewareMixin):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            _thread_local.user = request.user
        else:
            _thread_local.user = None
        response = self.get_response(request)
        return response

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
                _method = Markup.escape(_method)
                message = 'Unsupported _method: ' + _method
                return HttpResponse(message, status=500)
