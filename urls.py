from django.conf.urls.defaults import patterns, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^(?i)img/(?P<nsid>[A-Za-z0-9@]+)/?(?P<num>[0-9]+)?/?(?P<size>[A-Za-z0-9-]+)?/?(?P<popular>[p]{1})?', 'flickr.views.image'),
    url(r'^(?i)url/(?P<nsid>[A-Za-z0-9@]+)/?(?P<num>[0-9]+)?/?(?P<popular>[p]{1})?', 'flickr.views.redirect'),
    url(r'^(?i)searchimg/(?P<tags>[A-Za-z0-9-]+)/(?P<num>[0-9]+)/?(?P<size>[A-Za-z0-9-]+)?/?(?P<nsid>[A-Za-z0-9@]+)?', 'flickr.views.searchImage'),
    url(r'^(?i)searchurl/(?P<tags>[A-Za-z0-9-]+)/(?P<num>[0-9]+)/?(?P<nsid>[A-Za-z0-9@]+)?', 'flickr.views.searchRedirect'),
    url(r'^(?i)nsid/(?P<username>.+)', 'flickr.views.nsid'),
    url(r'^signatures$', 'flickr.views.main')

    # url(r'^easyflickrurl/', include('easyflickrurl.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)


if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.STATIC_ROOT,
        }),
    )

