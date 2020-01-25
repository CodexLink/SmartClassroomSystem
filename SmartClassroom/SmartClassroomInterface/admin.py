from django.contrib import admin
from .models import *

# Register your models here.

class SmartClassroomAdmin(admin.ModelAdmin):
    # ! We use this to hide our data from django-admin. No one will edit this one but can view it.
    exclude = ('roomClassReferrable', 'secSubReferrable')

admin.site.register((Classroom, CourseSet, ProgramBranch, SectionGroup, CourseSchedule, ClassroomLogger), SmartClassroomAdmin)