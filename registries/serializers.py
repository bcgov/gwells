from rest_framework import serializers
from gwells.models.ProvinceStateCode import ProvinceStateCode
from registries.models import (
    Organization,
    ContactInfo,
    Person,
    Register,
    RegistriesApplication,
    RegistriesApplicationStatus,
    ActivityCode,
    SubactivityCode,
    Qualification
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

    class Meta:
        model = Qualification
        fields = (
            'code',
            'description'
        )


class ContactInfoSerializer(AuditModelSerializer):
    """
    Serializes ContactInfo model fields.
    """
    person_name = serializers.StringRelatedField(source="person")
    organization_name = serializers.StringRelatedField(source="org")
    street_address = serializers.StringRelatedField(source="org.street_address")
    city = serializers.StringRelatedField(source="org.city")
    province_state = serializers.StringRelatedField(source="org.province_state.province_state_code")
    postal_code = serializers.StringRelatedField(source="org.postal_code")
    website_url = serializers.StringRelatedField(source="org.website_url")

    class Meta:
        model = ContactInfo
        fields = (
            'contact_at_guid',
            'organization_name',
            'street_address',
            'city',
            'postal_code',
            'province_state',
            'person_name',
            'person',
            'org',
            'contact_tel',
            'contact_email',
            'website_url'
        )


class SubactivitySerializer(serializers.ModelSerializer):
    """
    Serializes SubactivityCode model
    SubactivityCode records form a related set of an ActivityCode object
    """

    class Meta:
        model = SubactivityCode
        fields = (
            'registries_subactivity_guid',
            'code',
            'description',
        )


class ApplicationStatusSerializer(serializers.ModelSerializer):
    """
    Serializes RegistriesApplicationStatus for admin users
    ApplicationStatus objects form a related set for an Application object.
    """
    status = serializers.StringRelatedField(many=False, read_only=True)
    status_code = serializers.ReadOnlyField(source="status.code")

    class Meta:
        model = RegistriesApplicationStatus
        fields = (
            'status',
            'status_code',
            'notified_date',
            'effective_date',
            'expired_date',
        )


class ApplicationListSerializer(AuditModelSerializer):
    """
    Serializes RegistryApplication model fields for anonymous users
    """

    qualifications = QualificationSerializer(many=True, read_only=True)
    status_set = ApplicationStatusSerializer(many=True, read_only=True)
    subactivity = SubactivitySerializer()

    class Meta:
        model = RegistriesApplication
        fields = (
            'application_guid',
            'file_no',
            'reason_denied',
            'qualifications',
            'status_set',
            'subactivity'
        )


class RegistrationsListSerializer(serializers.ModelSerializer):
    """
    Serializes Register model
    Register items form a related set of an Application object
    """
    status = serializers.ReadOnlyField(source='status.description')
    activity = serializers.ReadOnlyField(source='registries_activity.description')
    applications = ApplicationListSerializer(many=True, read_only=True)

    class Meta:
        model = Register
        fields = (
            'activity',
            'status',
            'registration_no',
            'applications'
        )


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

    province_state = serializers.PrimaryKeyRelatedField(queryset=ProvinceStateCode.objects.all(), required=False)
    people = PersonSerializer(many=True, read_only=True)

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
            'certificate_authority',
            'people',
        )


class OrganizationAdminSerializer(AuditModelSerializer):
    """
    Serializes Organization model fields (admin fields list)
    """

    province_state = serializers.PrimaryKeyRelatedField(queryset=ProvinceStateCode.objects.all(), required=False)
    people = PersonSerializer(many=True, read_only=True)

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
            'certificate_authority',
            'people',
        )


class ActivitySerializer(serializers.ModelSerializer):
    """
    Serializes ActivityCode model
    A Register record has a foreign key relationship to an ActivityCode object
    """

    class Meta:
        model = ActivityCode
        fields = (
            'registries_activity_guid',
            'code',
            'description',
        )


class ApplicationAdminSerializer(AuditModelSerializer):
    """
    Serializes RegistryApplication model fields for admin users
    """

    registriesapplicationstatus_set = ApplicationStatusSerializer(many=True, read_only=True)

    class Meta:
        model = RegistriesApplication
        fields = (
            'application_guid',
            'registration',
            'file_no',
            'over19_ind',
            'registrar_notes',
            'reason_denied',
            'classificationappliedfor_set',
            'registriesapplicationstatus_set'
        )


class RegistrationAdminSerializer(serializers.ModelSerializer):
    """
    Serializes Register model for admin users
    """
    status = serializers.ReadOnlyField(source='status.description')
    activity = serializers.ReadOnlyField(source='registries_activity.description')
    activity_code = serializers.ReadOnlyField(source='registries_activity.code')
    register_removal_reason = serializers.StringRelatedField(read_only=True)
    applications = ApplicationAdminSerializer(many=True, read_only=True)

    class Meta:
        model = Register
        fields = (
            'activity',
            'activity_code',
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
    """

    organization = OrganizationSerializer()

    class Meta:
        model = Person
        fields = (
            'organization',
        )


    def to_representation(self, obj):
        """
        Flattens City list response
        """
        repr = super().to_representation(obj)

        # remove and store nested objects
        org = repr.pop('organization')

        # specify fields from ContactInfoSerializer.meta.fields
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

    province_state = serializers.ReadOnlyField(source="province_state.province_state_code")

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
    organization = serializers.PrimaryKeyRelatedField(queryset=Organization.objects.all(), required=False)

    class Meta:
        model = Person
        fields = (
            'person_guid',
            'first_name',
            'surname',
            'organization',
            'registrations',
        )


class PersonAdminSerializer(AuditModelSerializer):
    """
    Serializes the Person model (admin user fields)
    """

    organization = serializers.PrimaryKeyRelatedField(queryset=Organization.objects.all(), required=False)
    registrations = RegistrationAdminSerializer(many=True, read_only=True)

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
