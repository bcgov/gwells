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
from django.contrib import admin


# Import all models
from .models import (
    Survey,
    OnlineSurvey,
    Profile,
    ProvinceStateCode
)

class SurveyAdmin(admin.ModelAdmin):
    pass

class OnlineSurveyAdmin(admin.ModelAdmin):
    date_hierarchy = 'effective_date'
    empty_value_display = '- No Online Surveys defined -'
    radio_fields = {"survey_page": admin.HORIZONTAL}
    admin.save_as = True
    admin.save_on_top = True

# Register your models here.
admin.site.register(Survey, SurveyAdmin)
admin.site.register(OnlineSurvey, OnlineSurveyAdmin)
admin.site.register(Profile)
admin.site.register(ProvinceStateCode)
