'''
Created on May 17, 2013

@author: slf
'''


from rest_framework import viewsets
from remoteAlarmRestViews.serializers import UserSerializer #GroupSerializer
from remoteAlarm.models import AlarmUser
from remoteAlarm.models import AlarmEvent
from remoteAlarmRestViews.serializers import AlarmEventSerializer
from rest_framework.response import Response
# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = AlarmUser.objects.all()
    serializer_class = UserSerializer
    
# ViewSets define the view behavior.
class AlarmEventViewSet(viewsets.ModelViewSet):
    queryset = AlarmEvent.objects.all()
    serializer_class = AlarmEventSerializer

    def listByUserId(self, request,user_id=None):
        eventqueryset= AlarmEvent.objects.filter(user_id=user_id)
        serializer = AlarmEventSerializer(eventqueryset, many=True)
        return Response(serializer.data)


    


#class GroupViewSet(viewsets.ModelViewSet):
 #   queryset = Group.objects.all()
  #  serializer_class = GroupSerializer
