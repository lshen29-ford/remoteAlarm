from django.db import models
from datetime import datetime
from django.conf import settings
from remoteAlarm.managers import AlarmUserManager
from django.contrib.auth.models import (
     AbstractBaseUser
)
# Create your models here.





class AlarmUser(AbstractBaseUser):
    
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
        db_index=True,
    )
    date_of_birth = models.DateField()
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    phone_number=models.CharField(max_length=10);

    objects = AlarmUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['date_of_birth']
    

    
    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __unicode__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True
        

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

class AlarmEvent(models.Model):
  #  user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='all_alarm_events')
    event = models.CharField(max_length=100)
    order = models.IntegerField(max_length=10)
    user_id = models.IntegerField(max_length=10)
    
    EQUIRED_FIELDS = ['user_id']
    
    def __unicode__(self):
        return '%d: %s' % (self.order, self.event)
    
class Poll(models.Model):
    question = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    
    def __unicode__(self):
        return self.question
    # ...
    def was_published_today(self):
        return self.pub_date.date() == datetime.date.today()
    
    def was_published_recently(self):
        return self.pub_date >= datetime.astimezone().now() - datetime.timedelta(days=1)
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

class Choice(models.Model):
    poll = models.ForeignKey(Poll)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __unicode__(self):
        return self.choice_text