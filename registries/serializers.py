from rest_framework import serializers
from registries.models import (
    Organization,
    ContactAt,
    Person
)

class ContactAtSerializer(serializers.ModelSerializer):
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

class OrganizationListSerializer(serializers.ModelSerializer):
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
            #'fax_tel',
            #'website_url',
            #'certificate_authority',
        )


class OrganizationSerializer(serializers.ModelSerializer):
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


class PersonSerializer(serializers.ModelSerializer):
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


class PersonListSerializer(serializers.ModelSerializer):
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
