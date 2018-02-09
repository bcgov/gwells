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
    who_created = serializers.StringRelatedField()
    when_created = serializers.ReadOnlyField()
    who_updated = serializers.StringRelatedField()
    when_updated = serializers.ReadOnlyField()


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
            #'who_created',
            #'when_created',
            #'who_updated',
            #'when_updated',
            'org_guid',
            'name',
            'street_address',
            'city',
            'province_state',
            'postal_code',
            'main_tel',
            'who_created'
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
            'who_created',
            'when_created',
            'who_updated',
            'when_updated',
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


class PersonSerializer(AuditModelSerializer):
    """
    Serializes the Person model
    """

    companies = ContactAtSerializer(many=True, read_only=True)

    class Meta:
        model = Person
        fields = (
            'who_created',
            'when_created',
            'who_updated',
            'when_updated',
            'person_guid',
            'first_name',
            'surname',
            'companies',
        )


class PersonListSerializer(AuditModelSerializer):
    """
    Serializes the Person model for a list view (fewer fields than detail view)
    """

    companies = ContactAtSerializer(many=True, read_only=True)

    class Meta:
        model = Person
        fields = (
            # 'who_created',
            # 'when_created',
            # 'who_updated',
            # 'when_updated',
            'person_guid',
            'first_name',
            'surname',
            'companies',
        )
