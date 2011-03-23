from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('',
    url('^endpoint/', 'salmon.views.endpoint', name='salmon_endpoint'),
)
