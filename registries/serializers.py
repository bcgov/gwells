from rest_framework import serializers
from gwells.models.ProvinceStateCode import ProvinceStateCode
from registries.models import (
    Organization,
    ContactAt,
    Person,
    Register,   
    RegistriesApplication,
)

class AuditModelSerializer(serializers.ModelSerializer):
    """
    Serializes AuditModel fields.
    Can be inherited into serializers for models that inherit from AuditModel
    """
    create_user = serializers.StringRelatedField()
    create_date = serializers.ReadOnlyField()
    update_user = serializers.StringRelatedField()
    update_date = serializers.ReadOnlyField()


class RegistrationsSerializer(serializers.ModelSerializer):
    """
    Serializes Register model
    """
    status = serializers.ReadOnlyField(source='status.code')
    activity = serializers.ReadOnlyField(source='registries_activity.code')

    class Meta:
        model = Register
        fields = (
            'activity',
            'status',
            'registration_no'
        )


class ApplicationSerializer(AuditModelSerializer):
    """
    Serializes RegistryApplication model fields for anonymous users
    """

    registrations = RegistrationsSerializer(many=True, read_only=True)

    class Meta:
        model = RegistriesApplication
        fields = (
            'registrations',
        )


class ApplicationAdminSerializer(AuditModelSerializer):
    """
    Serializes RegistryApplication model fields for admin users
    """

    registrations = RegistrationsSerializer(many=True, read_only=True)

    class Meta:
        model = RegistriesApplication
        fields = (
            'application_guid',
            'person',
            'file_no',
            'over19_ind',
            'registrar_notes',
            'reason_denied',
            'registrations',
        )


class ContactAtSerializer(AuditModelSerializer):
    """
    Serializes ContactAt model fields.
    """
    person_name = serializers.StringRelatedField(source="person")
    organization_name = serializers.StringRelatedField(source="org")

    class Meta:
        model = ContactAt
        fields = (
            'contact_at_guid',            
            'organization_name',
            'person_name',
            'person',
            'org',
            'contact_tel',
            'contact_email'
        )


class OrganizationListSerializer(AuditModelSerializer):
    """
    Serializes Organization model fields for "list" view.
    """

    province_state = serializers.ReadOnlyField(source="province_state.province_state_code")
    contacts = ContactAtSerializer(many=True, read_only=True)

    class Meta:
        model = Organization

        # Using all fields for now
        fields = (
            'org_guid',
            'name',
            'street_address',
            'city',
            'province_state',
            'postal_code',
            'main_tel',
            'contacts',
        )


class OrganizationSerializer(AuditModelSerializer):
    """
    Serializes Organization model fields (public fields list)
    """

    province_state = serializers.PrimaryKeyRelatedField(queryset=ProvinceStateCode.objects.all(), required=False)
    contacts = ContactAtSerializer(many=True, read_only=True)

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
            'contacts',
        )

class OrganizationAdminSerializer(AuditModelSerializer):
    """
    Serializes Organization model fields (admin fields list)
    """

    province_state = serializers.PrimaryKeyRelatedField(queryset=ProvinceStateCode.objects.all(), required=False)
    contacts = ContactAtSerializer(many=True, read_only=True)

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
            'contacts',
        )


class PersonListSerializer(AuditModelSerializer):
    """
    Serializes the Person model for a list view (fewer fields than detail view)
    """

    companies = ContactAtSerializer(many=True, read_only=True)
    applications = ApplicationSerializer(many=True, read_only=True)

    class Meta:
        model = Person
        fields = (
            'person_guid',
            'first_name',
            'surname',
            'companies',
            'applications',
        )


class PersonSerializer(AuditModelSerializer):
    """
    Serializes the Person model (public/anonymous user fields)
    """

    companies = ContactAtSerializer(many=True, read_only=True)
    applications = ApplicationSerializer(many=True, read_only=True)

    class Meta:
        model = Person
        fields = (
            'person_guid',
            'first_name',
            'surname',
            'companies',
            'applications',
        )

class PersonAdminSerializer(AuditModelSerializer):
    """
    Serializes the Person model (admin user fields)
    """

    companies = ContactAtSerializer(many=True, read_only=True)
    applications = ApplicationAdminSerializer(many=True, read_only=True)

    class Meta:
        model = Person
        fields = (
            'person_guid',
            'first_name',
            'surname',
            'companies',
            'applications',
            'create_user',
            'create_date',
            'update_user',
            'update_date',
        )
