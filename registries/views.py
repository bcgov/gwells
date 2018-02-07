from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse
from rest_framework.generics import ListAPIView
from registries.models import Organization
from registries.serializers import DrillerListSerializer

class APIDrillerListView(ListAPIView):
    queryset = Organization.objects.all().select_related('province_state')
    serializer_class = DrillerListSerializer

# Create your views here.
def index(request):
    return HttpResponse("TEST: Driller Register app home index.")
