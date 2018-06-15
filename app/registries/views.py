"""
    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""

import reversion
from collections import OrderedDict
from django.db.models import Q
from django.http import HttpResponse, Http404
from django.utils import timezone
from django.views.generic import TemplateView
from django_filters import rest_framework as restfilters
from drf_yasg.utils import swagger_auto_schema
from reversion.views import RevisionMixin
from rest_framework import filters, status, exceptions
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly, AllowAny
from rest_framework.response import Response
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin
from rest_framework.views import APIView
from drf_multiple_model.views import ObjectMultipleModelAPIView
from gwells.roles import GWELLS_ROLE_GROUPS
from gwells.models.ProvinceStateCode import ProvinceStateCode
from reversion.models import Version
from registries.models import (
    AccreditedCertificateCode,
    ActivityCode,
    ApplicationStatusCode,
    ContactInfo,
    Organization,
    OrganizationNote,
    Person,
    PersonNote,
    ProofOfAgeCode,
    Register,
    RegistriesApplication,
    RegistriesRemovalReason,
    SubactivityCode,
    WellClassCode)
from registries.permissions import IsAdminOrReadOnly, GwellsPermissions
from registries.serializers import (
    ApplicationAdminSerializer,
    ApplicationStatusCodeSerializer,
    ApplicationListSerializer,
    CityListSerializer,
    ProofOfAgeCodeSerializer,
    OrganizationListSerializer,
    OrganizationAdminSerializer,
    OrganizationNameListSerializer,
    PersonAdminSerializer,
    PersonListSerializer,
    RegistrationAdminSerializer,
    RegistriesRemovalReasonSerializer,
    PersonNoteSerializer,
    ProvinceStateCodeSerializer,
    SubactivitySerializer,
    WellClassCodeSerializer,
    AccreditedCertificateCodeSerializer,
    OrganizationNoteSerializer)


class AuditCreateMixin(CreateModelMixin):
    """
    Adds create_user when instances are created.
    Create date is inserted in the model, and not required here.
    """

    def perform_create(self, serializer):
        serializer.validated_data['create_user'] = (self.request.user.profile.name or
                                                    self.request.user.get_username())
        return super().perform_create(serializer)


class AuditUpdateMixin(UpdateModelMixin):
    """
    Adds update_user when instances are updated
    Update date is inserted in the model, and not required here.
    """

    def perform_update(self, serializer):
        serializer.validated_data['update_user'] = (self.request.user.profile.name or
                                                    self.request.user.get_username())
        return super().perform_update(serializer)


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
    prov = restfilters.CharFilter(
        name="registrations__organization__province_state")
    status = restfilters.CharFilter(
        name="registrations__applications__current_status")
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


class OrganizationListView(RevisionMixin, AuditCreateMixin, ListCreateAPIView):
    """
    get:
    Returns a list of all registered drilling organizations

    post:
    Creates a new drilling organization record
    """

    permission_classes = (GwellsPermissions,)
    serializer_class = OrganizationListSerializer
    pagination_class = None

    # prefetch related objects for the queryset to prevent duplicate database trips later
    queryset = Organization.objects.all() \
        .select_related('province_state',) \
        .prefetch_related('registrations', 'registrations__person') \
        .filter(expired_date__isnull=True)

    # Allow searching against fields like organization name, address,
    # name or registration of organization contacts
    filter_backends = (filters.SearchFilter,)
    search_fields = (
        'name',
        'street_address',
        'city',
        'registrations__person__first_name',
        'registrations__person__surname',
        'registrations__applications__file_no'
    )


class OrganizationDetailView(RevisionMixin, AuditUpdateMixin, RetrieveUpdateDestroyAPIView):
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

    permission_classes = (GwellsPermissions,)

    # 'pk' and 'id' have been replaced by 'org_guid' as primary key for Organization model
    lookup_field = "org_guid"
    serializer_class = OrganizationAdminSerializer

    # prefetch related province, contacts and person records to prevent future additional database trips
    queryset = Organization.objects.all() \
        .select_related('province_state',) \
        .prefetch_related('registrations', 'registrations__person') \
        .filter(expired_date__isnull=True)

    def update(self, request, *args, **kwargs):
        reversion.set_comment("{} updated company {}".format(
            self.request.user.profile.name, self.get_object().name))
        return super(OrganizationDetailView, self).update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        Set expired_date to current date
        """

        instance = self.get_object()
        for reg in instance.registrations.all():
            if reg.person.expired_date is None:
                raise exceptions.ValidationError(
                    ('Organization has registrations associated with it. ')
                    ('Remove this organization from registration records first.'))
        instance.expired_date = timezone.now()
        instance.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


