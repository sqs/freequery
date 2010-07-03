from django.conf.urls.defaults import *

urlpatterns = patterns('freequery.org.search.views',
    (r'^$', 'search'),
)
