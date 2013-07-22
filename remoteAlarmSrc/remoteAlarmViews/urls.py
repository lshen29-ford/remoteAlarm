'''
Created on May 13, 2013

@author: slf
'''
from django.conf.urls import patterns, url
from remoteAlarmViews import views

urlpatterns = patterns('',
    url(r'^$', views.IndexView.as_view(), name='index'),
     # ex: /remoteAlarm/5/
    url(r'^(?P<pk>\d+)/$', views.DetailView.as_view(), name='detail'),
    # ex: /remoteAlarm/5/results/
    url(r'^(?P<pk>\d+)/results/$', views.ResultsView.as_view(), name='results'),
    # ex: /remoteAlarm/5/vote/
    url(r'^(?P<poll_id>\d+)/vote/$', views.vote, name='vote'),
)