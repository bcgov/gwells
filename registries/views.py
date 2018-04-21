from collections import OrderedDict
from django.http import HttpResponse
from django.utils import timezone
from django.views.generic import TemplateView
from django_filters import rest_framework as restfilters
from rest_framework import filters
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



class RegistriesIndexView(TemplateView):
    """
    Index page for Registries app - contains js frontend web app
    """
    template_name = 'registries/registries.html'


class CitiesListView(ListAPIView):
    """
    List of cities with a qualified, registered operator (driller or installer)

    get: returns a list of cities with a qualified, registered operator (driller or installer)
    """
    serializer_class = CityListSerializer
    lookup_field = 'person_guid'
    pagination_class = None

    # Fri 20 Apr 15:04:28 2018 GW @@SH-to-fix
    """
    queryset = Person.objects \
        .exclude(organization__city__isnull=True) \
        .exclude(organization__city='') \
        .select_related(
            'organization',
        ) \
        .distinct('organization__city') \
        .order_by('organization__city')
    """

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
