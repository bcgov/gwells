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
import re, json
from collections import OrderedDict
from django.db.models import Q, Prefetch, Count
from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.forms.models import model_to_dict
from django.views.generic import TemplateView
from django.contrib.gis.geos import Polygon, GEOSException
from django_filters import rest_framework as restfilters
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from reversion.views import RevisionMixin
from rest_framework import filters, status, exceptions
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_multiple_model.views import ObjectMultipleModelAPIView

from gwells.documents import MinioClient
from gwells.roles import REGISTRIES_VIEWER_ROLE
from gwells.models import ProvinceStateCode
from gwells.pagination import APILimitOffsetPagination
from gwells.roles import REGISTRIES_EDIT_ROLE, REGISTRIES_VIEWER_ROLE
from gwells.settings.base import get_env_variable
from reversion.models import Version
from registries.models import (
    AccreditedCertificateCode,
    ActivityCode,
    ApplicationStatusCode,
    Organization,
    OrganizationNote,
    Person,
    PersonNote,
    ProofOfAgeCode,
    Register,
    RegistriesApplication,
    RegistriesRemovalReason,
    SubactivityCode,
    WellClassCode,
    RegionalArea)
from registries.permissions import RegistriesEditPermissions, RegistriesEditOrReadOnly
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
    OrganizationNoteSerializer,
    PersonNameSerializer,
    RegionalAreaSerializer)
from gwells.change_history import generate_history_diff
from gwells.views import AuditCreateMixin, AuditUpdateMixin

class OrganizationListView(RevisionMixin, AuditCreateMixin, ListCreateAPIView):
    """
    get:
    Returns a list of all registered drilling organizations.

    post:
    Creates a new drilling organization record.
    """

    permission_classes = (RegistriesEditPermissions,)
    serializer_class = OrganizationListSerializer
    pagination_class = None

    # prefetch related objects for the queryset to prevent duplicate database trips later
    queryset = Organization.objects.all() \
        .select_related('province_state',) \
        .prefetch_related('registrations', 'registrations__person')

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

    def get_queryset(self):
        return self.queryset.filter(expiry_date__gt=timezone.now())


class OrganizationDetailView(RevisionMixin, AuditUpdateMixin, RetrieveUpdateDestroyAPIView):
    """
    get:
    Returns the specified drilling organization.

    put:
    Replaces the specified record with a new one.

    patch:
    Updates a drilling organization with the fields/values provided in the request body.

    delete:
    Removes the specified drilling organization record.
    """

    permission_classes = (RegistriesEditPermissions,)

    # 'pk' and 'id' have been replaced by 'org_guid' as primary key for Organization model
    lookup_field = "org_guid"
    serializer_class = OrganizationAdminSerializer

    # prefetch related province, contacts and person records to prevent future additional database trips
    queryset = Organization.objects.all() \
        .select_related('province_state',) \
        .prefetch_related('registrations', 'registrations__person')

    def get_queryset(self):
        return self.queryset.filter(expiry_date__gt=timezone.now())

    def destroy(self, request, *args, **kwargs):
        """
        Set expiry_date to current date
        """

        instance = self.get_object()
        for reg in instance.registrations.all():
            if reg.person.expiry_date is None:
                raise exceptions.ValidationError(
                    ('Organization has registrations associated with it. ')
                    ('Remove this organization from registration records first.'))
        instance.expiry_date = timezone.now()
        instance.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


class PersonOptionsView(APIView):
    
    def filterRegionalAreas(self, result):
        """
        Modify substrings shown in the registries search to move 'Regional District of' to the back
        The search uses a uuid and not the name key, so this operation is safe
        Args:
            result (List): List of regions from the serializer
        """
        substring = '^Regional Districts? of'
        for item in result:
            match = re.match(substring, item['name'])
            if match:
                district = match.group(0)
                item['name'] = item['name'].replace(match.group(0) + " ", "") + ", " + district
        result.sort(key=lambda item: item['name'])
        
    @swagger_auto_schema(auto_schema=None)
    def get(self, request, format=None, **kwargs):
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
        result['regional_areas'] = \
            list(map(lambda item: RegionalAreaSerializer(item).data,
                     RegionalArea.objects.all().order_by('name')))
        self.filterRegionalAreas(result['regional_areas'])
        
        return Response(result)



