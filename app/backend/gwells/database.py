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
import os
import logging

from django.conf import settings
from gwells.settings.base import get_env_variable

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def config():
    service_name = get_env_variable('DATABASE_SERVICE_NAME', '').upper().replace('-', '_')
    name = get_env_variable('DATABASE_NAME')

    # logger.info(f'Django Database Config')
    # logger.info(f'service_name: ', service_name[0])
    # logger.info(f'database_name: ', name[0])

    # return {
    #     'ENGINE': 'django.contrib.gis.db.backends.postgis',
    #     'NAME': name,
    #     'USER': get_env_variable('DATABASE_USER'),
    #     'PASSWORD': get_env_variable('DATABASE_PASSWORD'),
    #     'HOST': get_env_variable('{}_SERVICE_HOST'.format(service_name)),
    #     'PORT': get_env_variable('{}_SERVICE_PORT'.format(service_name)),
    # }
    
    return {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': os.getenv('DATABASE_NAME'),
        'USER': os.getenv('DATABASE_USER'),
        'PASSWORD': os.getenv('DATABASE_PASSWORD'),
        'HOST': os.getenv('DATABASE_SERVICE_NAME'),
        'PORT': os.getenv('DATABASE_PORT')
    }
