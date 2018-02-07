from django.http import HttpResponse
from rest_framework.generics import ListAPIView, RetrieveAPIView
from registries.models import Organization
from registries.serializers import DrillerListSerializer, DrillerDetailSerializer

class APIDrillerListView(ListAPIView):
    queryset = Organization.objects.all().select_related('province_state')
    serializer_class = DrillerListSerializer


class APIDrillerDetailView(RetrieveAPIView):
    queryset = Organization.objects.all()
    lookup_field = "org_guid"
    serializer_class = DrillerDetailSerializer


# Create your views here.
def index(request):
    return HttpResponse("TEST: Driller Register app home index.")
