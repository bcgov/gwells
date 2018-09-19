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
# TODO: Delete this file once Submissions has been completed using Vue.js
from django import forms
from django.forms.models import inlineformset_factory

from .ActivitySubmissionCommentForm import ActivitySubmissionCommentForm
from .ActivitySubmissionDevelopmentForm import ActivitySubmissionDevelopmentForm
from .ActivitySubmissionFilterPackForm import ActivitySubmissionFilterPackForm
from .ActivitySubmissionGpsForm import ActivitySubmissionGpsForm
from .ActivitySubmissionLocationForm import ActivitySubmissionLocationForm
from .ActivitySubmissionScreenIntakeForm import ActivitySubmissionScreenIntakeForm
from .ActivitySubmissionSurfaceSealForm import ActivitySubmissionSurfaceSealForm
from .ActivitySubmissionTypeAndClassForm import ActivitySubmissionTypeAndClassForm
from .ActivitySubmissionWaterQualityForm import ActivitySubmissionWaterQualityForm
from .CasingForm import CasingForm
from .LinerPerforationForm import LinerPerforationForm
from .LithologyForm import LithologyForm
from .ProductionDataForm import ProductionDataForm
from .ScreenForm import ScreenForm
from .SearchForm import SearchForm
from .WellCompletionForm import WellCompletionForm
from .WellOwnerForm import WellOwnerForm

from wells.models import ActivitySubmission, LithologyDescription, Casing, LinerPerforation, Screen,\
    ProductionData


ActivitySubmissionLithologyFormSet = inlineformset_factory(
    ActivitySubmission, LithologyDescription, form=LithologyForm, fk_name='activity_submission',
    can_delete=False, extra=10)
ActivitySubmissionCasingFormSet = inlineformset_factory(
    ActivitySubmission, Casing, form=CasingForm, fk_name='activity_submission', can_delete=False, extra=5)
ActivitySubmissionLinerPerforationFormSet = inlineformset_factory(
    ActivitySubmission, LinerPerforation, form=LinerPerforationForm, fk_name='activity_submission',
    can_delete=False, extra=5)
ActivitySubmissionScreenFormSet = inlineformset_factory(
    ActivitySubmission, Screen, form=ScreenForm, fk_name='activity_submission', can_delete=False, extra=5)
ProductionDataFormSet = inlineformset_factory(
    ActivitySubmission, ProductionData, form=ProductionDataForm, fk_name='activity_submission',
    can_delete=True, min_num=1, max_num=1)
