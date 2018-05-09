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
import logging
from django.utils import timezone
from django.db import transaction
import logging
from rest_framework import serializers
from registries.models import (
    Organization,
    ContactInfo,
    Person,
    Register,
    RegistriesApplication,
    RegistriesApplicationStatus,
    RegistriesStatusCode,
    ActivityCode,
    SubactivityCode,
    Qualification,
    ApplicationStatusCode,
    PersonNote
)

logger = logging.getLogger(__name__)


class AuditModelSerializer(serializers.ModelSerializer):
    """
    Serializes AuditModel fields.
    Can be inherited into serializers for models that inherit from AuditModel
    """
    create_user = serializers.ReadOnlyField()
    create_date = serializers.ReadOnlyField()
    update_user = serializers.ReadOnlyField()
    update_date = serializers.ReadOnlyField()


class PersonNoteSerializer(serializers.ModelSerializer):
    """
    Serializes PersonNote records
    """

    author = serializers.ReadOnlyField(source='author.profile.name')
    date = serializers.ReadOnlyField()

    class Meta:
        model = PersonNote
        fields = (
            'author',
            'date',
            'note'
        )


class QualificationSerializer(serializers.ModelSerializer):
    """
    Serializes Qualification model
    Qualification records form a related set of a SubactivityCode object
    """

    description = serializers.ReadOnlyField(source='well_class.description')

    class Meta:
        model = Qualification
        fields = (
            'well_class',
            'description',
        )


class ContactInfoSerializer(AuditModelSerializer):
    """
    Serializes ContactInfo model fields.
    """

    class Meta:
        model = ContactInfo
        fields = (
            'contact_tel',
            'contact_email'
        )


class SubactivitySerializer(serializers.ModelSerializer):
    """
    Serializes SubactivityCode model
    SubactivityCode records form a related set of an ActivityCode object
    """

    qualification_set = QualificationSerializer(many=True, read_only=True)

    class Meta:
        model = SubactivityCode
        fields = (
            'registries_subactivity_code',
            'description',
            'qualification_set',
        )


class ApplicationStatusSerializer(serializers.ModelSerializer):
    """
    Serializes RegistriesApplicationStatus for admin users
    ApplicationStatus objects form a related set for an Application object.
    """
    description = serializers.StringRelatedField(source='status.description')

    class Meta:
        model = RegistriesApplicationStatus
        fields = (
            'status',
            'description',
            'notified_date',
            'effective_date',
            'expired_date',
        )


class ApplicationListSerializer(AuditModelSerializer):
    """
    Serializes RegistryApplication model fields for anonymous users
    """

    qualifications = serializers.StringRelatedField(
        source='subactivity.qualification_set',
        many=True,
        read_only=True)
    subactivity = SubactivitySerializer()
    cert_authority = serializers.ReadOnlyField(
        source="primary_certificate.cert_auth.cert_auth_code")

    class Meta:
        model = RegistriesApplication
        fields = (
            'qualifications',
            'subactivity',
            'qualifications',
            'cert_authority')


class OrganizationListSerializer(AuditModelSerializer):
    """
    Serializes Organization model fields for "list" view.
    """

    class Meta:
        model = Organization
        fields = (
            'org_guid',
            'name',
            'org_verbose_name',
            'street_address',
            'city',
            'province_state',
            'postal_code',
            'main_tel',
            'fax_tel',
            'website_url',
        )


class RegistrationsListSerializer(serializers.ModelSerializer):
    """
    Serializes Register model for public/non authenticated users
    Register items form a related set of an Application object
    """
    status = serializers.ReadOnlyField(source='status.description')
    activity_description = serializers.ReadOnlyField(
        source='registries_activity.description')
    activity = serializers.ReadOnlyField(
        source="registries_activity.registries_activity_code")
    applications = serializers.SerializerMethodField()
    organization = OrganizationListSerializer()

    class Meta:
        model = Register
        fields = (
            'activity',
            'activity_description',
            'status',
            'registration_no',
            'applications',
            'organization'
        )

    def get_applications(self, registration):
        """
        Filter for approved applications (application has an 'approved' status that is not expired)
        """

        applications = [
            app for app in registration.applications.all()
            if any((x.status.registries_application_status_code == 'A' and x.expired_date is None)
                   for x in app.status_set.all())]

        serializer = ApplicationListSerializer(
            instance=applications, many=True)
        return serializer.data


class PersonBasicSerializer(serializers.ModelSerializer):
    """
    Serializes Person model with basic fields only
    """

    class Meta:
        model = Person
        fields = ('person_guid', 'name')


