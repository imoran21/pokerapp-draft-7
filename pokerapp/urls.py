from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'pokerapp.views.home', name='home'),
    url(r'^enter_table/', 'pokerapp.views.enter_table', name='enter_table'),
    url(r'^end_table/', 'pokerapp.views.end_table', name='end_table'),
    url(r'^end_game/', 'pokerapp.views.end_game', name='end_game'),
    url(r'^create_table/', 'pokerapp.views.create_table', name='create_table'),
    url(r'^leave_table/', 'pokerapp.views.leave_table', name='leave_table'),
    url(r'^view_table/', 'pokerapp.views.view_table', name='view_table'),
    url(r'^start_game/', 'pokerapp.views.start_game', name='start_game'),
    url(r'^call/', 'pokerapp.views.call', name='call'),
    url(r'^fold/', 'pokerapp.views.fold', name='fold'),

)