def person_search_qs(request):
    """ 
    Returns Person queryset, removing non-active and unregistered 
    drillers for anonymous users 
    Implementation note: The returned queryset is actually three related 
    querysets.  The first is the primary query set and is is a join 
    across several tables.  The other two querysets are 
    used to pre-fetch collections of related information (registrations 
    and applications).  
    Various filters can be requested (filter by 'activity', 'subactivity', 
    'geographic area', etc). In general, when a filter is needed, it is applied
    to each of the three querysets (or sometimes only two of them). 
    """
    query = request.GET
    qs = Person.objects.filter(expiry_date__gt=timezone.now())

    # base registration and application querysets
    registrations_qs = Register.objects.all()
    applications_qs = RegistriesApplication.objects.all()

    person_filters = Q()
    reg_filters = Q()
    appl_filters = Q()


    # Search for cities (split list and return all matches)
    # search comes in as a comma-separated querystring param e.g: ?city=Atlin,Lake Windermere,Duncan
    cities = query.get('city', None)
    if cities:
        cities = cities.split(',')
        person_filters = person_filters & Q(registrations__organization__city__in=cities)
        reg_filters = reg_filters & Q(organization__city__in=cities)
    
    # regional areas
    region_guids = query.get('region', None)
    if region_guids:
        region_guids = region_guids.split(',')
        regional_areas = RegionalArea.objects.filter(regional_area_guid__in=region_guids)
        person_filters &= Q(registrations__organization__regional_areas__in=regional_areas)
        reg_filters &= Q(organization__regional_areas__in=regional_areas)

    #bbox
    sw_long = query.get('sw_long')
    sw_lat = query.get('sw_lat')
    ne_long = query.get('ne_long')
    ne_lat = query.get('ne_lat')
    if sw_long and sw_lat and ne_long and ne_lat:
        try:
            bbox = Polygon.from_bbox((sw_long, sw_lat, ne_long, ne_lat))
            bbox.srid = 4326
            person_filters = person_filters & Q(registrations__organization__geom__bboverlaps=bbox)
            reg_filters = reg_filters & Q(organization__geom__bboverlaps=bbox)
        except (ValueError, GEOSException):
            pass

    #Subactivities param comes as a csv list
    subactivities = query.get('subactivities')
    if subactivities is not None:      
      subactivities = subactivities.split(",")
      person_filters = person_filters & \
            Q(registrations__applications__subactivity__registries_subactivity_code__in=subactivities)
      reg_filters = reg_filters & \
          Q(applications__subactivity__registries_subactivity_code__in=subactivities)
      appl_filters = appl_filters & \
          Q(subactivity__registries_subactivity_code__in=subactivities)

    activity = query.get('activity', None)
    status = query.get('status', None)
    user_is_staff = request.user.groups.filter(name=REGISTRIES_VIEWER_ROLE).exists()

    if activity:
        if (status == 'P' or not status) and user_is_staff:
            # We only allow staff to filter on status
            # For pending, or all, we also return search where there is no registration.
            person_filters = person_filters & \
                (
                    Q(registrations__registries_activity__registries_activity_code=activity) |
                    Q(registrations__isnull=True)
                )
            reg_filters = reg_filters & \
                Q(registries_activity__registries_activity_code=activity)
        else:
            # For all other searches, we strictly filter on activity.
            person_filters = person_filters & \
                Q(registrations__registries_activity__registries_activity_code=activity)
            reg_filters = reg_filters & \
                Q(registries_activity__registries_activity_code=activity)

    if user_is_staff:
        # User is logged in
        if status:
            if status == 'Removed':
                # Things are a bit more complicated if we're looking for removed, as the current
                # status doesn't come in to play.
                person_filters = person_filters & \
                    Q(registrations__applications__removal_date__isnull=False)
                reg_filters = reg_filters & \
                    Q(applications__removal_date__isnull=False)
                appl_filters = appl_filters & \
                    Q(removal_date__isnull=False)
            else:
                if status == 'P':
                    # If the status is pending, we also pull in any people without registrations
                    # or applications.
                    person_filters = person_filters & \
                        (
                            Q(registrations__applications__current_status__code=status) |
                            Q(registrations__isnull=True) |
                            Q(registrations__applications__isnull=True)                            
                        ) & \
                        Q(registrations__applications__removal_date__isnull=True)
                    reg_filters = reg_filters & \
                        (
                            Q(applications__current_status__code=status) |                                    
                            Q(applications__isnull=True)                            
                        ) & \
                        Q(applications__removal_date__isnull=True)   
                    appl_filters = appl_filters & \
                        (
                            Q(current_status__code=status)                                     
                            #Q(isnull=True)                            
                        ) & \
                        Q(removal_date__isnull=True)                      
                else:
                    person_filters = person_filters & \
                        (
                            Q(registrations__applications__current_status__code=status) &
                            Q(registrations__applications__removal_date__isnull=True)
                        )
                    reg_filters = reg_filters & \
                        (
                            Q(applications__current_status__code=status) &
                            Q(applications__removal_date__isnull=True)
                        )
                    appl_filters = appl_filters & \
                        (
                            Q(current_status__code=status) &
                            Q(removal_date__isnull=True)
                        )
    else:
        # User is not logged in
        # Only show active drillers to non-admin users and public
        person_filters = person_filters & \
            (
              Q(registrations__applications__current_status__code='A') &
              Q(registrations__applications__removal_date__isnull=True)
            )

        reg_filters = reg_filters & \
            (
                Q(applications__current_status__code='A') &
                Q(applications__removal_date__isnull=True)
            )
        appl_filters= appl_filters & \
            (
                Q(current_status='A') & 
                Q(removal_date__isnull=True)
            )

    #apply all the "main" and "registration" filters that were chosen above
    qs = qs.filter(person_filters)
    registrations_qs = registrations_qs.filter(reg_filters)
    applications_qs = applications_qs.filter(appl_filters)


    # generate applications queryset
    applications_qs = applications_qs \
        .select_related(
            'current_status',
            'primary_certificate',
            'primary_certificate__cert_auth',
            'subactivity',
        ) \
        .prefetch_related(
            'subactivity__qualification_set',
            'subactivity__qualification_set__well_class'
        ).distinct()    

    # generate registrations queryset, inserting filtered applications queryset defined above
    registrations_qs = registrations_qs \
        .select_related(
            'registries_activity',
            'organization',
            'organization__province_state',
        ) \
        .prefetch_related(
            Prefetch('applications', queryset=applications_qs)
        ).distinct()            

    # insert filtered registrations set
    qs = qs \
        .prefetch_related(
            Prefetch('registrations', queryset=registrations_qs)
        )

    return qs.distinct()

