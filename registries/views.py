from django.http import HttpResponse
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from registries.models import Organization
from registries.serializers import DrillerListSerializer, DrillerSerializer

class APIDrillerListCreateView(ListCreateAPIView):
    """
    get:
    Return a list of all registered drilling organizations

    post:
    Create a new drilling organization instance
    """
    
    queryset = Organization.objects.all().select_related('province_state')
    serializer_class = DrillerSerializer

    def list(self, request):
        queryset = self.get_queryset()
        serializer = DrillerListSerializer(queryset, many=True)
        return Response(serializer.data)


class APIDrillerRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    """
    get:
    Return the specified drilling organization

    patch:
    Updates the specified drilling organization with the fields/values provided in the request body

    delete:
    Removes the specified drilling organization record
    """

    queryset = Organization.objects.all()
    lookup_field = "org_guid"
    serializer_class = DrillerSerializer


# Create your views here.
def index(request):
    return HttpResponse("TEST: Driller Register app home index.")
