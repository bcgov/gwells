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
from django.db import connection


def get_column_description(table, column):
    with connection.cursor() as cursor:
        sql = ('SELECT pgd.description '
               'FROM pg_catalog.pg_statio_all_tables as st '
               'inner join pg_catalog.pg_description pgd on (pgd.objoid=st.relid) '
               'inner join information_schema.columns c on (pgd.objsubid=c.ordinal_position '
               'and c.table_schema=st.schemaname and c.table_name=st.relname) '
               'and c.table_name = %s and c.column_name = %s;')
        cursor.execute(sql, (table, column))
        row = cursor.fetchone()
        if row:
            result = row[0]
            # logger.debug('{}.{} = {}'.format(table, column, result))
            return result
        # else:
        #     logger.warning('no match for {}.{}'.format(table, column))