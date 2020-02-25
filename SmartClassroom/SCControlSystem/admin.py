from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
from .forms import UserAuthForm

"""
    Admin.py
    What the heck is this? What are those classes defined here?
    Those class represents displays inside DJango-Admin.
    For each object, we should configure them on what to include, what to filter, what to access, what fields to show, etc.
    # Here in this case, we have alot!

    The number of objects is equal to number class is defined here!
    So keep that in mind.

    Those subclass plays differently.
    ModelAdmin renders a particular object INSIDE. When I say inside, what I meant is, rendering their fields when modifying or creating new data on it.
    UserAdmin renders the Special Overidden User Model. Which means it does the same as ModelAdmin except that it is specially configured.
"""

class ClassroomActionLogAttributes(admin.ModelAdmin):
    model = ClassroomActionLog
    list_display = ('Course_Reference', 'ActionLevel', 'UserActionTaken', 'TimeRecorded')
    list_filter = ('Course_Reference', 'ActionLevel', 'UserActionTaken', 'TimeRecorded')

    readonly_fields = ('TimeRecorded',)

class ClassroomAttributes(admin.ModelAdmin):
    model = Classroom
    list_display = ('Classroom_Name', 'Classroom_CompleteString', 'Classroom_Building', 'Classroom_Floor', 'Classroom_Number', 'Classroom_AccessState', 'Classroom_Type', 'Classroom_Unique_ID')
    list_filter = ('Classroom_Name', 'Classroom_CompleteString', 'Classroom_Building', 'Classroom_Floor', 'Classroom_Number', 'Classroom_AccessState', 'Classroom_Type', 'Classroom_Unique_ID')

    readonly_fields = ('Classroom_CompleteString', 'Classroom_Unique_ID')

class CourseScheduleAttributes(admin.ModelAdmin):
    model = CourseSchedule
    list_display = ('CourseSchedule_CourseReference', 'CourseSchedule_Instructor', 'CourseSchedule_Room', 'CourseSchedule_Session_Start', 'CourseSchedule_Session_End', 'CourseSchedule_Lecture_Day')
    list_filter = ('CourseSchedule_CourseReference', 'CourseSchedule_Instructor', 'CourseSchedule_Room', 'CourseSchedule_Session_Start', 'CourseSchedule_Session_End', 'CourseSchedule_Lecture_Day')

    #readonly_fields = ('CourseSchedule_Unique_ID',)

class CourseAttributes(admin.ModelAdmin):
    model = Course
    list_display = ('Course_Name', 'Course_Code', 'Course_Units', 'Course_Capacity', 'Course_Type')
    list_filter = ('Course_Name', 'Course_Code', 'Course_Units', 'Course_Capacity', 'Course_Type')

class BranchAttributes(admin.ModelAdmin):
    model = ProgramBranch
    list_display = ('ProgramBranch_Code', 'ProgramBranch_Name')
    list_filter = ('ProgramBranch_Code', 'ProgramBranch_Name')

class DeviceInfoAttributes(admin.ModelAdmin):
    model = DeviceInfo
    list_display = ('Device_Name', 'Device_Status', 'Device_IP_Address', 'Device_Unique_ID',)
    list_filter = ('Device_Name', 'Device_Status', 'Device_IP_Address', 'Device_Unique_ID',)

    readonly_fields = ('Device_Unique_ID',)

class SensOutputAttributes(admin.ModelAdmin):
    model = SensOutput
    list_display = ('Sens_Name', 'Sens_Ref', 'Sens_Type', 'Sens_Output', 'Sens_Date_Committed')
    list_filter = ('Sens_Name', 'Sens_Ref', 'Sens_Type', 'Sens_Output', 'Sens_Date_Committed')

    readonly_fields = ('Sens_Date_Committed',)

class SectionGroupAttributes(admin.ModelAdmin):
    model = SectionGroup
    list_display = ('Section_CompleteStringGroup', 'Section_Program', 'Section_Year', 'Section_Semester', 'Section_SubUniqueGroup')
    list_filter = ('Section_CompleteStringGroup', 'Section_Program', 'Section_Year', 'Section_Semester', 'Section_SubUniqueGroup')

    readonly_fields = ('Section_CompleteStringGroup',)

class UserClassAttributes(UserAdmin):
    model = UserDataCredentials # ! A Model to reference at.
    """
        Types of Features in DJango-Admin
        List_Display makes you able to display their content by referencing a particular field.
        List_Filter is a feature exclusive based on referenced field. In short, you can filter on **that** field.
        Search_Fields is a set of fields candidated to be searched / indexed when user is looking something by typing in the search bar.
    """
    list_display = ('username', 'first_name', 'middle_name', 'last_name', 'dept_residence', 'user_role', 'is_active' ,'is_staff', 'is_superuser', 'date_joined', 'fp_id')
    list_filter = ('first_name', 'middle_name', 'last_name', 'user_role', 'dept_residence', 'is_active' ,'is_staff', 'is_superuser', 'date_joined', 'fp_id')
    search_fields = ('first_name', 'middle_name', 'last_name', 'user_role', 'dept_residence', 'is_active' ,'is_staff', 'is_superuser', 'date_joined', 'fp_id')

    # ! Fieldsets is a container that contains fields that can be displayed / read / modified. This fields are available when looking at them by CHANGING.
    fieldsets =  (
        ('User Credentials', {
            'fields': ('username', 'password', 'user_role', 'dept_residence', 'fp_id'),
            }
        ),
        ('User Information', {
            'fields': ('first_name', 'middle_name', 'last_name', 'avatar'),
            }
        ),
        ('Permissions and Restrictions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups'),
            }
        ),
        ('Dates | Last Login and Creation Time', {
            'fields': ('last_login', 'date_joined'),
            }
        ),
        ('Technical Information', {
            'fields': ('unique_id',),
            }
        ),
    )
    # ! Add_Fieldsets is a container that contains fields that is candidated to be filled on. This fields are available when CREATING / INSERTING NEW DATA.
    add_fieldsets = (
        ('User Credentials', {
            'fields': ('username', 'password1', 'password2', 'user_role', 'dept_residence'),
            }
        ),
        ('User Information', {
            'fields': ('first_name', 'middle_name', 'last_name', 'avatar'),
            }
        ),
        ('Permissions and Restrictions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups'),
            }
        ),
        ('Technical Information', {
            'fields': ('unique_id',),
            }
        ),

    )
    readonly_fields = ('unique_id', 'date_joined')

# ! Register All Customizations
admin.site.register(Classroom, ClassroomAttributes)
admin.site.register(Course,CourseAttributes)
admin.site.register(SectionGroup, SectionGroupAttributes)
admin.site.register(CourseSchedule, CourseScheduleAttributes)
admin.site.register(DeviceInfo, DeviceInfoAttributes)
admin.site.register(SensOutput, SensOutputAttributes)
admin.site.register(ClassroomActionLog, ClassroomActionLogAttributes)
admin.site.register(ProgramBranch, BranchAttributes)
admin.site.register(UserDataCredentials, UserClassAttributes)
