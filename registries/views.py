from django.http import HttpResponse
from django.utils import timezone
from rest_framework import filters
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin
from registries.models import Organization, Person, ContactAt, RegistriesApplication
from registries.permissions import IsAdminOrReadOnly
from registries.serializers import (
    ApplicationSerializer,
    OrganizationListSerializer,
    OrganizationSerializer,
    OrganizationAdminSerializer,
    PersonSerializer,
    PersonAdminSerializer,
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


class APILimitOffsetPagination(LimitOffsetPagination):
    """
    Provides LimitOffsetPagination with custom parameters.
    """

    max_limit = 100

class APIOrganizationListCreateView(AuditCreateMixin, ListCreateAPIView):
    """
    get:
    Returns a list of all registered drilling organizations

    post:
    Creates a new drilling organization record
    """

    permission_classes = (IsAdminOrReadOnly,)

    # prefetch related objects for the queryset to prevent duplicate database trips later
    queryset = Organization.objects.all() \
        .select_related('province_state') \
        .prefetch_related(
            'contacts',
            'contacts__person',
        )

    # Allow searching against fields like company name, address, name or registration of company contacts
    filter_backends = (filters.SearchFilter,)
    search_fields = (
        'name',
        'street_address',
        'city',
        'contacts__person__first_name',
        'contacts__person__surname',
        'contacts__person__applications__file_no'
        )

    pagination_class = APILimitOffsetPagination

    def get_queryset(self):
        """
        Filter out organizations with no registered drillers if user is anonymous
        """
        qs = self.queryset
        if not self.request.user.is_staff:
            qs = qs \
                .filter(contacts__person__applications__registrations__status__code='ACTIVE') \
                .distinct() # filtering on ContactAt model related items can return duplicate companies
        return qs

    def get_serializer_class(self):
        """
        Return appropriate serializer for user
        Admin serializers have more fields, including audit fields
        """
        if (self.request.user.is_staff):
            return OrganizationAdminSerializer
        return OrganizationSerializer

    # override list() in order to use a modified serializer (with fewer fields) for the list view
    def list(self, request):
        """
        Returns the list response, using the list serializer class (serializes fewer fields than detail view)
        """
        queryset = self.get_queryset()
        filtered_queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(filtered_queryset)
        if page is not None:
            serializer = OrganizationListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = OrganizationListSerializer(filtered_queryset)
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

    permission_classes = (IsAdminOrReadOnly,)

    # 'pk' and 'id' have been replaced by 'org_guid' as primary key for Organization model
    lookup_field = "org_guid"
    serializer_class = OrganizationSerializer

    # prefetch related province, contacts and person records to prevent future additional database trips
    queryset = Organization.objects.all() \
        .select_related('province_state') \
        .prefetch_related(
            'contacts',
            'contacts__person',
        )

    def get_queryset(self):
        """
        Filter out organizations with no registered drillers if user is anonymous
        """
        qs = self.queryset
        if not self.request.user.is_staff:
            qs = qs \
                .filter(contacts__person__applications__registrations__status__code='ACTIVE') \
                .distinct()
        return qs

    def get_serializer_class(self):
        if (self.request.user.is_authenticated()):
            return OrganizationAdminSerializer
        return self.serializer_class


class APIPersonListCreateView(AuditCreateMixin, ListCreateAPIView):
    """
    get:
    Returns a list of all person records

    post:
    Creates a new person record
    """

    permission_classes = (IsAdminOrReadOnly,)

    # Allow searching on name fields, names of related companies, etc.
    filter_backends = (filters.SearchFilter,)
    search_fields = (
        'first_name',
        'surname',
        'companies__org__name',
        'companies__org__city',
        'applications__registrations__registration_no'
        )

    pagination_class = APILimitOffsetPagination

    # fetch related companies and registration applications (prevent duplicate database trips)
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

    def get_queryset(self):
        """ Returns Person queryset, removing non-active and unregistered drillers for anonymous users """
        qs = self.queryset
        if not self.request.user.is_staff:
            qs = qs.filter(applications__registrations__status__code='ACTIVE').distinct()
        return qs

    def get_serializer_class(self):
        """ Returns the appropriate serializer for the user """
        if (self.request.user.is_staff):
            return PersonAdminSerializer
        return PersonSerializer

    def list(self, request):
        """ List response using serializer with reduced number of fields """
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

    permission_classes = (IsAdminOrReadOnly,)

    # pk field has been replaced by person_guid
    lookup_field = "person_guid"

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

    def get_queryset(self):
        """
        Returns only registered people (i.e. drillers with active registration) to anonymous users
        """
        qs = self.queryset
        if not self.request.user.is_staff:
            qs = qs.filter(applications__registrations__status__code='ACTIVE')
        return qs

    def get_serializer_class(self):
        if (self.request.user.is_staff):
            return PersonAdminSerializer
        return PersonSerializer


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
    Returns a list of all registration applications

    post:
    Creates a new registries application
    """

    permission_classes = (IsAdminUser,)

    queryset = RegistriesApplication.objects.all() \
        .select_related('person') \
        .prefetch_related(
            'register_set',
            'register_set__registries_activity',
            'register_set__status'
        )

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

    permission_classes = (IsAdminUser,)
    queryset = RegistriesApplication.objects.all().select_related('person')
    lookup_field = "application_guid"
    serializer_class = ApplicationSerializer
