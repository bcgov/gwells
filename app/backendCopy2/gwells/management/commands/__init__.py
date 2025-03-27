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


# Idea from: https://github.com/ActiveState/code
def ResultIter(cursor, arraysize=10000):
    while True:
        # cursor.fetchone(), suprisingly goes in the backround, and fetches everything.
        # cursor.fetchall(), obviously goes in the background, and fetches everything.
        # If we fetch everything at once, we may exceed the memory available - fetching in smaller
        # chunks allows us to not exceed memory, and to allow for streaming results.
        results = cursor.fetchmany(arraysize)
        if not results:
            break
        for result in results:
            yield result