def exclude_persons_without_registrations(request, filtered_queryset, statuses_that_disallow_empty_registrations=['A']):
    """
    In the following cases perform additional filtering on the 'filtered_queryset'
    to remove persons that have no registrations:
    1. when the request asked for status of *Registered* ('A')
    2. when the request asked to filter by bounding box (geographic area)
    3. when the request asked to filter by city
    Implementation note: Ideally we would rely on the queryset for this
    filtering, but the queryset is very complex, and it relies on
    multiple 'prefetches' (extra database queries).  It is most efficient to handle 
    this filtering post database query.    
    Returns an updated filtered_queryset
    """
    status_disallows_people_with_no_registrations = \
        request.GET.get('status') in statuses_that_disallow_empty_registrations 
    is_filtered_by_bbox = request.GET.get('sw_long') != None \
        and request.GET.get('sw_lat') != None \
        and request.GET.get('ne_long') != None\
        and request.GET.get('ne_lat') != None
    is_filtered_by_city = request.GET.get('city', "") != ""
    if is_filtered_by_bbox or is_filtered_by_city or \
        status_disallows_people_with_no_registrations:
        filtered_queryset = [f for f in filtered_queryset if len(f.registrations.all()) > 0]
    return filtered_queryset

class PersonListView(RevisionMixin, AuditCreateMixin, ListCreateAPIView):
    """
    get:
    Returns a list of all person records.

    post:
    Creates a new person record.
    """

    permission_classes = (RegistriesEditOrReadOnly,)
    serializer_class = PersonAdminSerializer
    pagination_class = APILimitOffsetPagination
    # Allow searching on name fields, names of related companies, etc.
    filter_backends = (restfilters.DjangoFilterBackend,
                       filters.SearchFilter, 
                       filters.OrderingFilter
                       )

                       
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
    queryset = Person.objects.all()

    def get_queryset(self):
        """ Returns Person queryset, removing non-active and unregistered drillers for anonymous users """

        return person_search_qs(self.request)

    @swagger_auto_schema(responses={200: PersonListSerializer(many=True)})
    def get(self, request, *args, **kwargs):
        # Returns self.list - overridden for schema documentation
        return self.list(request, *args, **kwargs)

    def list(self, request, **kwargs):
        """ List response using serializer with reduced number of fields """
        queryset = self.get_queryset()
        filtered_queryset = self.filter_queryset(queryset)
        filtered_queryset = exclude_persons_without_registrations(request, filtered_queryset) 

        page = self.paginate_queryset(filtered_queryset)
        if page is not None:
            serializer = PersonListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = PersonListSerializer(filtered_queryset, many=True)
        return Response(serializer.data)


