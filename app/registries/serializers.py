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
    ProofOfAgeCode,
    Organization,
    ContactInfo,
    Person,
    Register,
    RegistriesApplication,
    RegistriesStatusCode,
    ActivityCode,
    SubactivityCode,
    Qualification,
    ApplicationStatusCode,
    AccreditedCertificateCode,
    WellClassCode,
    PersonNote,
    PersonNote,
    OrganizationNote,
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


class ProofOfAgeCodeSerializer(serializers.ModelSerializer):
    """
    Serializes ProofOfAgeCode fields.
    """

    code = serializers.ReadOnlyField(source='registries_proof_of_age_code')

    class Meta:
        model = ProofOfAgeCode
        fields = (
            'code',
            'description'
        )

    def to_internal_value(self, data):
        if 'code' in data:
            return ProofOfAgeCode.objects.get(registries_proof_of_age_code=data['code'])
        return super().to_internal_value(data)


class OrganizationNoteSerializer(serializers.ModelSerializer):
    """
    Serializes OrganizationNote records
    """

    author = serializers.ReadOnlyField(source='author.profile.name')
    date = serializers.ReadOnlyField()

    class Meta:
        model = OrganizationNote
        fields = (
            'org_note_guid',
            'author',
            'date',
            'note'
        )


class PersonNoteSerializer(serializers.ModelSerializer):
    """
    Serializes PersonNote records
    """

    author = serializers.ReadOnlyField(source='author.profile.name')
    date = serializers.ReadOnlyField()

    class Meta:
        model = PersonNote
        fields = (
            'person_note_guid',
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

    qualification_set = QualificationSerializer(
        many=True,
        read_only=True)

    class Meta:
        model = SubactivityCode
        fields = (
            'registries_subactivity_code',
            'description',
            'qualification_set',
        )

    def to_internal_value(self, data):
        if 'registries_subactivity_code' in data:
            return SubactivityCode.objects.get(registries_subactivity_code=data['registries_subactivity_code'])
        return super().to_internal_value(data)


class ApplicationStatusCodeSerializer(serializers.ModelSerializer):

    code = serializers.ReadOnlyField(source='registries_application_status_code')

    class Meta:
        model = ApplicationStatusCode
        fields = (
            'code',
            'description'
        )

    def to_internal_value(self, data):
        if 'code' in data:
            return ApplicationStatusCode.objects.get(registries_application_status_code=data['code'])


class ApplicationListSerializer(AuditModelSerializer):
    """
    Serializes RegistryApplication model fields for anonymous users
    """

    qualifications = QualificationSerializer(
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
            'email',
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
            'organization',
        )

    def get_applications(self, registration):
        """
        Filter for approved applications (application has an 'approved' status that is not expired)
        """

        serializer = ApplicationListSerializer(
            instance=registration.applications.filter(current_status__registries_application_status_code='A'),
            many=True)
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
            'email',
            'website_url',
        )


class OrganizationAdminSerializer(AuditModelSerializer):
    """
    Serializes Organization model fields (admin fields list)
    """

    person_set = PersonSerializer(many=True, read_only=True)
    registrations_count = serializers.SerializerMethodField()
    notes = serializers.SerializerMethodField()

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
            'email',
            'website_url',
            'person_set',
            'notes',
            'registrations_count'
        )

    def get_notes(self, obj):
        """
        Get sorted notes
        """
        notes = OrganizationNote.objects \
            .filter(organization=obj.org_guid) \
            .order_by('-date') \
            .select_related('author', 'author__profile')
        serializer = OrganizationNoteSerializer(instance=notes, many=True)
        return serializer.data

    def get_registrations_count(self, obj):
        """ count registration records """
        return obj.registrations.count()


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


class AccreditedCertificateCodeSerializer(serializers.ModelSerializer):

    # CertifyingAuthorityCode
    cert_auth = serializers.ReadOnlyField(source='cert_auth.description')

    class Meta:
        model = AccreditedCertificateCode
        fields = (
            'acc_cert_guid',
            'name',
            'cert_auth'
        )

    def to_internal_value(self, data):
        if 'acc_cert_guid' in data:
            return AccreditedCertificateCode.objects.get(acc_cert_guid=data['acc_cert_guid'])
        return super().to_internal_value(data)


