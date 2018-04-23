from collections import OrderedDict
from django.http import HttpResponse, Http404
from django.utils import timezone
from django.views.generic import TemplateView
from django_filters import rest_framework as restfilters
from rest_framework import filters, status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin
from registries.models import Organization, Person, ContactInfo, RegistriesApplication, Register
from registries.permissions import IsAdminOrReadOnly, IsGwellsAdmin
from registries.serializers import (
    ApplicationAdminSerializer,
    ApplicationListSerializer,
    CityListSerializer,
    OrganizationListSerializer,
    OrganizationSerializer,
    OrganizationAdminSerializer,
    OrganizationNameListSerializer,
    PersonSerializer,
    PersonAdminSerializer,
    PersonListSerializer,
    RegistrationAdminSerializer,)


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

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('offset', self.offset),
            ('results', data)
        ]))


class PersonFilter(restfilters.FilterSet):
    """
    Allows APIPersonListView to filter response by city, province, or registration status.
    """
    # city = restfilters.MultipleChoiceFilter(name="organization__city")
    prov = restfilters.CharFilter(name="organization__province_state")
    status = restfilters.CharFilter(name="registrations__status")
    activity = restfilters.CharFilter(
        name="registrations__registries_activity")

    class Meta:
        model = Person
        fields = ('prov', 'status')


class RegistriesIndexView(TemplateView):
    """
    Index page for Registries app - contains js frontend web app
    """
    template_name = 'registries/registries.html'


class OrganizationListView(AuditCreateMixin, ListCreateAPIView):
    """
    get:
    Returns a list of all registered drilling organizations

    post:
    Creates a new drilling organization record
    """

    permission_classes = (IsGwellsAdmin,)
    serializer_class = OrganizationSerializer
    pagination_class = APILimitOffsetPagination

    # prefetch related objects for the queryset to prevent duplicate database trips later
    queryset = Organization.objects.all() \
        .select_related('province_state',) \
        .prefetch_related('person_set',) \
        .filter(expired_date__isnull=True)

    # Allow searching against fields like organization name, address,
    # name or registration of organization contacts
    filter_backends = (filters.SearchFilter,)
    search_fields = (
        'name',
        'street_address',
        'city',
        'person_set__first_name',
        'person_set__surname',
        'person_set__registrations__applications__file_no'
    )

    def get_queryset(self):
        """
        Filter out organizations with no registered drillers if user is anonymous
        """
        qs = self.queryset
        if not self.request.user.is_staff:
            qs = qs \
                .filter(person_set__registrations__status='ACTIVE')
        return qs

    def get_serializer_class(self):
        """
        Return appropriate serializer for user
        Admin serializers have more fields, including audit fields
        """
        if self.request and self.request.user.is_staff:
            return OrganizationAdminSerializer
        return self.serializer_class

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


class OrganizationDetailView(AuditUpdateMixin, RetrieveUpdateDestroyAPIView):
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
        .select_related('province_state',) \
        .prefetch_related('person_set',) \
        .filter(expired_date__isnull=True)

    def get_queryset(self):
        """
        Filter out organizations with no registered drillers if user is anonymous
        """
        qs = self.queryset
        if not self.request.user.is_staff:
            qs = qs \
                .filter(person_set__registrations__status='ACTIVE') \
                .distinct()
        return qs

    def get_serializer_class(self):
        if self.request and self.request.user.is_staff:
            return OrganizationAdminSerializer
        return self.serializer_class

    def destroy(self, request, *args, **kwargs):
        """
        Set expired_date to current date
        """
        try:
            instance = self.get_object()
            instance.expired_date = timezone.now()
            instance.save()
        except Http404:
            pass
        return Response(status=status.HTTP_204_NO_CONTENT)


class PersonListView(AuditCreateMixin, ListCreateAPIView):
    """
    get:
    Returns a list of all person records

    post:
    Creates a new person record
    """

    permission_classes = (IsAdminOrReadOnly,)
    serializer_class = PersonSerializer
    pagination_class = APILimitOffsetPagination

    # Allow searching on name fields, names of related companies, etc.
    filter_backends = (restfilters.DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter)
    filter_class = PersonFilter
    ordering_fields = ('surname', 'organization__name')
    ordering = ('surname',)
    search_fields = (
        'first_name',
        'surname',
        'organization__name',
        'organization__city',
        'registrations__registration_no'
    )

    # fetch related companies and registration applications (prevent duplicate database trips)
    queryset = Person.objects \
        .all() \
        .select_related('organization') \
        .prefetch_related(
            'contact_info',
            'registrations',
            'registrations__registries_activity',
            'registrations__status',
            'registrations__applications',
            'registrations__applications__status_set',
            'registrations__applications__status_set__status',
            'registrations__applications__subactivity',
            'registrations__applications__subactivity__qualification_set',
            'registrations__applications__subactivity__qualification_set__well_class'
        ).filter(
            expired_date__isnull=True
        ).distinct()

    def get_queryset(self):
        """ Returns Person queryset, removing non-active and unregistered drillers for anonymous users """
        qs = self.queryset

        # Search for cities (split list and return all matches)
        # search comes in as a comma-separated querystring param e.g: ?city=Atlin,Lake Windermere,Duncan
        cities = self.request.query_params.get('city', None)
        if cities:
            cities = cities.split(',')
            qs = qs.filter(organization__city__in=cities)

        # Only show active drillers to non-admin users and public
        if not self.request.user.is_staff:
            qs = qs.filter(registrations__status='ACTIVE')

        return qs

    def get_serializer_class(self):
        """ Returns the appropriate serializer for the user """
        if self.request and self.request.user.is_staff:
            return PersonAdminSerializer
        return self.serializer_class

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