class PersonDetailView(RevisionMixin, AuditUpdateMixin, RetrieveUpdateDestroyAPIView):
    """
    get:
    Returns the specified person.

    put:
    Replaces the specified person record with a new one.

    patch:
    Updates a person with the fields/values provided in the request body.

    delete:
    Removes the specified person record.
    """

    permission_classes = (RegistriesEditPermissions,)
    serializer_class = PersonAdminSerializer

    # pk field has been replaced by person_guid
    lookup_field = "person_guid"

    queryset = Person.objects \
        .all() \
        .prefetch_related(
            'notes',
            'notes__author',
            'registrations',
            'registrations__registries_activity',
            'registrations__organization',
            'registrations__applications',
            'registrations__applications__current_status',
            'registrations__applications__primary_certificate',
            'registrations__applications__primary_certificate__cert_auth',
            'registrations__applications__subactivity',
            'registrations__applications__subactivity__qualification_set',
            'registrations__applications__subactivity__qualification_set__well_class'
        ).distinct()

    def get_queryset(self):
        """
        Returns only registered people (i.e. drillers with active registration) to anonymous users
        """
        qs = self.queryset.filter(expiry_date__gt=timezone.now())
        if not self.request.user.groups.filter(name=REGISTRIES_VIEWER_ROLE).exists():
            qs = qs.filter(Q(applications__current_status__code='A'),
                           Q(applications__removal_date__isnull=True))
        return qs

    def destroy(self, request, *args, **kwargs):
        """
        Set expiry_date to current date
        """

        instance = self.get_object()
        instance.expiry_date = timezone.now()
        instance.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


class CitiesListView(ListAPIView):
    """
    List of cities with a qualified, registered operator (driller or installer).

    get:
    Returns a list of cities with a qualified, registered operator (driller or installer).
    """
    serializer_class = CityListSerializer
    lookup_field = 'register_guid'
    pagination_class = None
    permission_classes = (RegistriesEditOrReadOnly,)
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
        if not self.request.user.groups.filter(name=REGISTRIES_VIEWER_ROLE).exists():
            qs = qs.filter(
                Q(applications__current_status__code='A'),
                Q(applications__removal_date__isnull=True))
        if self.kwargs.get('activity') == 'drill':
            qs = qs.filter(registries_activity='DRILL')
        if self.kwargs.get('activity') == 'install':
            qs = qs.filter(registries_activity='PUMP')
        return qs


