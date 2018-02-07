from django.shortcuts import render

from django.conf import settings
from django.http import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse("TEST: Driller Register app home index.")