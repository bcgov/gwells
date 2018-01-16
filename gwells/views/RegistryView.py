from django.views import generic

class RegistryView(generic.TemplateView):
    template_name = 'gwells/registry.html'

    def get_context_data(self, **kwargs):
        """
        Return the context for the page.
        """
        context = super(RegistryView, self).get_context_data(**kwargs)
        return context
