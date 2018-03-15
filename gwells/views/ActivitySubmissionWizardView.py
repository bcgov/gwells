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

from formtools.wizard.views import SessionWizardView

from ..models import *
from ..views import ActivitySubmissionDetailView
from ..views import TEMPLATES

class ActivitySubmissionWizardView(SessionWizardView):
    instance = None

    def get_context_data(self, **kwargs):
        """
        Return the context for the page.
        """
        context = super(ActivitySubmissionWizardView, self).get_context_data(**kwargs)
        return context

    def get_template_names(self):
        return [TEMPLATES[self.steps.current]]

    def get_context_data(self, form, **kwargs):
        context = super(ActivitySubmissionWizardView, self).get_context_data(form=form, **kwargs)
        context['wizard_data'] = self.get_all_cleaned_data()

        if self.steps.current == 'type_and_class' and not 'water_supply_well_class_code' in context:
            # Get the pk of water supply well class so jquery can show/hide intended water use field
            try:
                water_supply_class = WellClassCode.objects.get(code='WATR_SPPLY')
                context['water_supply_well_class_code'] = water_supply_class.well_class_code
            except Exception as e:
                context['water_supply_well_class_code'] = None
        return context

    def get_form_instance(self, step):
        if self.instance is None:
            self.instance = ActivitySubmission()
        return self.instance

    def get_form_initial(self, step):
        initial = {}

        if step == 'surface_seal':
            # Determine if casing exists so surface seal fields can be validated as required in their clean methods
            casing_data = self.get_cleaned_data_for_step('casing')
            initial.update({'casing_exists': False})
            if casing_data:
                for casing in casing_data:
                    if casing:
                        initial.update({'casing_exists': True})
                        break
        elif step == 'screen':
            # Make at least 1 row of screen required if Screen Intake == Screen on the previous step
            intake_data = self.get_cleaned_data_for_step('screen_intake')
            form_class = self.form_list[step]
            form_class.min_num = 0
            if intake_data and intake_data.get('screen_intake'):
                try:
                    screen_screen_intake = ScreenIntake.objects.get(code='SCREEN')
                except Exception as e:
                    screen_screen_intake = None
                if intake_data.get('screen_intake') == screen_screen_intake:
                    form_class.min_num = 1
        elif step == 'well_completion':
            # Determine well class to decide which fields are required
            initial.update({'well_class_code': ''})
            type_and_class_data = self.get_cleaned_data_for_step('type_and_class')
            if type_and_class_data and type_and_class_data.get('well_class'):
                initial.update({'well_class_code': type_and_class_data.get('well_class').code})

        return initial

    def done(self, form_list, form_dict, **kwargs):
        submission = self.instance
        cleaned_data = self.get_all_cleaned_data()
        characteristics_data = cleaned_data.pop('water_quality_characteristics')

        if submission.well_activity_type.well_activity_code == 'CON' and not submission.well:
            #TODO
            w = submission.create_well()
            w.save()
            submission.well = w
            submission.save()
            lithology_list = form_dict['lithology'].save()
            lithology_list = list(lithology_list)
            for lith in lithology_list:
                lith.pk = None
                lith.activity_submission = None
                lith.well = w
                lith.save()
            casing_list = form_dict['casing'].save()
            casing_list = list(casing_list)
            for casing in casing_list:
                casing.pk = None
                casing.activity_submission = None
                casing.well = w
                casing.save()
            perforation_list = form_dict['liner_perforation'].save()
            perforation_list = list(perforation_list)
            for perforation in perforation_list:
                perforation.pk = None
                perforation.activity_submission = None
                perforation.well = w
                perforation.save()
            screen_list = form_dict['screen'].save()
            screen_list = list(screen_list)
            for screen in screen_list:
                screen.pk = None
                screen.activity_submission = None
                screen.well = w
                screen.save()
            production_list = form_dict['production_data'].save()
            production_list = list(production_list)
            for production in production_list:
                production.pk = None
                production.activity_submission = None
                production.well = w
                production.save()
            for characteristic in characteristics_data:
                submission.water_quality_characteristics.add(characteristic)
                w.water_quality_characteristics.add(characteristic)
        else:
            submission.save()
            lithology_list = form_dict['lithology'].save()
            casing_list = form_dict['casing'].save()
            perforation_list = form_dict['liner_perforation'].save()
            screen_list = form_dict['screen'].save()
            production_list = form_dict['production_data'].save()
            for characteristic in characteristics_data:
                submission.water_quality_characteristics.add(characteristic)

        return HttpResponseRedirect('/submission/')
