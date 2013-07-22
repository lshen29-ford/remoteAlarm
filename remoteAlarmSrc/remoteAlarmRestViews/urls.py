'''
Created on May 18, 2013

@author: slf
'''
from django.conf.urls import patterns, url, include
from rest_framework import routers
from remoteAlarmRestViews import restfulviews


user_list = restfulviews.UserViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

user_detail = restfulviews.UserViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

alarm_event_list = restfulviews.AlarmEventViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

alarm_event_detail = restfulviews.AlarmEventViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

alarm_event_list_query = restfulviews.AlarmEventViewSet.as_view({
    'get': 'listByUserId'
})


router = routers.DefaultRouter()
router.register(r'users', restfulviews.UserViewSet)
router.register(r'events', restfulviews.AlarmEventViewSet)
#router.register(r'groups', restfulviews.GroupViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browseable API.
urlpatterns = patterns('',
    url(r'^', include(router.urls)),
    url(r'^users/$', user_list, name='user_list'),
    url(r'^users/(?P<pk>[0-9]+)/$', user_detail, name='user_detail'),

    url(r'^events/$', alarm_event_list, name='alarm_event_list'),
    url(r'^events/(?P<pk>[0-9]+)/$', alarm_event_detail, name='alarm_event_detail'),
    url(r'^events/(?P<user_id>[0-9]+)/listByUserId/$', alarm_event_list_query, name='alarm_event_list_query'),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
)