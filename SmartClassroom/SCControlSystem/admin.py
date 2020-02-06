from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

# Register your models here.


class ModelAttributes(admin.ModelAdmin):
    # ! We use this to hide our data from django-admin. No one will edit this one but can view it.
    model = UserDataCredentials
    exclude = ('Classroom_CompleteString', 'Section_CompleteStringGroup')
    # list_filter = ()  # Contain only fields in your `custom-user-model` intended for filtering. Do not include `groups`since you do not have it
    # search_fields = ()  # Contain only fields in your `custom-user-model` intended for searching
    # ordering = ()  # Contain only fields in your `custom-user-model` intended to ordering
    # filter_horizontal = () # Leave it empty. You have neither `groups` or `user_permissions`
    # fieldsets = UserAdmin.fieldsets + (
    #        (None, {'fields': ('mobile',)}),
    # )


class UserClassAttributes(UserAdmin):
    model = UserDataCredentials # ! A Model or DB to reference at.

    """
        Types of Features in DJango-Admin
        List_Display makes you able to display their content by referencing a particular field.
        List_Filter is a feature exclusive based on referenced field. In short, you can filter on **that** field.

    """
    list_display = ('first_name', 'Middle_Name', 'last_name', 'User_Role', 'is_active' ,'is_staff', 'is_superuser', 'date_joined',)  # Contain only fields in your `custom-user-model`
    list_filter = ('first_name', 'Middle_Name', 'last_name', 'User_Role', 'is_active' ,'is_staff', 'is_superuser', 'date_joined',)  # Contain only fields in your `custom-user-model`
    search_fields = ('first_name', 'Middle_Name', 'last_name', 'User_Role', 'is_active' ,'is_staff', 'is_superuser', 'date_joined',)  # Contain only fields in your `custom-user-model`

    # ! Fieldsets is container that contains fields that can be read / modified.
    # * The reason why we did UserAdmin.fieldsets + because we just want to have additional items.
    # ! The default ones will be retained.

    fieldsets = UserAdmin.fieldsets + (
        ('Security Unique Assets', {
            'fields': ('Common_ID', 'Unique_ID'),
            }
        ),
        ('Additional Personal info', {
            'fields': ('Middle_Name', 'User_Role'),
            }
        ),
    )
    readonly_fields = ('Common_ID', 'Unique_ID',)



admin.site.register((Classroom,
                     Course,
                     SectionGroup,
                     ProgramBranch,
                     CourseSchedule,
                     ClassroomActionLog
                     ), ModelAttributes)

admin.site.register(UserDataCredentials, UserClassAttributes)
