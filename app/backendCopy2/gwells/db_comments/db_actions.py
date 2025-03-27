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

    This code courtesy of Transportation Fuels Reporting System (https://github.com/bcgov/tfrs),
    originally written by Robert Johnstone (https://github.com/plasticviking)
"""
import importlib
import inspect
import logging
from collections import namedtuple

from django.db import connection, ProgrammingError

logger = logging.getLogger(__name__)

_exception_message = 'Caught a database exception while updating comments. ' \
                     'If you are reverting a migration, you can ignore this safely.'


def create_db_comments(table_name, table_comment, column_comments=None):
    """Populate comments for non-model tables (like Django-specific tables)"""

    with connection.cursor() as cursor:
        try:
            # logger.info('comment on table "{}" is "{}"'.format(table_name, table_comment))
            cursor.execute(
                'comment on table "{}" is %s'.format(table_name), [table_comment]
            )
        except ProgrammingError:
            logger.error(_exception_message)

        if column_comments is not None:
            for column, comment in column_comments.items():
                try:
                    # logger.info('comment on column "{}"."{}" is "{}"'.format(table_name, column, comment))
                    cursor.execute(
                        'comment on column "{}"."{}" is %s'.format(table_name, column), [comment]
                    )
                except ProgrammingError as e:
                    logger.error('{} -- {}'.format(_exception_message, e))


def create_db_comments_from_models(models):
    """Populate comments for model tables"""

    with connection.cursor() as cursor:
        for model_class in models:
            # Doing the check for abstract is a bit weird, we have to create an instance of the class, we
            # can't check it on the class definition.
            if model_class()._meta.abstract:
                # If it's an abstract class, don't proceed.
                continue

            table = model_class.db_table_name() \
                if hasattr(model_class, 'db_table_name') else None
            table_comment = model_class.db_table_comment \
                if hasattr(model_class, 'db_table_comment') else None
            column_comments = model_class.db_column_comments() \
                if hasattr(model_class, 'db_column_comments') else None

            if table is None and table_comment is not None:
                raise Exception('Missing db_table_name method on %s' % model_class.__name__)

            if table_comment is not None:
                try:
                    # logger.info('comment on table "{}" is "{}"'.format(table, table_comment))
                    cursor.execute(
                        'comment on table "{}" is %s'.format(table), [table_comment]
                    )
                except ProgrammingError as e:
                    logger.error('{} -- {}'.format(_exception_message, e))

            if column_comments is not None:
                for column, comment in column_comments.items():
                    try:
                        if comment is not None:
                            # logger.info('comment on column "{}"."{}" is "{}"'.format(table, column, comment))
                            cursor.execute(
                                'comment on column "{}"."{}" is %s'.format(table, column), [comment]
                            )
                    except ProgrammingError as e:
                        logger.error('{} -- {}'.format(_exception_message, e))


def get_all_model_classes(model_module_name):
    """
    Get all the model classes in specified module.
    """

    module = importlib.import_module(model_module_name)

    classes = set()

    for name, obj in inspect.getmembers(module):
        if inspect.getmodule(obj) is not None \
                and inspect.getmodule(obj).__name__.startswith(model_module_name):
            # Assume anything with a 'Meta' attribute is a model
            if inspect.isclass(obj) and hasattr(obj, '_meta'):
                classes.add(obj)

    return classes
