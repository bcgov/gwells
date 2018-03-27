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
    QualificationCode,
    ClassificationAppliedFor
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
    Serializes QualificationCode model
    QualificationCode records form a related set of a SubactivityCode object
    """

    class Meta:
        model = QualificationCode
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


class OrganizationSerializer(AuditModelSerializer):
    """
    Serializes Organization model fields (public fields list)
    """

    province_state = serializers.PrimaryKeyRelatedField(queryset=ProvinceStateCode.objects.all(), required=False)
    contacts = ContactInfoSerializer(many=True, read_only=True)

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
    contacts = ContactInfoSerializer(many=True, read_only=True)

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


class SubactivitySerializer(serializers.ModelSerializer):
    """
    Serializes SubactivityCode model
    SubactivityCode records form a related set of an ActivityCode object
    """
    qualificationcode_set = QualificationSerializer(many=True)

    class Meta:
        model = SubactivityCode
        fields = (
            'registries_subactivity_guid',
            'code',
            'description',
            'qualificationcode_set'
        )


class ClassificationAppliedForSerializer(serializers.ModelSerializer):
    """
    Serializes the ClassificationAppliedFor model.
    ClassificationAppliedFor objects form a related set of Application objects
    """
    primary_certificate_authority = OrganizationSerializer(many=False, read_only=True)
    registries_subactivity = SubactivitySerializer(many=False)

    class Meta:
        model = ClassificationAppliedFor
        fields = (
            'registries_subactivity',
            'primary_certificate_authority',
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

    class Meta:
        model = RegistriesApplication
        fields = (
            'application_guid',
            'file_no',
            'reason_denied',
            'qualifications',
            'status_set'
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


class ApplicationAdminSerializer(AuditModelSerializer):
    """
    Serializes RegistryApplication model fields for admin users
    """

    
    classificationappliedfor_set = ClassificationAppliedForSerializer(many=True, read_only=True)
    registriesapplicationstatus_set = ApplicationStatusSerializer(many=True, read_only=True)

    class Meta:
        model = RegistriesApplication
        fields = (
            'application_guid',
            'person',
            'file_no',
            'over19_ind',
            'registrar_notes',
            'reason_denied',
            'classificationappliedfor_set',
            'registriesapplicationstatus_set'
        )


class RegistrationsAdminSerializer(serializers.ModelSerializer):
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

    companies = ContactInfoSerializer(many=True, read_only=True)

    class Meta:
        model = Person
        fields = (
            'companies',
        )


    def to_representation(self, obj):
        """
        Flattens City list response
        """
        repr = super().to_representation(obj)

        # remove and store nested objects
        companies = repr.pop('companies')

        # specify fields from ContactInfoSerializer.meta.fields
        company_fields = (
            'city',
            'province_state',
        )

        # bring each of the specified fields from the nested "companies" dict to the main dict
        # NOTE: because of the one to many relationship, we get an array of companies
        # After discussing with LM, we will return only the first company.
        for field in company_fields:
            if len(companies) and companies[0][field]:
                repr[field] = companies[0][field]
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

        # Using all fields for now
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

    class Meta:
        model = Person
        fields = (
            'person_guid',
            'first_name',
            'surname',
            'organization',
            'registrations',
        )


    # def to_representation(self, obj):
    #     """
    #     Flattens Person list response
    #     fields must be unique (PersonListSerializer.meta.fields, company_fields and registration_fields)
    #     Missing fields are given an empty string
    #     """
    #     repr = super().to_representation(obj)

    #     # remove and store nested objects
    #     companies = repr.pop('companies')
    #     applications = repr.pop('applications')
    #     registrations = None
    #     if len(applications) and len(applications[0]['registrations']):
    #         registrations = applications[0].pop('registrations')

    #     # specify fields from ContactInfoSerializer.meta.fields
    #     company_fields = (
    #         'organization_name',
    #         'street_address',
    #         'city',
    #         'province_state',
    #         'contact_tel',
    #         'contact_email'
    #     )

    #     # from RegistrationsSerializer.meta.fields
    #     registration_fields = ('activity', 'status', 'registration_no')

    #     # bring each of the specified fields from the nested "companies" dict to the main dict
    #     # NOTE: because of the one to many relationship, we get an array of companies
    #     # After discussing with LM, we will return only the first company.
    #     for field in company_fields:
    #         if len(companies) and companies[0][field]:
    #             repr[field] = companies[0][field]
    #         else:
    #             repr[field] = None

    #     for field in registration_fields:
    #         if registrations and len(registrations) > 0 and registrations[0][field]:
    #             repr[field] = registrations[0][field]
    #         else:
    #             repr[field] = None

    #     return repr


class PersonSerializer(AuditModelSerializer):
    """
    Serializes the Person model (public/anonymous user fields)
    """

    company = ContactInfoSerializer(many=True, read_only=True)
    registrations = RegistrationsListSerializer(many=True, read_only=True)

    class Meta:
        model = Person
        fields = (
            'person_guid',
            'first_name',
            'surname',
            'company',
            'registrations',
        )


class PersonAdminSerializer(AuditModelSerializer):
    """
    Serializes the Person model (admin user fields)
    """

    organization = OrganizationSerializer()
    registrations = RegistrationsAdminSerializer(many=True, read_only=True)

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
