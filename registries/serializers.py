from rest_framework import serializers
from registries.models import (
    Organization,
    ContactAt,
    Person
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

class OrganizationListSerializer(AuditModelSerializer):
    """
    Serializes Organization model fields for "list" view.
    """

    province_state = serializers.ReadOnlyField(source="province_state.code")

    class Meta:
        model = Organization

        # Using all fields for now
        fields = (
            #'create_user',
            #'create_date',
            #'update_user',
            #'update_date',
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

    province_state = serializers.ReadOnlyField(source="province_state.code")
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
        )


class PersonSerializer(AuditModelSerializer):
    """
    Serializes the Person model
    """

    companies = ContactAtSerializer(many=True, read_only=True)

    class Meta:
        model = Person
        fields = (
            'create_user',
            'create_date',
            'update_user',
            'update_date',
            'person_guid',
            'first_name',
            'surname',
            'companies',
        )