class PersonOptionsView(APIView):

    @swagger_auto_schema(auto_schema=None)
    def get(self, request, format=None):
        result = {}
        for activity in ActivityCode.objects.all():
            # Well class query
            well_class_query = WellClassCode \
                .objects.filter(
                    qualification__subactivity__registries_activity=activity.registries_activity_code) \
                .order_by('registries_well_class_code').distinct('registries_well_class_code')
            # Sub activity query
            sub_activity_query = SubactivityCode \
                .objects.filter(
                    registries_activity=activity).order_by('display_order')
            # Certificate code query
            cert_code_query = AccreditedCertificateCode \
                .objects.filter(
                    registries_activity=activity.registries_activity_code) \
                .order_by('name')

            result[activity.registries_activity_code] = {
                'well_class_codes':
                    list(map(lambda item: WellClassCodeSerializer(
                        item).data, well_class_query)),
                'subactivity_codes':
                    list(map(lambda item: SubactivitySerializer(
                        item).data, sub_activity_query)),
                'accredited_certificate_codes':
                    list(map(lambda item: AccreditedCertificateCodeSerializer(
                        item).data, cert_code_query))
            }
        result['proof_of_age_codes'] = \
            list(map(lambda item: ProofOfAgeCodeSerializer(item).data,
                     ProofOfAgeCode.objects.all().order_by('display_order')))
        result['approval_outcome_codes'] = \
            list(map(lambda item: ApplicationStatusCodeSerializer(item).data,
                     ApplicationStatusCode.objects.all()))
        result['reason_removed_codes'] = \
            list(map(lambda item: RegistriesRemovalReasonSerializer(item).data,
                     RegistriesRemovalReason.objects.all()))
        result['province_state_codes'] = \
            list(map(lambda item: ProvinceStateCodeSerializer(item).data,
                     ProvinceStateCode.objects.all().order_by('display_order')))

        return Response(result)


