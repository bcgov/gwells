from rest_framework import serializers
from registries.models import Organization
from gwells.models import ProvinceState

class DrillerListSerializer(serializers.ModelSerializer):
    province_state = serializers.ReadOnlyField()

    class Meta:
        model = Organization

        # Using all fields for now
        fields = (
            #'who_created',
            #'when_created',
            #'who_updated',
            #'when_updated',
            'name',
            'street_address',
            'city',
            'province_state',
            'postal_code',
            'main_tel',
            'fax_tel',
            'website_url',
            'certificate_authority',
        )
