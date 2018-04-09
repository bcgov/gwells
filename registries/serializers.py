from rest_framework import serializers
from gwells.models.ProvinceStateCode import ProvinceStateCode
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
    ApplicationStatusCode
)


class AuditModelSerializer(serializers.ModelSerializer):
    """
    Serializes AuditModel fields.
    Can be inherited into serializers for models that inherit from AuditModel
    """
    create_user = serializers.ReadOnlyField()
    create_date = serializers.ReadOnlyField()
    update_user = serializers.ReadOnlyField()
    update_date = serializers.ReadOnlyField()


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
    status_set = ApplicationStatusSerializer(many=True, read_only=True)
    subactivity = SubactivitySerializer()
    cert_authority = serializers.ReadOnlyField(source="primary_certificate.cert_auth.cert_auth_code")

    class Meta:
        model = RegistriesApplication
        fields = (
            'application_guid',
            'file_no',
            'reason_denied',
            'qualifications',
            'status_set',
            'subactivity',
            'qualifications',
            'cert_authority')


class RegistrationsListSerializer(serializers.ModelSerializer):
    """
    Serializes Register model
    Register items form a related set of an Application object
    """
    status = serializers.ReadOnlyField(source='status.description')
    activity_description = serializers.ReadOnlyField(source='registries_activity.description')
    activity = serializers.ReadOnlyField(source="registries_activity.registries_activity_code")
    applications = ApplicationListSerializer(many=True, read_only=True)

    class Meta:
        model = Register
        fields = (
            'activity',
            'activity_description',
            'status',
            'registration_no',
            'applications'
        )


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
    qualifications = serializers.StringRelatedField(
        source='subactivity.qualification_set',
        many=True,
        read_only=True)

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
            'registrar_notes',
            'reason_denied',
            'subactivity',
            'qualifications',
            'status_set'
        )
    
    def create(self, validated_data):
        """
        Create an application as well as a default status record of "pending"
        """
        try:
            app = RegistriesApplication.objects.create(**validated_data)
        except TypeError:
            raise TypeError('A field may need to be made read only.')
  
        # make a status record to go with the new application
        pending = ApplicationStatusCode.objects.get(registries_application_status_code='P')
        RegistriesApplicationStatus.objects.create(
            application=app,
            status=pending)

        return app


class RegistrationAdminSerializer(AuditModelSerializer):
    """
    Serializes Register model for admin users
    """
    status = serializers.PrimaryKeyRelatedField(queryset=RegistriesStatusCode.objects.all())
    register_removal_reason = serializers.StringRelatedField(read_only=True)
    applications = ApplicationAdminSerializer(many=True, read_only=True)
    person_name = serializers.StringRelatedField(source='person.name')

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
            'status',
            'registration_no',
            'registration_date',
            'register_removal_reason',
            'register_removal_date',
            'applications'
        )


class CityListSerializer(serializers.ModelSerializer):
    """
    Serializes city and province fields for list of cities with qualified drillers
    The queryset is limited to one record per unique city in the Person table
    The OrganizationSerializer fields are used to fill in city, province data
    """

    organization = OrganizationSerializer()

    class Meta:
        model = Person
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


class OrganizationListSerializer(AuditModelSerializer):
    """
    Serializes Organization model fields for "list" view.
    """

    class Meta:
        model = Organization
        fields = (
            'org_guid',
            'name',
            'street_address',
            'city',
            'province_state',
            'postal_code',
            'main_tel',
        )


class PersonListSerializer(AuditModelSerializer):
    """
    Serializes the Person model for a list view (fewer fields than detail view)
    """
    registrations = RegistrationsListSerializer(many=True, read_only=True)
    organization = OrganizationListSerializer()
    contact_info = ContactInfoSerializer(many=True, read_only=True)

    class Meta:
        model = Person
        fields = (
            'person_guid',
            'first_name',
            'surname',
            'organization',
            'registrations',
            'contact_info'
        )


class PersonAdminSerializer(AuditModelSerializer):
    """
    Serializes the Person model (admin user fields)
    """

    # organization = serializers.PrimaryKeyRelatedField(queryset=Organization.objects.all(), required=False)
    registrations = RegistrationAdminSerializer(many=True, read_only=True)
    organization = OrganizationListSerializer(required=False)

    def to_internal_value(self, data):
        self.fields['organization'] = serializers.PrimaryKeyRelatedField(
            queryset=Organization.objects.all(), required=False)
        return super(PersonAdminSerializer, self).to_internal_value(data)

    class Meta:
        model = Person
        fields = (
            'person_guid',
            'first_name',
            'surname',
            'organization',
            'registrations',
            'create_user',
            'create_date',
            'update_user',
            'update_date',
        )
