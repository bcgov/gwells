from django.views import generic
from django.http import HttpResponse
from ..models import WellActivityCode

class HealthView(generic.TemplateView):
    def health(request):
        return HttpResponse(WellActivityCode.objects.count())
