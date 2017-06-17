from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin

from welcome.views import index, health
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    # Examples:
    # url(r'^$', 'project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', views.HelloWorldView.as_view(), name='home'),
    url(r'^search$', views.well_search, name='search'),
    #url(r'^(?P<pk>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})/$', views.DetailView.as_view(), name='detail'),
    url(r'^submission/$', views.ActivitySubmissionListView.as_view(), name='activity_submission_list'),
    url(r'^submission/create$', views.ActivitySubmissionWizardView.as_view(views.FORMS), name='activity_submission_create'),
    url(r'^submission/(?P<pk>[0-9]+)$', views.ActivitySubmissionDetailView.as_view(), name='activity_submission_detail'),
    url(r'^well/(?P<pk>[0-9]+)$', views.WellDetailView.as_view(), name='well_detail'),
    url(r'^health$', health),
    url(r'^admin/', admin.site.urls),
    url(r'^additional-information', TemplateView.as_view(template_name='gwells/additional_information.html'), name='additional_information'),
    url(r'^test$', index),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns