from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

# Register your models here.


class ModelAttributes(admin.ModelAdmin):
    # ! We use this to hide our data from django-admin. No one will edit this one but can view it.
    model = UserDataCredentials
    exclude = ('Classroom_CompleteString', 'Section_CompleteStringGroup')
    #list_display = ()  # Contain only fields in your `custom-user-model`
    #list_filter = ()  # Contain only fields in your `custom-user-model` intended for filtering. Do not include `groups`since you do not have it
    #search_fields = ()  # Contain only fields in your `custom-user-model` intended for searching
    #ordering = ()  # Contain only fields in your `custom-user-model` intended to ordering
    #filter_horizontal = () # Leave it empty. You have neither `groups` or `user_permissions`
    #fieldsets = UserAdmin.fieldsets + (
    #        (None, {'fields': ('mobile',)}),
    #)

class UserClassAttributes(UserAdmin):
    pass

admin.site.register((Classroom,
                     Course,
                     SectionGroup,
                     ProgramBranch,
                     CourseSchedule,
                     ClassroomActionLog
                     ), ModelAttributes)

admin.site.register(UserDataCredentials, UserClassAttributes)