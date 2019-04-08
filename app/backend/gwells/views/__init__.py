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
import logging

from django.views.generic import TemplateView
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin
from rest_framework.generics import ListAPIView

from gwells.serializers import SurveySerializer
from gwells.models import Survey


logger = logging.getLogger(__name__)


class AuditCreateMixin(CreateModelMixin):
    """
    Adds create_user when instances are created.
    Create date is inserted in the model, and not required here.
    """

    def perform_create(self, serializer):
        if self.request.user.profile.username is None:
            raise exceptions.ValidationError(('Username must be set.'))

        logger.info('Setting create_user and update_user to {}'.format(self.request.user.profile.username))
        serializer.validated_data['create_user'] = self.request.user.profile.username
        serializer.validated_data['update_user'] = self.request.user.profile.username
        return super().perform_create(serializer)


class AuditUpdateMixin(UpdateModelMixin):
    """
    Adds update_user when instances are updated
    Update date is inserted in the model, and not required here.
    """

    def perform_update(self, serializer):
        if self.request.user.profile.username is None:
            raise exceptions.ValidationError(('Username must be set.'))

        logger.info('Setting update_user to {}'.format(self.request.user.profile_username))
        serializer.validated_data['update_user'] = self.request.user.profile.username
        return super().perform_update(serializer)


class HealthView(TemplateView):
    def health(request):
        return HttpResponse(WellActivityCode.objects.count())


class SurveyListView(ListAPIView):
    """
    get: returns a list of active surveys
    """

    serializer_class = SurveySerializer
    queryset = Survey.objects.filter(survey_enabled=True)
    pagination_class = None


class HomeView(TemplateView):
    template_name = 'gwells/gwells_spa.html'
