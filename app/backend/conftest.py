import pytest

@pytest.fixture(scope='session')
def django_db_setup():
    settings.DATABASES['gwells'] = {
        'ENGINE': get_env_variable('DATABASE_ENGINE'),
        'NAME': get_env_variable('DATABASE_NAME'),
        'USER': get_env_variable('DATABASE_USER'),
        'PASSWORD': get_env_variable('DATABASE_PASSWORD'),
        'HOST': get_env_variable('DATABASE_SERVICE_NAME'),
        'PORT': get_env_variable('POSTGRESQL_SERVICE_PORT'),
    }
