'''
Created on May 17, 2013

@author: slf
'''
from remoteAlarm.models import AlarmUser
from remoteAlarm.models import AlarmEvent
from rest_framework import serializers

class AlarmEventField(serializers.RelatedField):
    read_only = False
    
    def to_native(self, value):
        return 'Event %d: %s' % (value.order, value.event)
    

class UserSerializer(serializers.ModelSerializer):
   # all_alarm_events = AlarmEventField(many=True)
     
    class Meta:
        model = AlarmUser
        fields = ( 'phone_number', 'email','date_of_birth')

#class GroupSerializer(serializers.ModelSerializer):
#    class Meta:
#        model = Group
#        fields = ('name')

class AlarmEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlarmEvent
        fields = ('order','event','user_id')
        


    
    