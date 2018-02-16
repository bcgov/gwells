from django.http import HttpResponse
from django.utils import timezone
from rest_framework import filters
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin
from registries.models import Organization, Person, ContactAt, RegistriesApplication
from registries.serializers import (
    ApplicationSerializer,
    OrganizationListSerializer,
    OrganizationSerializer,
    PersonSerializer,
    PersonListSerializer,
)

class AuditCreateMixin(CreateModelMixin):
    """
    Adds create_user and create_date fields when instances are created
    """

    def perform_create(self, serializer):
        serializer.save(
            create_user=self.request.user.get_username(),
            create_date=timezone.now()
            )


class AuditUpdateMixin(UpdateModelMixin):
    """
    Adds update_user and update_date fields when instances are updated
    """

    def perform_update(self, serializer):
        serializer.save(
            update_user=self.request.user.get_username(),
            update_date=timezone.now()
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

    serializer_class = PersonSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('first_name', 'surname', 'companies__org__name')
    max_limit = 1

    def get_queryset(self):
        if (self.request.user.is_authenticated()):
            queryset = Person.objects \
                    .all() \
                    .prefetch_related(
                        'companies',
                        'companies__org',
                        'applications',
                        'applications__registrations',
                        'applications__registrations__registries_activity',
                        'applications__registrations__status'
                    )
        else:
            queryset = Person.objects \
                    .filter(applications__registrations__status__code='ACTIVE') \
                    .prefetch_related(
                        'companies',
                        'companies__org',
                        'applications',
                        'applications__registrations',
                        'applications__registrations__registries_activity',
                        'applications__registrations__status'
                    )
        return queryset

    

    def list(self, request):
        queryset = self.get_queryset()
        filtered_queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(filtered_queryset)
        if page is not None:
            serializer = PersonListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = PersonListSerializer(filtered_queryset, many=True)
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


# Placeholder for base url.
def index(request):
    return HttpResponse("TEST: Driller Register app home index.")


#
# APPLICATION ENDPOINT VIEWS
# To confirm entry point to these views, see urls.py urlpatterns list ("application" entries)
#

class APIApplicationListCreateView(AuditCreateMixin, ListCreateAPIView):
    """
    get:
    Returns a list of all registered drilling organizations

    post:
    Creates a new drilling organization record
    """

    queryset = RegistriesApplication.objects.all().prefetch_related('register_set', 'register_set__registries_activity', 'register_set__status').select_related('person')
    serializer_class = ApplicationSerializer


class APIApplicationRetrieveUpdateDestroyView(AuditUpdateMixin, RetrieveUpdateDestroyAPIView):
    """
    get:
    Returns the specified drilling application

    put:
    Replaces the specified record with a new one

    patch:
    Updates a drilling application with the set of values provided in the request body

    delete:
    Removes the specified drilling application record
    """

    queryset = RegistriesApplication.objects.all().select_related('person')
    lookup_field = "application_guid"
    serializer_class = ApplicationSerializer
