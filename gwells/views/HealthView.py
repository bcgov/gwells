from django.views import generic

class HealthView(generic.TemplateView):
    def health(request):
        return HttpResponse(WellActivityType.objects.count())