class PersonListView(RevisionMixin, AuditCreateMixin, ListCreateAPIView):
    """
    get:
    Returns a list of all person records

    post:
    Creates a new person record
    """

    permission_classes = (DjangoModelPermissionsOrAnonReadOnly,)
    serializer_class = PersonAdminSerializer
    pagination_class = APILimitOffsetPagination

    # Allow searching on name fields, names of related companies, etc.
    filter_backends = (restfilters.DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter)
    ordering_fields = ('surname', 'registrations__organization__name')
    ordering = ('surname',)
    search_fields = (
        'first_name',
        'surname',
        'registrations__organization__name',
        'registrations__organization__city',
        'registrations__registration_no'
    )

    # fetch related companies and registration applications (prevent duplicate database trips)
    queryset = Person.objects \
        .all() \
        .prefetch_related(
            'contact_info'
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
            qs = qs.filter(registrations__organization__city__in=cities)

        activity = self.request.query_params.get('activity', None)
        status = self.request.query_params.get('status', None)

        if activity:


<< << << < HEAD
            if status == 'P' or not status:
                # For pending, or all, we also return search where there is no registration.
                qs = qs.filter(Q(registrations__registries_activity__registries_activity_code=activity) |
                               Q(registrations__isnull=True))
            else:
                # For all other searches, we strictly filter on activity.
                qs = qs.filter(
                    registrations__registries_activity__registries_activity_code=activity)
== == == =
            qs = qs.filter(
                registrations__registries_activity__registries_activity_code=activity)
>>>>>> > improvements to orm queries
        if not self.request.user.groups.filter(name__in=GWELLS_ROLE_GROUPS).exists():
            # User is not logged in
            # Only show active drillers to non-admin users and public
            qs = qs.filter(
                Q(registrations__applications__current_status__code='A'),
                Q(registrations__applications__removal_date__isnull=True))
        else:
            # User is logged in
            if status:
                if status == 'Removed':
                    # Things are a bit more complicated if we're looking for removed, as the current
                    # status doesn't come in to play.
                    qs = qs.filter(
                        registrations__applications__removal_date__isnull=False)
                else:
                    if status == 'P':
                        # If the status is pending, we also pull in any people without registrations
                        # or applications.
                        qs = qs.filter(Q(registrations__applications__current_status__code=status) |
                                       Q(registrations__isnull=True) |
                                       Q(registrations__applications__isnull=True),
                                       Q(registrations__applications__removal_date__isnull=True))
                    else:
                        qs = qs.filter(
                            Q(registrations__applications__current_status__code=status),
                            Q(registrations__applications__removal_date__isnull=True))
        return qs

    @swagger_auto_schema(responses={200: PersonListSerializer(many=True)})
    def get(self, request, *args, **kwargs):
        """ Returns self.list - decorated for schema documentation """
        return super(PersonListView, self).list(request, *args, **kwargs)

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


class PersonDetailView(RevisionMixin, AuditUpdateMixin, RetrieveUpdateDestroyAPIView):
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

    permission_classes = (GwellsPermissions,)
    serializer_class = PersonAdminSerializer

    # pk field has been replaced by person_guid
    lookup_field = "person_guid"

    queryset = Person.objects \
        .all() \
        .prefetch_related(
            'notes',
            'notes__author',
            'contact_info',
            'registrations',
            'registrations__registries_activity',
            'registrations__organization',
            'registrations__status',
            'registrations__applications',
            'registrations__applications__current_status',
            'registrations__applications__primary_certificate',
            'registrations__applications__primary_certificate__cert_auth',
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
        if not self.request.user.groups.filter(name__in=GWELLS_ROLE_GROUPS).exists():
            qs = qs.filter(registrations__status='ACTIVE')
        return qs

    def destroy(self, request, *args, **kwargs):
        """
        Set expired_date to current date
        """

        instance = self.get_object()
        instance.expired_date = timezone.now()
        instance.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


class CitiesListView(ListAPIView):
    """
    List of cities with a qualified, registered operator (driller or installer)

    get: returns a list of cities with a qualified, registered operator (driller or installer)
    """
    serializer_class = CityListSerializer
    lookup_field = 'register_guid'
    pagination_class = None
    permission_classes = (AllowAny,)
    queryset = Register.objects \
        .exclude(organization__city__isnull=True) \
        .exclude(organization__city='') \
        .select_related(
            'organization', 'organization__province_state'
        ) \
        .distinct('organization__city') \
        .order_by('organization__city')

    def get_queryset(self):
        """
        Returns only registered operators (i.e. drillers with active registration) to anonymous users
        if request has a kwarg 'activity' (accepts values 'drill' and 'install'), queryset
        will filter for that activity
        """
        qs = self.queryset
        if not self.request.user.groups.filter(name__in=GWELLS_ROLE_GROUPS).exists():
            qs = qs.filter(status='ACTIVE')
        if self.kwargs['activity'] == 'drill':
            qs = qs.filter(registries_activity='DRILL')
        if self.kwargs['activity'] == 'install':
            qs = qs.filter(registries_activity='PUMP')
        return qs


class RegistrationListView(RevisionMixin, AuditCreateMixin, ListCreateAPIView):
    """
    get:
    List all registration records

    post:
    Create a new well driller or well pump installer registration record for a person
    """

    permission_classes = (GwellsPermissions,)
    serializer_class = RegistrationAdminSerializer
    queryset = Register.objects.all() \
        .select_related(
            'person',
            'registries_activity',
            'status',
            'organization',
            'register_removal_reason',) \
        .prefetch_related(
            'applications',
            'applications__current_status',
            'applications__primary_certificate',
            'applications__primary_certificate__cert_auth',
            'applications__subactivity',
            'applications__subactivity__qualification_set',
            'applications__subactivity__qualification_set__well_class'
    )


class RegistrationDetailView(RevisionMixin, AuditUpdateMixin, RetrieveUpdateDestroyAPIView):
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

    permission_classes = (GwellsPermissions,)
    serializer_class = RegistrationAdminSerializer
    lookup_field = 'register_guid'
    queryset = Register.objects.all() \
        .select_related(
            'person',
            'registries_activity',
            'status',
            'organization',
            'register_removal_reason',) \
        .prefetch_related(
            'applications',
            'applications__current_status',
            'applications__primary_certificate',
            'applications__primary_certificate__cert_auth',
            'applications__subactivity',
            'applications__subactivity__qualification_set',
            'applications__subactivity__qualification_set__well_class'
    )


class ApplicationListView(RevisionMixin, AuditCreateMixin, ListCreateAPIView):
    """
    get:
    Returns a list of all registration applications

    post:
    Creates a new registries application
    """

    permission_classes = (GwellsPermissions,)
    serializer_class = ApplicationAdminSerializer
    queryset = RegistriesApplication.objects.all() \
        .select_related(
            'registration',
            'registration__person',
            'registration__registries_activity',
            'registration__status',
            'registration__register_removal_reason')


class ApplicationDetailView(RevisionMixin, AuditUpdateMixin, RetrieveUpdateDestroyAPIView):
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

    permission_classes = (GwellsPermissions,)
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

    permission_classes = (GwellsPermissions,)
    serializer_class = OrganizationNameListSerializer
    queryset = Organization.objects \
        .filter(expired_date__isnull=True) \
        .select_related('province_state')
    pagination_class = None
    lookup_field = 'organization_guid'


class PersonNoteListView(AuditCreateMixin, ListCreateAPIView):
    """
    get:
    Returns notes associated with a Person record

    post:
    Adds a note record to the specified Person record
    """

    permission_classes = (GwellsPermissions,)
    serializer_class = PersonNoteSerializer
    swagger_schema = None

    def get_queryset(self):
        person = self.kwargs['person_guid']
        return PersonNote.objects.filter(person=person).order_by('-date')

    def perform_create(self, serializer):
        """ Add author to serializer data """
        person = self.kwargs['person_guid']
        serializer.validated_data['person'] = Person.objects.get(
            person_guid=person)
        serializer.validated_data['author'] = self.request.user
        return super(PersonNoteListView, self).perform_create(serializer)


class PersonNoteDetailView(AuditUpdateMixin, RetrieveUpdateDestroyAPIView):
    """
    get:
    Returns a PersonNote record

    put:
    Replaces a PersonNote record with a new one

    patch:
    Updates a PersonNote record with the set of fields provided in the request body

    delete:
    Removes a PersonNote record
    """

    permission_classes = (GwellsPermissions,)
    serializer_class = PersonNoteSerializer
    swagger_schema = None

    def get_queryset(self):
        person = self.kwargs['person']
        return PersonNote.objects.filter(person=person)


class OrganizationNoteListView(AuditCreateMixin, ListCreateAPIView):
    """
    get:
    Returns notes associated with a Organization record

    post:
    Adds a note record to the specified Organization record
    """

    permission_classes = (GwellsPermissions,)
    serializer_class = OrganizationNoteSerializer
    swagger_schema = None

    def get_queryset(self):
        org = self.kwargs['org_guid']
        return OrganizationNote.objects.filter(organization=org).order_by('-date')

    def perform_create(self, serializer):
        """ Add author to serializer data """
        org = self.kwargs['org_guid']
        serializer.validated_data['organization'] = Organization.objects.get(
            org_guid=org)
        serializer.validated_data['author'] = self.request.user
        return super(OrganizationNoteListView, self).perform_create(serializer)


class OrganizationNoteDetailView(AuditUpdateMixin, RetrieveUpdateDestroyAPIView):
    """
    get:
    Returns a OrganizationNote record

    put:
    Replaces a OrganizationNote record with a new one

    patch:
    Updates a OrganizationNote record with the set of fields provided in the request body

    delete:
    Removes a OrganizationNote record
    """

    permission_classes = (GwellsPermissions,)
    serializer_class = OrganizationNoteSerializer
    swagger_schema = None

    def get_queryset(self):
        org = self.kwargs['org_guid']
        return OrganizationNote.objects.filter(organization=org)


class OrganizationHistory(APIView):
    """
    get: returns a history of changes to an Organization model record
    """

    permission_classes = (GwellsPermissions,)
    queryset = Organization.objects.all()
    swagger_schema = None

    def get(self, request, org_guid):
        org_guid = self.kwargs['org_guid']
        try:
            organization = Organization.objects.get(org_guid=org_guid)
        except Organization.DoesNotExist:
            raise Http404("Organization not found")

        # query records in history for this model.
        history = [obj.field_dict for obj in organization.history.all().order_by(
            '-revision__date_created')]

        history_diff = []

        for i in range(len(history)):
            changed = False
            cur = history[i]
            prev = None

            if i < (len(history) - 1):
                prev = history[i+1]

            item = {
                "diff": {},
                "prev": {},
                "user": cur['update_user'] or cur['create_user'],
                "date": cur['update_date'] or cur['create_date']
            }
            if prev is None:
                item['created'] = True
                history_diff.append(item)

            else:
                for key, value in prev.items():
                    # loop through the previous record and add changed fields to the 'diff' dict
                    # leave out update/create stamps
                    if (cur[key] != value and
                            key != "update_date" and
                            key != "update_user" and
                            key != "create_date" and
                            key != "create_user"):
                        item['diff'][key] = cur[key]
                        item['prev'][key] = value
                        changed = True
                if changed:
                    history_diff.append(item)

        return Response(history_diff)


class PersonHistory(APIView):
    """
    get: returns a history of changes to a Person model record
    """

    permission_classes = (GwellsPermissions,)
    queryset = Person.objects.all()
    swagger_schema = None

    def get(self, request, person_guid):
        """
        Retrieves version history for the specified Person record and creates a list of diffs
        for each revision.
        """

        person_guid = self.kwargs['person_guid']
        try:
            person = Person.objects.get(person_guid=person_guid)
        except Person.DoesNotExist:
            raise Http404("Person not found")

        # query records in history for this model.
        history = [obj.field_dict for obj in person.history.all().order_by(
            '-revision__date_created')]

        history_diff = []

        for i in range(len(history)):
            changed = False
            cur = history[i]
            prev = None

            if i < (len(history) - 1):
                prev = history[i+1]

            item = {
                "diff": {},
                "prev": {},
                "user": cur['update_user'] or cur['create_user'],
                "date": cur['update_date'] or cur['create_date']
            }
            if prev is None:
                item['created'] = True
                history_diff.append(item)

            else:
                for key, value in prev.items():
                    # loop through the previous record and add changed fields to the 'diff' dict
                    # leave out update/create stamps
                    if (cur[key] != value and
                            key != "update_date" and
                            key != "update_user" and
                            key != "create_date" and
                            key != "create_user"):
                        item['diff'][key] = cur[key]
                        item['prev'][key] = value
                        changed = True
                if changed:
                    history_diff.append(item)

        return Response(history_diff)