class PersonSerializer(AuditModelSerializer):
    """
    Serializes the Person model (public/anonymous user fields)
    """

    registrations = RegistrationsListSerializer(many=True, read_only=True)

    class Meta:
        model = Person
        fields = (
            'person_guid',
            'first_name',
            'surname',
            'registrations',
        )


class OrganizationSerializer(AuditModelSerializer):
    """
    Serializes Organization model fields (public fields list)
    """

    class Meta:
        model = Organization
        fields = (
            'org_guid',
            'name',
            'org_verbose_name',
            'street_address',
            'city',
            'province_state',
            'postal_code',
            'main_tel',
            'fax_tel',
            'website_url',
        )


class OrganizationAdminSerializer(AuditModelSerializer):
    """
    Serializes Organization model fields (admin fields list)
    """

    person_set = PersonSerializer(many=True, read_only=True)

    class Meta:
        model = Organization
        fields = (
            'create_user',
            'create_date',
            'update_user',
            'update_date',
            'org_guid',
            'name',
            'org_verbose_name',
            'street_address',
            'city',
            'province_state',
            'postal_code',
            'main_tel',
            'fax_tel',
            'website_url',
            'person_set',
        )


class ActivitySerializer(serializers.ModelSerializer):
    """
    Serializes ActivityCode model
    A Register record has a foreign key relationship to an ActivityCode object
    """

    class Meta:
        model = ActivityCode
        fields = (
            'registries_activity_code',
            'description',
        )


class ApplicationAdminSerializer(AuditModelSerializer):
    """
    Serializes RegistryApplication model fields for admin users
    """

    status_set = ApplicationStatusSerializer(many=True, read_only=True)
    current_status = ApplicationStatusSerializer(required=False)
    cert_authority = serializers.ReadOnlyField(
        source="primary_certificate.cert_auth.cert_auth_code")
    qualifications = serializers.StringRelatedField(
        source='subactivity.qualification_set',
        many=True,
        read_only=True)
    subactivity = SubactivitySerializer()

    class Meta:
        model = RegistriesApplication
        fields = (
            'create_user',
            'create_date',
            'update_user',
            'update_date',
            'application_guid',
            'registration',
            'file_no',
            'over19_ind',
            'cert_authority',
            'registrar_notes',
            'reason_denied',
            'subactivity',
            'qualifications',
            'status_set',
            'current_status'
        )

    def to_internal_value(self, data):
        """
        Set fields to different serializers for create/update operations.
        This method is called on POST/PUT/PATCH requests
        """
        self.fields['subactivity'] = serializers.PrimaryKeyRelatedField(
            queryset=SubactivityCode.objects.all())
        return super(ApplicationAdminSerializer, self).to_internal_value(data)

    def create(self, validated_data):
        """
        Create an application as well as a default status record of "pending"
        """
        try:
            app = RegistriesApplication.objects.create(**validated_data)
        except TypeError:
            raise TypeError('A field may need to be made read only.')

        # make a status record to go with the new application
        # by default we set the ApplicationStatus to P(ending).
        pending = ApplicationStatusCode.objects.get(
            registries_application_status_code='P')
        RegistriesApplicationStatus.objects.create(
            application=app,
            status=pending)

        return app

    @transaction.atomic
    def update(self, instance, validated_data):
        """
        The update is wrapped inside a transaction since we're changing a few
        records and creating one. We want to avoid a state where where a partial
        change occurs, especially if it leaves an application without a current
        status.
        """
        # We pop the current status, as the update method on the base
        # class cannot serialize nested fields.
        validated_status = validated_data.pop('current_status', None)

        if validated_status:
            # Validated_status is an OrderedDict at this point.
            validated_status_code = validated_status.get(
                'status').registries_application_status_code
            current_status = instance.current_status
            if current_status:
                current_status_code = current_status.status.registries_application_status_code
            else:
                logger.error(
                    'RegistryApplication {} does not have a current status'.format(instance))
                current_status_code = None

            if validated_status_code != current_status_code:
                if current_status:
                    # Expire existing status.
                    current_status.expired_date = timezone.now()
                    current_status.save()
                new_status = ApplicationStatusCode.objects.get(
                    registries_application_status_code=validated_status_code)
                # Create a new status.
                RegistriesApplicationStatus.objects.create(
                    application=instance,
                    status=new_status)

        return super().update(instance, validated_data)