class PersonDetailView(AuditUpdateMixin, RetrieveUpdateDestroyAPIView):
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
    serializer_class = PersonSerializer

    # pk field has been replaced by person_guid
    lookup_field = "person_guid"

    queryset = Person.objects \
        .all() \
        .select_related('organization') \
        .prefetch_related(
            'registrations',
            'registrations__registries_activity',
            'registrations__status',
            'registrations__applications',
            'registrations__applications__status_set',
            'registrations__applications__subactivity',
            'registrations__applications__subactivity__qualification_set',
            'registrations__applications__subactivity__qualification_set__well_class'
        ).filter(
            expired_date__isnull=True
        ).distinct()

    def get_queryset(self):
        """
        Returns only registered people (i.e. drillers with active registration) to anonymous users
        """
        qs = self.queryset
        if not self.request.user.is_staff:
            qs = qs.filter(registrations__status='ACTIVE')
        return qs

    def get_serializer_class(self):
        if self.request and self.request.user.is_staff:
            return PersonAdminSerializer
        return self.serializer_class

    def destroy(self, request, *args, **kwargs):
        """
        Set expired_date to current date
        """
        try:
            instance = self.get_object()
            instance.expired_date = timezone.now()
            instance.save()
        except Http404:
            pass
        return Response(status=status.HTTP_204_NO_CONTENT)


class CitiesListView(ListAPIView):
    """
    List of cities with a qualified, registered operator (driller or installer)

    get: returns a list of cities with a qualified, registered operator (driller or installer)
    """
    serializer_class = CityListSerializer
    lookup_field = 'person_guid'
    pagination_class = None
    queryset = Person.objects \
        .exclude(organization__city__isnull=True) \
        .exclude(organization__city='') \
        .select_related(
            'organization',
        ) \
        .distinct('organization__city') \
        .order_by('organization__city') \
        .filter(expired_date__isnull=True)

    def get_queryset(self):
        """
        Returns only registered operators (i.e. drillers with active registration) to anonymous users
        if request has a kwarg 'activity' (accepts values 'drill' and 'install'), queryset
        will filter for that activity
        """
        qs = self.queryset
        if not self.request.user.is_staff:
            qs = qs.filter(registrations__status='ACTIVE')
        if self.kwargs['activity'] == 'drill':
            qs = qs.filter(registrations__registries_activity='DRILL')
        if self.kwargs['activity'] == 'install':
            qs = qs.filter(registrations__registries_activity='PUMP')
        return qs


class RegistrationListView(AuditCreateMixin, ListCreateAPIView):
    """ 
    get:
    List all registration records

    post:
    Create a new well driller or well pump installer registration record for a person
    """

    permission_classes = (IsAdminUser,)
    serializer_class = RegistrationAdminSerializer
    queryset = Register.objects.all() \
        .select_related(
            'person',
            'registries_activity',
            'status',
            'register_removal_reason',) \
        .prefetch_related('applications')


class RegistrationDetailView(AuditUpdateMixin, RetrieveUpdateDestroyAPIView):
    """
    get:
    Returns a well driller or well pump installer registration record

    put:
    Replaces a well driller or well pump installer registration record with a new one

    patch:
    Updates a registration record with new values

    delete:
    Removes the specified registration record from the database
    """

    permission_classes = (IsAdminUser,)
    serializer_class = RegistrationAdminSerializer
    lookup_field = 'register_guid'
    queryset = Register.objects.all() \
        .select_related(
            'person',
            'registries_activity',
            'status',
            'register_removal_reason',) \
        .prefetch_related('applications')


class ApplicationListView(AuditCreateMixin, ListCreateAPIView):
    """
    get:
    Returns a list of all registration applications

    post:
    Creates a new registries application
    """

    permission_classes = (IsAdminUser,)
    serializer_class = ApplicationAdminSerializer
    queryset = RegistriesApplication.objects.all() \
        .select_related(
            'registration',
            'registration__person',
            'registration__registries_activity',
            'registration__status',
            'registration__register_removal_reason')


class ApplicationDetailView(AuditUpdateMixin, RetrieveUpdateDestroyAPIView):
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
    serializer_class = ApplicationAdminSerializer
    queryset = RegistriesApplication.objects.all() \
        .select_related(
            'registration',
            'registration__person',
            'registration__registries_activity',
            'registration__status',
            'registration__register_removal_reason')
    lookup_field = "application_guid"


class OrganizationNameListView(ListAPIView):
    """
    Simple list of organizations with only organization names
    """

    permission_classes = (IsGwellsAdmin,)
    serializer_class = OrganizationNameListSerializer
    queryset = Organization.objects.filter(expired_date__isnull=True)
    pagination_class = None
    lookup_field = 'organization_guid'