class RegistrationListView(RevisionMixin, AuditCreateMixin, ListCreateAPIView):
    """
    get:
    List all registration records.

    post:
    Create a new well driller or well pump installer registration record for a person.
    """

    permission_classes = (RegistriesEditPermissions,)
    serializer_class = RegistrationAdminSerializer
    queryset = Register.objects.all() \
        .select_related(
            'person',
            'registries_activity',
            'organization',) \
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
    Returns a well driller or well pump installer registration record.

    put:
    Replaces a well driller or well pump installer registration record with a new one.

    patch:
    Updates a registration record with new values.

    delete:
    Removes the specified registration record from the database.
    """

    permission_classes = (RegistriesEditPermissions,)
    serializer_class = RegistrationAdminSerializer
    lookup_field = 'register_guid'
    queryset = Register.objects.all() \
        .select_related(
            'person',
            'registries_activity',
            'organization',) \
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
    Returns a list of all registration applications.

    post:
    Creates a new registries application.
    """

    permission_classes = (RegistriesEditPermissions,)
    serializer_class = ApplicationAdminSerializer
    queryset = RegistriesApplication.objects.all() \
        .select_related(
            'registration',
            'registration__person',
            'registration__registries_activity')


class ApplicationDetailView(RevisionMixin, AuditUpdateMixin, RetrieveUpdateDestroyAPIView):
    """
    get:
    Returns the specified drilling application.

    put:
    Replaces the specified record with a new one.

    patch:
    Updates a drilling application with the set of values provided in the request body.

    delete:
    Removes the specified drilling application record.
    """

    permission_classes = (RegistriesEditPermissions,)
    serializer_class = ApplicationAdminSerializer
    queryset = RegistriesApplication.objects.all() \
        .select_related(
            'registration',
            'registration__person',
            'registration__registries_activity')
    lookup_field = "application_guid"


class OrganizationNameListView(ListAPIView):
    """
    A list of organizations with only organization names.
    """
    permission_classes = (RegistriesEditOrReadOnly,)
    serializer_class = OrganizationNameListSerializer
    queryset = Organization.objects \
        .select_related('province_state')
    pagination_class = None
    lookup_field = 'organization_guid'

    def get_queryset(self):
        return self.queryset.filter(expiry_date__gt=timezone.now())


