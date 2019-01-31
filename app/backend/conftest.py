import pytest

@pytest.fixture(scope='session')
def django_db_setup():
"""

DATABASE_SCHEMA=public
DATABASE_USER=userGN0
DATABASE_NAME=gwells
DATABASE_ENGINE=postgresql
DATABASE_SERVICE_NAME=gwells-pgsql-dev-pr-1116
"""
    settings.DATABASES['default'] = {
        'ENGINE': get_env_variable('DATABASE_ENGINE'),
        'NAME': get_env_variable('DATABASE_NAME'),
        'USER': get_env_variable('DATABASE_USER'),
        'PASSWORD': get_env_variable('DATABASE_PASSWORD'),
        'HOST': get_env_variable('DATABASE_SERVICE_NAME'),
        'PORT': get_env_variable('POSTGRESQL_SERVICE_PORT'),
    }
