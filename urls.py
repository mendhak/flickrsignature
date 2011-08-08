from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^(?i)img/(?P<nsid>[A-Za-z0-9@]+)/?(?P<num>[0-9]+)?/?(?P<size>[A-Za-z0-9-]+)?/?', 'flickr.views.image'),
    url(r'^(?i)url/(?P<nsid>[A-Za-z0-9@]+)/?(?P<num>[0-9]+)?', 'flickr.views.redirect'),
    url(r'^(?i)nsid/(?P<username>.+)', 'flickr.views.nsid'),

    # url(r'^easyflickrurl/', include('easyflickrurl.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