class PersonNoteListView(AuditCreateMixin, ListCreateAPIView):
    """
    get:
    Returns notes associated with a Person record.

    post:
    Adds a note record to the specified Person record.
    """

    permission_classes = (RegistriesEditPermissions,)
    serializer_class = PersonNoteSerializer

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
    Returns a PersonNote record.

    put:
    Replaces a PersonNote record with a new one.

    patch:
    Updates a PersonNote record with the set of fields provided in the request body.

    delete:
    Removes a PersonNote record.
    """

    permission_classes = (RegistriesEditPermissions,)
    serializer_class = PersonNoteSerializer
    queryset = PersonNote.objects.all()
    lookup_field = 'person_note_guid'
    lookup_url_kwarg = 'note_guid'

def canDelete(self, author):
    """Checks if user has permission to change Notes.
        Notes can only be edited by Admins and the note's creator
    """
    return self.request.user.groups.filter(name="gwells_admin").exists() or \
        self.request.user.groups.filter(name="admin").exists() or \
        author == self.request.user

def get_persons_note(self, person_guid, note_guid):
    """Fetches the note requested"""
    if self.queryset.filter(person_note_guid=note_guid, person=person_guid).exists():
        return self.queryset.get(person_note_guid=note_guid, person=person_guid)
    return None

def get(self, request, person_guid, note_guid, **kwargs):
    note = self.get_persons_note(person_guid, note_guid)
    if note:
        return Response(model_to_dict(note))
    return HttpResponse(status=404)

def delete(self, request, person_guid, note_guid, **kwargs):
    """Handles deletion for Persons Notes."""
    note = self.get_persons_note(person_guid, note_guid)
    if note:
        if self.canDelete(note.author):
            note.delete()
            return HttpResponse(status=204)
        return HttpResponse(status=401)
    return HttpResponse(status=404)

def patch(self, request, person_guid, note_guid, **kwargs):
    """Updates a Note with new content information.
        Notes can only be updated by the user who created them
    """
    note = self.get_persons_note(person_guid, note_guid)
    new_note_content = json.loads(request.body.decode('utf-8')).get("note", None)
    if note:
        if note.author == self.request.user:
            if new_note_content:
                note.note = new_note_content
                note.save()
                return HttpResponse(status=200)
            return HttpResponse(status=400)
        return HttpResponse(status=403)
    return HttpResponse(status=404)


class OrganizationNoteListView(AuditCreateMixin, ListCreateAPIView):
    """
    get:
    Returns notes associated with a Organization record.

    post:
    Adds a note record to the specified Organization record.
    """

    permission_classes = (RegistriesEditPermissions,)
    serializer_class = OrganizationNoteSerializer

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
    Returns a OrganizationNote record.

    patch:
    Updates a OrganizationNote record with the set of fields provided in the request body.

    delete:
    Removes a OrganizationNote record.
    """

    permission_classes = (RegistriesEditPermissions,)
    serializer_class = OrganizationNoteSerializer

    def canDelete(self, author):
        """Checks if user has permission to change Notes.
           Notes can only be edited by Admins and the note's creator
        """
        return self.request.user.groups.filter(name="gwells_admin").exists() or \
            self.request.user.groups.filter(name="admin").exists() or \
            author == self.request.user
    
    def get_organization_note(self, org_guid, note_guid):
        """Fetches the note requested"""
        if OrganizationNote.objects.filter(org_note_guid=note_guid, organization=org_guid).exists():
            return OrganizationNote.objects.get(org_note_guid=note_guid, organization=org_guid)
        return None
    
    def get(self, request, org_guid, note_guid, **kwargs):
        note = self.get_organization_note(org_guid, note_guid)
        if note:
            return Response(model_to_dict(note))
        return HttpResponse(status=404)
    
    def delete(self, request, org_guid, note_guid, **kwargs):
        """Handles deletion for Organization Notes."""
        note = self.get_organization_note(org_guid, note_guid)
        if note:
            if self.canDelete(note.author):
                note.delete()
                return HttpResponse(status=204)
            return HttpResponse(status=401)
        return HttpResponse(status=404)
    
    def patch(self, request, org_guid, note_guid, **kwargs):
        """Updates a Note with new content information.
           Notes can only be updated by the user who created them
        """
        note = self.get_organization_note(org_guid, note_guid)
        new_note_content = json.loads(request.body.decode('utf-8')).get("note", None)
        if note:
            if note.author == self.request.user:
                if new_note_content:
                    note.note = new_note_content
                    note.save()
                    return HttpResponse(status=200)
                return HttpResponse(status=400)
            return HttpResponse(status=403)
        return HttpResponse(status=404)

class OrganizationHistory(APIView):
    """
    get:
    Returns a history of changes to an Organization model record.
    """

    permission_classes = (RegistriesEditPermissions,)
    queryset = Organization.objects.all()

    def get(self, request, org_guid, **kwargs):
        try:
            organization = Organization.objects.get(org_guid=org_guid)
        except Organization.DoesNotExist:
            raise Http404("Organization not found")

        # query records in history for this model.
        organization_history = [obj for obj in organization.history.all().order_by(
            '-revision__date_created')]

        history_diff = generate_history_diff(organization_history)

        return Response(history_diff)


