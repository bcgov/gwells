from django.http import HttpResponse
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from registries.models import Organization
from registries.serializers import DrillerListSerializer, DrillerSerializer

class APIDrillerListCreateView(ListCreateAPIView):
    queryset = Organization.objects.all().select_related('province_state')
    serializer_class = DrillerSerializer

    def list(self, request):
        queryset = self.get_queryset()
        serializer = DrillerListSerializer(queryset, many=True)
        return Response(serializer.data)


class APIDrillerRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Organization.objects.all()
    lookup_field = "org_guid"
    serializer_class = DrillerSerializer


# Create your views here.
def index(request):
    return HttpResponse("TEST: Driller Register app home index.")
