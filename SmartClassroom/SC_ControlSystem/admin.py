from django.contrib import admin
from .models import *

# Register your models here.


class SmartClassroomAdminInitSet(admin.ModelAdmin):
    # ! We use this to hide our data from django-admin. No one will edit this one but can view it.
    exclude = 'Classroom_CompleteString', 'Section_CompleteStringGroup'


admin.site.register((Classroom,
                     Course,
                     SectionGroup,
                     ProgramBranch,
                     CourseSchedule,
                     ClassroomActionLog,
                     UserDataCredentials,
                     ), SmartClassroomAdminInitSet)
