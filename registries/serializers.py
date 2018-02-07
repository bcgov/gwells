from rest_framework import serializers
from registries.models import Organization
from gwells.models import ProvinceState


class DrillerListSerializer(serializers.ModelSerializer):
    """
    Serializer for Driller model "list" view.
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