class PersonHistory(APIView):
    """
    get:
    Returns a history of changes to a Person model record.
    """

    permission_classes = (RegistriesEditPermissions,)
    queryset = Person.objects.all()

    def get(self, request, person_guid, **kwargs):
        """
        get:
        Retrieves version history for the specified Person record and creates a list of diffs for each revision.
        """

        try:
            person = Person.objects.get(person_guid=person_guid)
        except Person.DoesNotExist:
            raise Http404("Person not found")

        # query records in history for this model.
        person_history = [obj for obj in person.history.all().order_by(
            '-revision__date_created')]

        person_history_diff = generate_history_diff(
            person_history, 'Person profile')

        registration_history = []
        registration_history_diff = []

        application_history = []
        application_history_diff = []

        # generate diffs for version history in each of the individual's registrations
        for reg in person.registrations.all():
            registration_history = [
                obj for obj in reg.history.all()]
            registration_history_diff += generate_history_diff(
                registration_history, reg.registries_activity.description + ' registration')

            for app in reg.applications.all():
                application_history = [
                    obj for obj in app.history.all()]
                application_history_diff += generate_history_diff(
                    application_history, app.subactivity.description + ' application')

        # generate application diffs

        history_diff = sorted(
            person_history_diff +
            registration_history_diff +
            application_history_diff, key=lambda x: x['date'], reverse=True)

        return Response(history_diff)


class PersonNameSearch(ListAPIView):
    """Search for a person in the Register."""

    permission_classes = (RegistriesEditOrReadOnly,)
    serializer_class = PersonNameSerializer
    pagination_class = None
    lookup_field = 'person_guid'

    ordering = ('surname',)

    def get_queryset(self):
        """
        This view returns all names with expired records filtered out.
        """
        return Person.objects.filter(expiry_date__gt=timezone.now())

class ListFiles(APIView):
    """
    List documents associated with a person in the Registry.

    get:
    Returns list of files found for the person identified in the URI.
    """


    def get(self, request, person_guid, **kwargs):
        user_is_staff = self.request.user.groups.filter(
            Q(name=REGISTRIES_EDIT_ROLE) | Q(name=REGISTRIES_VIEWER_ROLE)).exists()

        client = MinioClient(
            request=request, disable_private=(not user_is_staff))

        documents = client.get_documents(
            person_guid, resource="driller", include_private=user_is_staff)

        return Response(documents)


class PreSignedDocumentKey(APIView):
    """
    Get a pre-signed document key to upload into an S3 compatible document store

    post:
    Obtain a URL that is pre-signed to allow client-side uploads.
    """

    queryset = Person.objects.all()
    permission_classes = (RegistriesEditPermissions,)

    def get(self, request, person_guid, **kwargs):
        person = get_object_or_404(self.queryset, pk=person_guid)
        client = MinioClient(
            request=request, disable_private=False)

        object_name = request.GET.get("filename")
        filename = client.format_object_name(object_name, person.person_guid, "driller")
        bucket_name = get_env_variable("S3_REGISTRANT_BUCKET")

        # All documents are private for drillers
        url = client.get_presigned_put_url(
            filename, bucket_name=bucket_name, private=True)

        return JsonResponse({"object_name": object_name, "url": url})


class DeleteDrillerDocument(APIView):
    """
    Delete a document from a S3 compatible store.

    delete:
    Remove the specified object from the S3 store.
    """

    queryset = Person.objects.all()
    permission_classes = (RegistriesEditPermissions,)

    def delete(self, request, person_guid, **kwargs):
        person = get_object_or_404(self.queryset, pk=person_guid)
        client = MinioClient(
            request=request, disable_private=False)

        is_private = False
        bucket_name = get_env_variable("S3_REGISTRANT_BUCKET")

        if request.GET.get("private") == "true":
            is_private = True
            bucket_name = get_env_variable("S3_PRIVATE_REGISTRANT_BUCKET")

        object_name = request.GET.get("filename")
        client.delete_document(object_name, bucket_name=bucket_name, private=is_private)

        return HttpResponse(status=204)