class RegistrationAdminSerializer(AuditModelSerializer):
    """
    Serializes Register model for admin users
    """
    status = serializers.PrimaryKeyRelatedField(
        queryset=RegistriesStatusCode.objects.all())
    register_removal_reason = serializers.StringRelatedField(read_only=True)
    applications = ApplicationAdminSerializer(many=True, read_only=True)
    person_name = serializers.StringRelatedField(source='person.name')
    organization = OrganizationListSerializer()
    activity_description = serializers.StringRelatedField(
        source='registries_activity.description')

    class Meta:
        model = Register
        fields = (
            'create_user',
            'create_date',
            'update_user',
            'update_date',
            'register_guid',
            'person',
            'person_name',
            'registries_activity',
            'activity_description',
            'status',
            'registration_no',
            'registration_date',
            'register_removal_reason',
            'register_removal_date',
            'applications',
            'organization'
        )

    def to_internal_value(self, data):
        """
        Set fields to different serializers for create/update operations.
        """
        self.fields['organization'] = serializers.PrimaryKeyRelatedField(
            queryset=Organization.objects.all(), required=False, allow_null=True)
        return super(RegistrationAdminSerializer, self).to_internal_value(data)


class CityListSerializer(serializers.ModelSerializer):
    """
    Serializes city and province fields for list of cities with qualified drillers
    The queryset is limited to one record per unique city in the Person table
    The OrganizationSerializer fields are used to fill in city, province data
    """

    organization = OrganizationSerializer()

    class Meta:
        model = Register
        fields = (
            'organization',
        )

    def to_representation(self, instance):
        """
        Flattens City list response to make an array of { city: '', province_state: '' } objects
        """
        repr = super().to_representation(instance)

        # remove and store nested objects
        org = repr.pop('organization')

        # specify fields from OrganizationSerializer
        company_fields = (
            'city',
            'province_state',
        )

        for field in company_fields:
            if org and org[field]:
                repr[field] = org[field]
            else:
                repr[field] = None

        return repr


class PersonListSerializer(AuditModelSerializer):
    """
    Serializes the Person model for a list view (fewer fields than detail view)
    """
    contact_info = ContactInfoSerializer(many=True, read_only=True)
    registrations = serializers.SerializerMethodField()

    class Meta:
        model = Person
        fields = (
            'person_guid',
            'first_name',
            'surname',
            'registrations',
            'contact_info',
            'contact_tel',
            'contact_cell',
            'contact_email'
        )

    def get_registrations(self, person):
        """
        Filter for active registrations
        """

        registrations = [
            reg for reg in person.registrations.all() if reg.status.registries_status_code == 'ACTIVE']

        serializer = RegistrationsListSerializer(
            instance=registrations, many=True)
        return serializer.data


class RegistrationAutoCreateSerializer(AuditModelSerializer):
    """
    Serializer for creating a registration when a Person record is created
    """

    class Meta:
        model = Register
        fields = ('registries_activity', 'status',
                  'registration_no', 'organization')


class PersonAdminSerializer(AuditModelSerializer):
    """
    Serializes the Person model (admin user fields)
    """

    registrations = RegistrationAdminSerializer(many=True)
    contact_info = ContactInfoSerializer(many=True, required=False)
    notes = PersonNoteSerializer(many=True, read_only=True)

    def to_internal_value(self, data):
        """
        Set fields to different serializers for create/update operations.
        This method is called on POST/PUT/PATCH requests
        """
        self.fields['registrations'] = RegistrationAutoCreateSerializer(
            many=True, required=False)
        return super(PersonAdminSerializer, self).to_internal_value(data)

    def create(self, validated_data):
        """
        Create Register and ContactInfo records to go along with a new person record
        """

        registrations = validated_data.pop(
            'registrations') if 'registrations' in validated_data else list()
        contacts = validated_data.pop(
            'contact_info') if 'contact_info' in validated_data else list()

        person = Person.objects.create(**validated_data)

        for reg_data in registrations:
            Register.objects.create(person=person, **reg_data)
        for contact_data in contacts:
            ContactInfo.objects.create(person=person, **contact_data)
        return person

    def update(self, instance, validated_data):
        """
        Remove nested serializers before updating Person instance
        """
        if 'registrations' in validated_data:
            validated_data.pop('registrations')
        if 'contact_info' in validated_data:
            validated_data.pop('contact_info')
        return super(PersonAdminSerializer, self).update(instance, validated_data)

    class Meta:
        model = Person
        fields = (
            'person_guid',
            'first_name',
            'surname',
            'contact_tel',
            'contact_cell',
            'contact_email',
            'contact_info',
            'well_driller_orcs_no',
            'pump_installer_orcs_no',
            'registrations',
            'notes',
            'create_user',
            'create_date',
            'update_user',
            'update_date',
        )


class OrganizationNameListSerializer(serializers.ModelSerializer):
    """
    Organization list serializer (name of organization only)
    """

    class Meta:
        model = Organization
        fields = ('org_guid', 'name', 'org_verbose_name')
