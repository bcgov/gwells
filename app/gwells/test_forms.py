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

from .forms import *
from django.test import TestCase

#TODO split tests into one file per class

class FormsTestCase(TestCase):

    def test_activity_submission_comment_form_instantiation(self):
        activity_submission_comment_form = ActivitySubmissionCommentForm()
        self.assertIsInstance(activity_submission_comment_form, ActivitySubmissionCommentForm)

    def test_activity_submission_development_form_instantiation(self):
        test_activity_submission_development_form = ActivitySubmissionDevelopmentForm()
        self.assertIsInstance(test_activity_submission_development_form, ActivitySubmissionDevelopmentForm)

    def test_activity_submission_filter_pack_form_instantiation(self):
        activity_submission_filter_pack_form = ActivitySubmissionFilterPackForm()
        self.assertIsInstance(activity_submission_filter_pack_form, ActivitySubmissionFilterPackForm)

    def test_activity_submission_gps_form_instantiation(self):
        activity_submission_gps_form = ActivitySubmissionGpsForm()
        self.assertIsInstance(activity_submission_gps_form, ActivitySubmissionGpsForm)

    def test_activity_submission_location_form_instantiation(self):
        activity_submission_location_form = ActivitySubmissionLocationForm()
        self.assertIsInstance(activity_submission_location_form, ActivitySubmissionLocationForm)

    def test_activity_submission_screen_intake_form_instantiation(self):
        activity_submission_screen_intake_form = ActivitySubmissionScreenIntakeForm()
        self.assertIsInstance(activity_submission_screen_intake_form,ActivitySubmissionScreenIntakeForm)

    def test_activity_submission_surface_seal_form_instantiation(self):
        activity_submission_surface_seal_form = ActivitySubmissionSurfaceSealForm()
        self.assertIsInstance(activity_submission_surface_seal_form, ActivitySubmissionSurfaceSealForm)

    def test_activity_submission_type_and_class_form_instantiation(self):
        activity_submission_type_and_class_form = ActivitySubmissionTypeAndClassForm()
        self.assertIsInstance(activity_submission_type_and_class_form, ActivitySubmissionTypeAndClassForm)

    def test_activity_submission_water_quality_form_instantiation(self):
        test_activity_submission_water_quality_form = ActivitySubmissionWaterQualityForm()
        self.assertIsInstance(test_activity_submission_water_quality_form, ActivitySubmissionWaterQualityForm)

    def test_casing_form_instantiation(self):
        casing_form = CasingForm()
        self.assertIsInstance(casing_form, CasingForm)

    def test_liner_perforation_form_instantiation(self):
        liner_perforation_form = LinerPerforationForm()
        self.assertIsInstance(liner_perforation_form, LinerPerforationForm)

    def test_lithology_form_instantiation(self):
        lithology_form = LithologyForm()
        self.assertIsInstance(lithology_form, LithologyForm)

    def test_production_data_form_instantiation(self):
        production_data_form = ProductionDataForm()
        self.assertIsInstance(production_data_form, ProductionDataForm)

    def test_screen_form_instantiation(self):
        screen_form = ScreenForm()
        self.assertIsInstance(screen_form, ScreenForm)

    def test_search_form_instantiation(self):
        search_form = SearchForm()
        self.assertIsInstance(search_form, SearchForm)

    def test_well_completion_form_instantiation(self):

        well_completion_form = WellCompletionForm(initial={'well_class_code':None})
        self.assertIsInstance(well_completion_form, WellCompletionForm)

    def test_well_owner_form_instantiation(self):
        well_owner_form = WellOwnerForm()
        self.assertIsInstance(well_owner_form, WellOwnerForm)
