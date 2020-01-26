from django.contrib import admin
from .models import *
from django import forms

# Register your models here.

class SmartClassroomAdminInitSet(admin.ModelAdmin):
    # ! We use this to hide our data from django-admin. No one will edit this one but can view it.
    #readonly_fields = ('',)
    pass

admin.site.register((Classroom, Course, ProgramBranch, SectionGroup, CourseSchedule, ClassroomActionLog), SmartClassroomAdminInitSet)