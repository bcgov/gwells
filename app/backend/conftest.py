import pytest
import get_env_variable
import settings

engines = {
    'sqlite': 'django.db.backends.sqlite3',
    'postgresql': 'django.db.backends.postgresql',
    'postgis': 'django.contrib.gis.db.backends.postgis',
    'mysql': 'django.db.backends.mysql',
}

@pytest.fixture(scope='session')
def django_db_setup():
    service_name = get_env_variable('DATABASE_SERVICE_NAME', '').upper().replace('-', '_')
    name = get_env_variable('DATABASE_NAME')
    engine = engines['postgis']

    settings.DATABASES['gwells'] = {
        'ENGINE': engine,
        'NAME': name,
        'USER': get_env_variable('DATABASE_USER'),
        'PASSWORD': get_env_variable('DATABASE_PASSWORD'),
        'HOST': get_env_variable('{}_SERVICE_HOST'.format(service_name)),
        'PORT': get_env_variable('{}_SERVICE_PORT'.format(service_name)),
    }