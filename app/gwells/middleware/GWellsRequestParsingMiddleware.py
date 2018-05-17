#attribution https://thihara.github.io/Django-Req-Parsing/

from django.http import HttpResponseBadRequest
from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponse

class GWellsRequestParsingMiddleware(MiddlewareMixin):

    def get(self, request):
        pass

    def post(self, request):
        pass

    def put(self, request):
        request.PUT = request.POST

    def delete(self, request):
        pass

    def process_request(self, request):
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
