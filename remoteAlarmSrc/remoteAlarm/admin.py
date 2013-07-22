'''
Created on May 8, 2013

@author: slf
'''
from django import forms
from django.contrib import admin
from remoteAlarm.models import Choice
from remoteAlarm.models import Poll
from remoteAlarm.models import AlarmEvent
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from remoteAlarm.models import AlarmUser

class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = AlarmUser
        fields = ('email', 'date_of_birth','last_login')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = AlarmUser
        fields = ['email', 'password', 'date_of_birth', 'is_active', 'is_admin','last_login','phone_number']

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class AlarmUserAdmin(UserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'date_of_birth', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('date_of_birth',)}),
        ('Permissions', {'fields': ('is_admin',)}),
        ('Important dates', {'fields': ('last_login',)}),
        ('phone number', {'fields': ('phone_number',)}),  
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'date_of_birth', 'password1', 'password2','phone_number')
            }
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

# Now register the new UserAdmin...
admin.site.register(AlarmUser, AlarmUserAdmin)
# ... and, since we're not using Django's builtin permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)



class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 3
    
class PollAdmin(admin.ModelAdmin):
    fieldsets = [
                 (None,               {'fields': ['question']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]
    list_filter = ['pub_date']
    
# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class AlarmInline(admin.StackedInline):
    model = AlarmEvent
    can_delete = False
    verbose_name_plural = 'alarm'


    
# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
#class UserProfileInline(admin.StackedInline):
#    model = UserProfile
#    can_delete = False
#    verbose_name_plural = 'userProfile'

# Define a new User admin
class UserEventAdmin(AlarmUserAdmin):
    inlines = (AlarmInline,)
    

# Re-register UserAdmin
admin.site.unregister(AlarmUser)
admin.site.register(AlarmUser, UserEventAdmin)

admin.site.register(Poll,PollAdmin)
admin.site.register(Choice)