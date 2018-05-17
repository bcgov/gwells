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


# TODO: By default, we want to enforce environment variables to be set. In order to smoothly introduce
# strict environmental variable checking, we are currently defauling to 'False'. Once issues in the build
# pipeline are resolved, change code below to:
# REQUIRE_ENV_VARIABLES = getenv('REQUIRE_ENV_VARIABLES', 'True') == 'True'
REQUIRE_ENV_VARIABLES = getenv('REQUIRE_ENV_VARIABLES', 'False') == 'True'
if not REQUIRE_ENV_VARIABLES:
    logger.warn('REQUIRE_ENV_VARIABLES is set to False')


def get_env_variable(var_name, default_value=None, strict=False):
    """ Returns the environment variable specified in :var_name:, or uses the :default_value: specified

    :param var_name: The name of the environment variable.
    :param default_value: The desired default value to use if the environment variable is not set.
    :param strict: When set to True, and REQUIRE_ENV_VARIABLES is set to True, throw an exception.
    """
    result = getenv(var_name)
    if not result:
        # If there's no environment variable, we fail over to using the default value, if specified,
        # unless we're in "REQUIRE_ENV_VARIABLES"
        msg = 'Environment variable "{}" not set'.format(var_name)
        if strict and REQUIRE_ENV_VARIABLES:
            # Default values are NOT acceptable, we raise an exception.
            raise ImproperlyConfigured(msg)
        else:
            # Default values may be used, but will result in a warning message.
            result = default_value
            logger.warn(msg)
    return result
