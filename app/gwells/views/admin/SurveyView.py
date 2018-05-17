from django.views.generic import View
from gwells.models.Survey import Survey
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.shortcuts import redirect
from django.template import loader
from django.http import HttpResponse
from django.http import HttpResponseNotAllowed
from django.http import HttpResponseNotFound
from django.http import HttpResponseServerError
import uuid
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.core.exceptions import PermissionDenied

from django.contrib.auth.models import Permission
from django.contrib.auth.models import Group

def get_handler_method(request_handler, http_method):

    try:
        handler_method = getattr(request_handler, http_method.lower())

        if callable(handler_method):
            return handler_method

    except AttributeError:
        pass

class SurveyView(LoginRequiredMixin, View):

    login_url = reverse_lazy('admin:login')
    model = Survey

    fields = ['survey_introduction_text', 'survey_link', 'survey_page', 'survey_enabled']

    http_methods = ['GET', 'POST', 'HEAD', 'PUT', 'DELETE', 'OPTIONS', 'TRACE']

    def dispatch(self, request, *args, **kwargs):

        #ensure that there is a user whose authentication can be validated
        if not hasattr(request, 'user'):
            self.request = request
            return self.handle_no_permission()

        #LoginRequired
        if not request.user.is_authenticated:
            self.request = request
            return self.handle_no_permission()

        user_groups = Group.objects.filter(user=request.user)
        admin_group = Group.objects.get(name='admin')

        if not admin_group in user_groups:
            if self.raise_exception or self.request.user.is_authenticated:
                raise PermissionDenied("Prermission Denied")
            return redirect_to_login(self.request.get_full_path(), self.get_login_url(), self.get_redirect_field_name())

        request_handler = self

        _method = request.POST.get('_method')

        if _method == None:
            _method = request.method

        if _method != None:
            if _method.upper() in SurveyView.http_methods:
                handler_method = get_handler_method(request_handler, _method.upper())

                if handler_method:
                    return handler_method(request, *args, **kwargs)
            else:
                methods = [method for method in http_methods if get_handler_method(request_handler, _method)]
                if len(methods) > 0:
                    return HttpResponseNotAllowed(methods)
                else:
                    return HttpResponseServerError("Invalid method")

    def add_prefix(self, name, form_number):
        return 'form-' + str(form_number) + '-' + name

    def alter_fields_for_post(self, fields, form_number):
        for key in fields:
            fields[key]=self.add_prefix(fields[key], form_number)

    def __create_or_update_survey(self, request, method, form_number=0, **kwargs):

        form_fields = {'SURVEY_INTRODUCTION_TEXT':'survey_introduction_text',
                  'SURVEY_PAGE':'survey_page',
                  'SURVEY_LINK':'survey_link',
                  'SURVEY_ENABLED':'survey_enabled'}

        if method.upper()=='PUT':
            fields = {'PUT':request.PUT}
            survey = Survey()
        elif method.upper() == 'POST':
            fields = {'POST':request.POST}
            form_fields['SURVEY_GUID'] = 'survey_guid'
            self.alter_fields_for_post(form_fields, form_number)
            survey = Survey.objects.get(pk=fields[method].get(form_fields['SURVEY_GUID']))
        else:
            return HttpResponseNotAllowed(methods)

        survey.survey_introduction_text = fields[method].get(form_fields['SURVEY_INTRODUCTION_TEXT'])
        survey.survey_page = fields[method].get(form_fields['SURVEY_PAGE'])
        survey.survey_link = fields[method].get(form_fields['SURVEY_LINK'])

        enabled = fields[method].get(form_fields['SURVEY_ENABLED'])

        if enabled == None or enabled == False:
            enabled = False
        elif enabled == 'on':
            enabled = True

        survey.survey_enabled = enabled

        survey.save()

    def get(self, request, **kwargs):

        template = loader.get_template('gwells/survey_detail.html')

        uri = request.build_absolute_uri()
        survey_guid = uri.rsplit('/', 1)[1]
        survey_guid = uuid.UUID(hex=survey_guid) #type conversion

        survey = Survey.objects.get(pk=survey_guid)
        context = {'survey': survey, }

        return HttpResponse(template.render(context, request))

    def put(self, request, **kwargs):
        self.__create_or_update_survey(request, 'PUT')
        return redirect(reverse('site_admin'))

    def post(self, request, **kwargs):
        form_number = request.POST.get('form-number')

        if form_number==None:
            return HttpResponseNotFound('<h1>No survey specified - id required</h1>')

        form_number = int(form_number)
        self.__create_or_update_survey(request, 'POST', form_number)

        return redirect(reverse('site_admin'))

    def delete(self, request, **kwargs):
        form_number = request.POST.get('form-number')
        form_number = int(form_number)
        field_name = self.add_prefix('survey_guid', form_number)

        survey_guid = request.POST.get(field_name)
        survey = Survey.objects.get(pk=survey_guid)
        survey.delete()

        return redirect(reverse('site_admin'))
