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

from ..models import *

from django import forms
from django.forms.models import inlineformset_factory

ActivitySubmissionLithologyFormSet = inlineformset_factory(ActivitySubmission, LithologyDescription, form=LithologyForm, fk_name='activity_submission', can_delete=False, extra=10)
ActivitySubmissionCasingFormSet = inlineformset_factory(ActivitySubmission, Casing, form=CasingForm, fk_name='activity_submission', can_delete=False, extra=5)
ActivitySubmissionLinerPerforationFormSet = inlineformset_factory(ActivitySubmission, LinerPerforation, form=LinerPerforationForm, fk_name='activity_submission', can_delete=False, extra=5)
ActivitySubmissionScreenFormSet = inlineformset_factory(ActivitySubmission, Screen, form=ScreenForm, fk_name='activity_submission', can_delete=False, extra=5)
ProductionDataFormSet = inlineformset_factory(ActivitySubmission, ProductionData, form=ProductionDataForm, fk_name='activity_submission', can_delete=True, min_num=1, max_num=1)

__all__ = ['ActivitySubmissionCasingFormSet',
           'ActivitySubmissionCommentForm',
           'ActivitySubmissionDevelopmentForm',
           'ActivitySubmissionLinerPerforationFormSet',
           'ActivitySubmissionGpsForm',
           'ActivitySubmissionFilterPackForm',
           'ActivitySubmissionLithologyFormSet',
           'ActivitySubmissionLocationForm',
           'ActivitySubmissionScreenFormSet',
           'ActivitySubmissionScreenIntakeForm',
           'ActivitySubmissionSurfaceSealForm',
           'ActivitySubmissionTypeAndClassForm',
           'ActivitySubmissionWaterQualityForm',
           'CasingForm',
           'LinerPerforationForm',
           'LithologyForm',
           'ProductionDataForm',
           'ProductionDataFormSet',
           'ScreenForm',
           'SearchForm',
           'WellCompletionForm',
           'WellOwnerForm']
