from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve',
           {'document_root': 'static/'}),
    (r'^search', include('freequery.org.search.urls')),
    (r'^$', 'freequery.org.search.views.home'),
)
