from django.views import generic
from gwells.models import Survey

class RegistryView(generic.TemplateView):
    template_name = 'gwells/registry.html'

    def get_context_data(self, **kwargs):
        """
        Return the context for the page.
        """
        context = super(RegistryView, self).get_context_data(**kwargs)
        surveys = Survey.objects.order_by('create_date')
        context['surveys'] = surveys
        context['page'] = 'r'

        return context
