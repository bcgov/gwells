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

from django.views import generic

class AdminView(generic.TemplateView):
    template_name = 'gwells/admin.html'

    def get_context_data(self, **kwargs):
        """
        Return the context for the page.
        """
        context = super(AdminView, self).get_context_data(**kwargs)
        return context
