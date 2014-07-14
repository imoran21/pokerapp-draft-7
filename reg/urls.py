from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'reg.views.home', name='home'),
    url(r'^login/', 'reg.views.login_view', name='login_view'),
    url(r'^logout/', 'reg.views.logout_view', name='logout_view'),
    url(r'^register/', 'reg.views.register_view', name='register_view'),

    url(r'^admin/', include(admin.site.urls)),
)
