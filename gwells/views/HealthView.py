from django.views import generic
from django.http import HttpResponse
from ..models import WellActivityType

class HealthView(generic.TemplateView):
    def health(request):
        return HttpResponse(WellActivityType.objects.count())
