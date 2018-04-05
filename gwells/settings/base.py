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
from os import getenv
import logging

from django.core.exceptions import ImproperlyConfigured

logger = logging.getLogger('gwells.settings.base')


# By default, we want to enforce environment variables to be set
ENFORCE_ENV_VARIABLES = getenv('ENFORCE_ENV_VARIABLES', 'True') == 'True'
if not ENFORCE_ENV_VARIABLES:
    logger.warn('ENFORCE_ENV_VARIABLE is set to False')


def get_env_variable(var_name, default_value=None):
    result = getenv(var_name)
    if not result:
        msg = 'Set the {} environment variable'.format(var_name)
        if ENFORCE_ENV_VARIABLES:
            raise ImproperlyConfigured(msg)
        else:
            logger.debug(msg)
            result = default_value
    return result
