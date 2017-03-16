from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin

from welcome.views import index, health
from . import views

urlpatterns = [
    # Examples:
    # url(r'^$', 'project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', views.HelloWorldView.as_view()),
    url(r'^search$', views.well_search, name='search'),
    #url(r'^well/(?P<pk>[0-9]+)/$', views.WellView.as_view(), name='well'),
    url(r'^health$', health),
    url(r'^admin/', admin.site.urls),
    url(r'^test$', index),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns