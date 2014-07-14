from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'pokerapp.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^reg/', include('reg.urls')), 
    url(r'^pokerapp/', include('pokerapp.urls')), 
    url(r'^admin/', include(admin.site.urls)),
)
