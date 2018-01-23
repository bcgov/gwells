from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

class RegistryHomeView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'registry/index.html'

    def get_context_data(self, **kwargs):
        """
        Return the context for the page.
        """
        context = super(RegistryHomeView, self).get_context_data(**kwargs)
        return context
