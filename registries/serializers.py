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
    status = serializers.ReadOnlyField(source='status.description')
    activity = serializers.ReadOnlyField(source='registries_activity.description')

    class Meta:
        model = Register
        fields = (
            # 'register_guid',
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
            # 'application_guid',
            # 'person',
            # 'file_no',
            # 'over19_ind',
            # 'registrar_notes',
            # 'reason_denied',
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
#             'display_order',
#         )


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
            'contacts',
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


    def to_representation(self, obj):
        """
        Flattens Person list response
        fields must be unique (PersonListSerializer.meta.fields, company_fields and registration_fields)
        Missing fields are given an empty string
        """
        repr = super().to_representation(obj)

        # remove and store nested objects
        companies = repr.pop('companies')
        applications = repr.pop('applications')
        registrations = None
        if len(applications) and len(applications[0]['registrations']):
            registrations = applications[0].pop('registrations')

        # specify fields from ContactAtSerializer.meta.fields
        company_fields = ('organization_name', 'contact_tel', 'contact_email')

        # from RegistrationsSerializer.meta.fields
        registration_fields = ('activity', 'status', 'registration_no')

        # bring each of the specified fields from the nested "companies" dict to the main dict
        # NOTE: because of the one to many relationship, we get an array of companies
        # After discussing with LM, we will return only the first company.
        for field in company_fields:
            if len(companies) and companies[0][field]:
                repr[field] = companies[0][field]
            else:
                repr[field] = None

        for field in registration_fields:
            if registrations and len(registrations) > 0 and registrations[0][field]:
                repr[field] = registrations[0][field]
            else:
                repr[field] = None

        return repr


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
            # 'create_user',
            # 'create_date',
            # 'update_user',
            # 'update_date',
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
