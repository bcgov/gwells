import pytest
from gwells.settings.base import get_env_variable

@pytest.fixture(scope='session')
def django_db_setup():
    service_name = get_env_variable('DATABASE_SERVICE_NAME', '').upper().replace('-', '_')

    settings.DATABASES['default'] = {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'HOST': get_env_variable('DATABASE_SERVICE_NAME'),        
        'NAME': get_env_variable('DATABASE_NAME'),
        'USER': get_env_variable('DATABASE_USER'),
        'PASSWORD': get_env_variable('DATABASE_PASSWORD'),
        'HOST': get_env_variable('{}_SERVICE_HOST'.format(service_name)),
        'PORT': get_env_variable('{}_SERVICE_PORT'.format(service_name)),
    }