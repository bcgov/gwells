from django.views import generic
from django.shortcuts import render

class TestErrorsView(generic.TemplateView):
    def test_500_view(request):
        # Return an "Internal Server Error" 500 response code.
        return render(request, '500.html',status=500)

    def test_404_view(request):
        # Return an "Internal Server Error" 500 response code.
        return render(request, '404.html',status=404)
