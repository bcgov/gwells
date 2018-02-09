from django.http import HttpResponse
from django.utils import timezone
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin
from registries.models import Organization, Person, ContactAt
from registries.serializers import OrganizationListSerializer, OrganizationSerializer, PersonSerializer, PersonListSerializer

class AuditCreateMixin(CreateModelMixin):
    """
    Adds who_created and when_created fields when instances are created
    """

    def perform_create(self, serializer):
        serializer.save(
            who_created=self.request.user,
            when_created=timezone.now()
            )


class AuditUpdateMixin(UpdateModelMixin):
    """
    Adds who_updated and when_updated fields when instances are updated
    """

    def perform_update(self, serializer):
        serializer.save(
            who_updated=self.request.user,
            when_updated=timezone.now()
        )


class APIOrganizationListCreateView(AuditCreateMixin, ListCreateAPIView):
    """
    get:
    Returns a list of all registered drilling organizations

    post:
    Creates a new drilling organization record
    """

    queryset = Organization.objects.all().select_related('province_state')
    serializer_class = OrganizationSerializer

    # override list() in order to use a modified serializer (with fewer fields) for the list view
    def list(self, request):
        queryset = self.get_queryset()
        serializer = OrganizationListSerializer(queryset, many=True)
        return Response(serializer.data)


class APIOrganizationRetrieveUpdateDestroyView(AuditUpdateMixin, RetrieveUpdateDestroyAPIView):
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


class APIPersonListCreateView(AuditCreateMixin, ListCreateAPIView):
    """
    get:
    Returns a list of all person records

    post:
    Creates a new person record
    """

    queryset = Person.objects.all().prefetch_related('companies')
    serializer_class = PersonSerializer

    def list(self, request):
        queryset = self.get_queryset()
        serializer = PersonListSerializer(queryset, many=True)
        return Response(serializer.data)


class APIPersonRetrieveUpdateDestroyView(AuditUpdateMixin, RetrieveUpdateDestroyAPIView):
    """
    get:
    Returns the specified person

    put:
    Replaces the specified person record with a new one

    patch:
    Updates a person with the fields/values provided in the request body

    delete:
    Removes the specified person record
    """

    # TODO: For public view, only return registered drillers. Needs to be fixed when registered functionality added.
    # queryset = Person.objects.filter( isRegistered=True )
    queryset = Person.objects.all()
    lookup_field = "person_guid"
    serializer_class = PersonSerializer

    def perform_update(self, serializer):
        serializer.save(
            who_updated=self.request.user,
            when_updated=timezone.now()
        )

# Placeholder for base url.
def index(request):
    return HttpResponse("TEST: Driller Register app home index.")
