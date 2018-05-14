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

from ..forms import *

FORMS = [('type_and_class', ActivitySubmissionTypeAndClassForm),
         ('owner', WellOwnerForm),
         ('location', ActivitySubmissionLocationForm),
         ('gps', ActivitySubmissionGpsForm),
         ('lithology', ActivitySubmissionLithologyFormSet),
         ('casing', ActivitySubmissionCasingFormSet),
         ('surface_seal', ActivitySubmissionSurfaceSealForm),
         ('liner_perforation', ActivitySubmissionLinerPerforationFormSet),
         ('screen_intake', ActivitySubmissionScreenIntakeForm),
         ('screen', ActivitySubmissionScreenFormSet),
         ('filter_pack', ActivitySubmissionFilterPackForm),
         ('development', ActivitySubmissionDevelopmentForm),
         ('production_data', ProductionDataFormSet),
         ('water_quality', ActivitySubmissionWaterQualityForm),
         ('well_completion', WellCompletionForm),
         ('comments', ActivitySubmissionCommentForm),
        ]

TEMPLATES = {'type_and_class': 'gwells/activity_submission_form.html',
             'owner': 'gwells/activity_submission_form.html',
             'location': 'gwells/activity_submission_form.html',
             'gps': 'gwells/activity_submission_form.html',
             'lithology': 'gwells/activity_submission_lithology_form.html',
             'casing': 'gwells/activity_submission_casing_form.html',
             'surface_seal': 'gwells/activity_submission_form.html',
             'liner_perforation': 'gwells/activity_submission_liner_perforation_form.html',
             'screen_intake': 'gwells/activity_submission_form.html',
             'screen': 'gwells/activity_submission_screen_form.html',
             'filter_pack': 'gwells/activity_submission_form.html',
             'development': 'gwells/activity_submission_form.html',
             'production_data': 'gwells/activity_submission_form.html',
             'water_quality': 'gwells/activity_submission_form.html',
             'well_completion': 'gwells/activity_submission_form.html',
             'comments': 'gwells/activity_submission_form.html',
            }

from .ActivitySubmissionDetailView import ActivitySubmissionDetailView
from .ActivitySubmissionListView import ActivitySubmissionListView
from .ActivitySubmissionWizardView import ActivitySubmissionWizardView
from .HealthView import HealthView
from .RegistryView import RegistryView
from .SearchView import SearchView
from .WellDetailView import WellDetailView




__all__ = ['ActivitySubmissionDetailView', 'ActivitySubmissionListView', 'ActivitySubmissionWizardView', 'FORMS', 'HealthView', 'RegistryView', 'SearchView', 'TEMPLATES', 'WellDetailView']
