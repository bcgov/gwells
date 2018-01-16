from .ActivitySubmissionDetailView import ActivitySubmissionDetailView
from .HealthView import HealthView
from .RegistryView import RegistryView
from .SearchView import SearchView
from .WellDetailView import WellDetailView
from ..forms import *

__all__ = ['ActivitySubmissionDetailView', 'FORMS', 'HealthView', 'RegistryView', 'SearchView', 'TEMPLATES', 'WellDetailView']

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
