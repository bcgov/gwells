"""
    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""
import logging

from django.db import connection

from drf_yasg import openapi


logger = logging.getLogger(__name__)

GEO_JSON_302_MESSAGE = ('All requests to this endpoint result by default in a redirect to a pre-generated '
                        'GeoJSON file (as documented in 200 OK Response) hosted on a seperate server.')


GEO_JSON_PARAMS = [
    openapi.Parameter(
        'realtime',
        openapi.IN_QUERY,
        title="Experimental!",
        description=('If set to true, GWELLS will attempt to generate GeoJSON in realtime. By default GWELLS '
                     'will redirect to a location with a pre-generated GeoJSON file.'),
        type=openapi.TYPE_BOOLEAN,
        required=False,
        default=False),
    openapi.Parameter(
        'sw_long',
        openapi.IN_QUERY,
        title="Experimental!",
        description='South West extent (longitude component) of bounding box to limit results to.',
        type=openapi.TYPE_STRING,
        required=False,
        default=None
    ),
    openapi.Parameter(
        'sw_lat',
        openapi.IN_QUERY,
        title="Experimental!",
        description='South West extent (latitude component) of bounding box to limit results to.',
        type=openapi.TYPE_STRING,
        required=False,
        default=None
    ),
    openapi.Parameter(
        'ne_long',
        openapi.IN_QUERY,
        title="Experimental!",
        description='North East extent (longitude component) of bounding box to limit results to.',
        type=openapi.TYPE_STRING,
        required=False,
        default=None
    ),
    openapi.Parameter(
        'ne_lat',
        openapi.IN_QUERY,
        title="Experimental!",
        description='North East extent (latitude component) of bounding box to limit results to.',
        type=openapi.TYPE_STRING,
        required=False,
        default=None
    )
]


def get_field_type(field):
    """
    Given a DJango model field, return the appropriate openapi type.
    """
    internal_type = field.get_internal_type()
    if internal_type == 'AutoField' or internal_type == 'PositiveIntegerField':
        return openapi.TYPE_INTEGER
    elif internal_type == 'CharField' or internal_type == 'TextField':
        return openapi.TYPE_STRING
    elif internal_type == 'DecimalField':
        return openapi.TYPE_NUMBER
    elif internal_type == 'ForeignKey':
        return get_field_type(field.target_field)


def get_field_format(field):
    """
    Given a Django model field, return the appropriate openapi format.
    """
    internal_type = field.get_internal_type()
    if internal_type == 'AutoField' or internal_type == 'PositiveIntegerField':
        return openapi.FORMAT_INT32
    elif internal_type == 'DecimalField':
        return openapi.FORMAT_FLOAT
    elif internal_type == 'CharField' or internal_type == 'TextField':
        # No type for CharField
        return None
    elif internal_type == 'ForeignKey':
        return get_field_format(field.target_field)
    else:
        logger.info('not handling {}'.format(internal_type))
    return None


def get_column_minimum(internal_type):
    """
    Given an internal type, find the appropriate openapi minimum value.
    """
    if internal_type == 'PositiveIntegerField':
        return 0
    elif internal_type == 'AutoField':
        return 0
    return None


def get_model_feature_schema(model, field_name):
    """
    Given a field name for a particular model, create the appropriate openapi schema for GeoJSON feature.
    """
    args = {}
    field = model._meta.get_field(field_name)
    internal_type = field.get_internal_type()
    args['type'] = get_field_type(field)

    type_format = get_field_format(field)
    if type_format:
        args['format'] = type_format
        if type_format == openapi.FORMAT_FLOAT:
            type_string = field.db_type(connection)
            # The type string will be something like numeric(8, 3), where the 3, is the decimal places.
            scale = int(type_string[type_string.rfind(',')+1:-1].strip())
            # We do 0.1 to the power of decimal places, but have to round to get a nice clean number.
            args['multipleOf'] = round(pow(0.1, scale), scale)

    if args['type'] == openapi.TYPE_INTEGER:
        minimum = get_column_minimum(internal_type)
        if minimum is not None:
            args['minimum'] = minimum

    title = getattr(field, 'verbose_name', None)
    if title:
        args['title'] = title

    description = getattr(field, 'db_comment', None)
    if description:
        args['description'] = description

    if args['type'] == openapi.TYPE_STRING:
        max_length = getattr(field, 'max_length', None)
        if max_length:
            args['max_length'] = max_length

    return openapi.Schema(**args)


def get_geometry(geometry_type):
    """
    Given the desired geometry types, return an openapi schema for a GeoJSON geometry.
    """
    geometry_type_description = None
    if geometry_type == 'Point':
        geometry_type_description = 'https://tools.ietf.org/html/rfc7946#appendix-A.1'
    elif geometry_type == 'Polygon':
        geometry_type_description = 'https://tools.ietf.org/html/rfc7946#appendix-A.3'
    return openapi.Schema(
        type=openapi.TYPE_OBJECT,
        title='GeoJSON Geometry Object.',
        description='See: https://tools.ietf.org/html/rfc7946#section-3.1',
        properties={
            'type': openapi.Schema(
                type=openapi.TYPE_STRING,
                enum=[geometry_type],
                title='Geometry object type.',
                description=geometry_type_description),
            'coordinates': openapi.Schema(
                type=openapi.TYPE_ARRAY,
                description='Array of coordinates.',
                items=openapi.Schema(
                    type=openapi.TYPE_NUMBER,
                    format=openapi.FORMAT_FLOAT))
        })


def get_features(properties, geometry_type):
    """
    Given the properties and geometry types, return a openapi schema for a GeoJSON feature.
    """
    return openapi.Schema(
        type=openapi.TYPE_ARRAY,
        description='Array of GeoJSON "Feature" objects.',
        items=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'type': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    enum=['Feature'],
                    title='GeoJSON object type.',
                    description='See: https://tools.ietf.org/html/rfc7946#section-3.2'),
                'geometry': get_geometry(geometry_type),
                'properties': properties
            }
        ))


def get_geojson_schema(properties, geometry_type):
    """
    Given the properties and geometry types, return an openapi schema for a GeoJSON response.
    """
    return openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'type': openapi.Schema(
                type=openapi.TYPE_STRING,
                enum=[
                    'FeatureCollection'],
                title='GeoJSON object type.',
                description='See: https://tools.ietf.org/html/rfc7946#section-3.3'),
            'features': get_features(properties, geometry_type)
        })
