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
    status = serializers.StringRelatedField(source='status.code')
    activity = serializers.StringRelatedField(source='registries_activity.code')

    class Meta:
        model = Register
        fields = (
            # 'register_guid',
            'activity',
            'status',
        )


class ApplicationSerializer(AuditModelSerializer):
    """
    Serializes RegistryApplication model fields
    """

    registrations = RegistrationsSerializer(many=True, read_only=True)

    class Meta:
        model = RegistriesApplication
        fields = (
            # 'application_guid',
            # 'person',
            # 'file_no',
            # 'over19_ind',
            # 'registrar_notes',
            # 'reason_denied',
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
            'person',
            'org',
            'person_name',
            'organization_name',
            'contact_tel',
            'contact_email'
        )


# class ProvinceStateCodeSerializer(serializers.ModelSerializer):
#     """
#     Serializes Province/State objects for use by the Organization endpoints
#     """

#     class Meta:
#         model = ProvinceStateCode
#         fields = (
#             'province_state_guid',
#             'code',
#             'description',
#             'sort_order',
#         )


class OrganizationListSerializer(AuditModelSerializer):
    """
    Serializes Organization model fields for "list" view.
    """

    province_state = serializers.ReadOnlyField(source="province_state.code")

    class Meta:
        model = Organization

        # Using all fields for now
        fields = (
            # 'create_user',
            # 'create_date',
            # 'update_user',
            # 'update_date',
            'org_guid',
            'name',
            'street_address',
            'city',
            'province_state',
            'postal_code',
            'main_tel',
            #'fax_tel',
            #'website_url',
            #'certificate_authority',
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
            # 'create_user',
            # 'create_date',
            # 'update_user',
            # 'update_date',
            'person_guid',
            'first_name',
            'surname',
            'companies',
            'applications',
        )


class PersonSerializer(AuditModelSerializer):
    """
    Serializes the Person model
    """

    companies = ContactAtSerializer(many=True, read_only=True)

    class Meta:
        model = Person
        fields = (
            'person_guid',
            'first_name',
            'surname',
            'companies',
            'create_user',
            'create_date',
            'update_user',
            'update_date',
        )
