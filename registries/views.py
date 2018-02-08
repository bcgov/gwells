from django.http import HttpResponse
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from registries.models import Organization
from registries.serializers import OrganizationListSerializer, OrganizationSerializer

class APIOrganizationListCreateView(ListCreateAPIView):
    """
    get:
    Returns a list of all registered drilling organizations

    post:
    Creates a new drilling organization record
    """

    queryset = Organization.objects.all().select_related('province_state')
    serializer_class = OrganizationSerializer

    def list(self, request):
        queryset = self.get_queryset()
        serializer = OrganizationListSerializer(queryset, many=True)
        return Response(serializer.data)


class APIOrganizationRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    """
    get:
    Returns the specified drilling organization

    put:
    Replaces the specified record with a new one

    patch:
    Updates a drilling organization with the fields/values provided in the request body

    delete:
    Removes the specified drilling organization record
    """

    queryset = Organization.objects.all()
    lookup_field = "org_guid"
    serializer_class = OrganizationSerializer


# Create your views here.
def index(request):
    return HttpResponse("TEST: Driller Register app home index.")