class ApplicationAdminSerializer(AuditModelSerializer):
    """
    Serializes RegistryApplication model fields for admin users
    """

    qualifications = serializers.StringRelatedField(
        source='subactivity.qualification_set',
        many=True,
        read_only=True)
    subactivity = SubactivitySerializer()
    registration = serializers.StringRelatedField(
        source='registration.register_guid')
    # We need choices here in order to popuplate an OPTIONS request with
    # valid values.
    primary_certificate = AccreditedCertificateCodeSerializer(required=False)
    primary_certificate_no = serializers.CharField(required=False)
    proof_of_age = ProofOfAgeCodeSerializer(required=False)
    current_status = ApplicationStatusCodeSerializer(required=False)

    class Meta:
        model = RegistriesApplication
        fields = (
            'application_outcome_date',
            'application_outcome_notification_date',
            'application_recieved_date',
            'create_user',
            'create_date',
            'update_user',
            'update_date',
            'application_guid',
            'registration',
            'file_no',
            'proof_of_age',
            'primary_certificate',
            'primary_certificate_no',
            'registrar_notes',
            'reason_denied',
            'subactivity',
            'qualifications',
            'current_status'
        )

    def to_internal_value(self, data):
        """
        Set fields to different serializers for create/update operations.
        This method is called on POST/PUT/PATCH requests
        """
        self.fields['registration'] = serializers.PrimaryKeyRelatedField(
            queryset=Register.objects.all())
        if 'application_outcome_date' in data and data['application_outcome_date'] == '':
            data['application_outcome_date'] = None
        if 'application_outcome_notification_date' in data and data['application_outcome_notification_date'] == '':
            data['application_outcome_notification_date'] = None
        if 'application_recieved_date' in data and data['application_recieved_date'] == '':
            data['application_recieved_date'] = None
        return super().to_internal_value(data)

    def create(self, validated_data):
        """
        Create an application as well as a default status record of "pending"
        """
        try:
            app = RegistriesApplication.objects.create(**validated_data)
        except TypeError:
            raise TypeError('A field may need to be made read only.')

        return app
    

class RegistrationAdminSerializer(AuditModelSerializer):
    """
    Serializes Register model for admin users
    """
    status = serializers.PrimaryKeyRelatedField(
        queryset=RegistriesStatusCode.objects.all())
    register_removal_reason = serializers.StringRelatedField(read_only=True)
    applications = ApplicationAdminSerializer(many=True, read_only=True)
    person_name = serializers.StringRelatedField(source='person.name')
    organization = OrganizationAdminSerializer()
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
        return super().to_internal_value(data)


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


class QualificationAutoCreateSerializer(serializers.ModelSerializer):
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


class ApplicationAutoCreateSerializer(AuditModelSerializer):
    """
    Serializes RegistryApplication when a Registration
    record is created
    """

    primary_certificate = AccreditedCertificateCodeSerializer(
        required=False)
    proof_of_age = ProofOfAgeCodeSerializer(required=False)
    qualifications = QualificationAutoCreateSerializer(
        many=True,
        read_only=True)
    registration = serializers.StringRelatedField(
        source='registration.register_guid')
    subactivity = SubactivitySerializer(
        required=False
    )

    class Meta:
        model = RegistriesApplication
        fields = (
            'application_recieved_date',
            'create_user',
            'create_date',
            'current_status',
            'update_user',
            'update_date',
            'application_guid',
            'registration',
            'file_no',
            'proof_of_age',
            'primary_certificate',
            'primary_certificate_no',
            'registrar_notes',
            'reason_denied',
            'subactivity',
            'qualifications'
        )


class RegistrationAutoCreateSerializer(AuditModelSerializer):
    """
    Serializer for creating a registration when a Person record is created
    """

    applications = ApplicationAutoCreateSerializer(many=True, required=False)

    class Meta:
        model = Register
        fields = (
            'registries_activity',
            'status',
            'registration_no',
            'organization',
            'applications',
            'create_user',
            'create_date',
        )


class PersonAdminSerializer(AuditModelSerializer):
    """
    Serializes the Person model (admin user fields)
    """

    registrations = RegistrationAdminSerializer(many=True)
    contact_info = ContactInfoSerializer(many=True, required=False)
    notes = serializers.SerializerMethodField()

    def get_notes(self, obj):
        """
        Get sorted notes
        """
        notes = PersonNote.objects \
            .filter(person=obj.person_guid) \
            .order_by('-date') \
            .select_related('author', 'author__profile')
        serializer = PersonNoteSerializer(instance=notes, many=True)
        return serializer.data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def to_internal_value(self, data):
        """
        Set fields to different serializers for create/update operations.
        This method is called on POST/PUT/PATCH requests
        """
        self.fields['registrations'] = RegistrationAutoCreateSerializer(
            many=True, required=False)
        return super().to_internal_value(data)

    def create(self, validated_data):
        """
        Create Register and ContactInfo records to go along with a new person record
        """
        registrations = validated_data.pop('registrations', list())
        contacts = validated_data.pop('contact_info', list())
        # The audit information has to be applied to all child records.
        audit_info = {'create_user': validated_data.get('create_user')}

        person = Person.objects.create(**validated_data)

        for reg_data in registrations:
            reg_data = {**reg_data, **audit_info}
            applications = reg_data.pop('applications', list())
            register = Register.objects.create(person=person, **reg_data)
            for app_data in applications:
                app_data = {**app_data, **audit_info}
                app = RegistriesApplication.objects.create(
                    registration=register, **app_data)
        for contact_data in contacts:
            contact_data = {**contact_data, **audit_info}
            contact = ContactInfo.objects.create(person=person, **contact_data)

        return Person.objects.get(person_guid=person.person_guid)

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


class WellClassCodeSerializer(serializers.ModelSerializer):
    """
    Well class code serializer
    """

    class Meta:
        model = WellClassCode
        fields = ('registries_well_class_code', 'description')
