from django.contrib.auth import logout
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from gwells.settings import auth_uri
from gwells.settings import public_uri
from gwells.settings import APP_CONTEXT_ROOT

from django.http import HttpResponse
from django.views import View

class LogOutView(View):

    def get(self, request, *args, **kwargs):
        logout(request) #logout of django
        logout_uri = auth_uri + 'protocol/openid-connect/logout?redirect_uri=' + public_uri + '/' + APP_CONTEXT_ROOT
        return redirect(logout_uri) #logout of authentication server
