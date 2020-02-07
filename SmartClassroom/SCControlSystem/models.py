from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator, MaxLengthValidator
from .externs.subject_types import *
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.contrib.auth.models import AbstractUser
from uuid import uuid4
from django.utils.crypto import get_random_string

# ! ImageField Avatar to Account Function Use

def user_avatar_path(instance, filename):
    return 'usersrc/useravatar_{0}/{1}'.format(instance.unique_id, filename)

'''
# ! Integrity Information for ProgramBranch Model
We only have one field here. Why? Because, you dont want to see someone
choosing Architecture and assigned to CpE. That's pretty much stupid if you think about it.
# ! Status: Completed
'''


class ProgramBranch(models.Model):
    class Meta:
        verbose_name = "Department Program"
        db_table = "dept_programs"

    ProgramBranch_Code = models.CharField(max_length=20, primary_key=True, null=False, blank=False, verbose_name="Program Code", help_text="Declare the program code in shortest way possible", unique=True)
    ProgramBranch_Name = models.CharField(max_length=60, null=True, blank=True, verbose_name="Program Name", help_text="Declare proper names according to the typical standards in relation to Program Name.")

    def __str__(self):
        return '%s | %s' % (self.ProgramBranch_Code, self.ProgramBranch_Name)

# ! Extending DJango's Default User Model by Subclassing AbstractUser
# ! User DataSet Information
class UserDataCredentials(AbstractUser):
    class Meta:
        verbose_name = "User Credential"
        db_table = "user_auth_crendentials"

    # ! These commented fields has been already existing in the User Model. So by extending it, we have only few fields to declare right now.
    middle_name = models.CharField(max_length=20, null=True, blank=True, help_text="A Name that is not supplied by User Model. Added for Unique User Purposes.")
    unique_id = models.UUIDField(max_length=32, default=uuid4, editable=False, unique=True, help_text="A Unique Identifier for your Account. This is used for DB authentication and references. Please DO NOT SHARE IT OUTSIDE.")
    user_role = models.CharField(max_length=27, null=False, blank=False, choices=RoleDeclaredTypes, default=RoleDeclaredTypes[0], help_text="Roles Defined that gives users multiple actions to do. Pick one with RISK.")
    dept_residence = models.ForeignKey(ProgramBranch, to_field="ProgramBranch_Code", verbose_name='Staff Department Residence', help_text='Please refer the program code form where this staff resides.', null=False, blank=False, on_delete=models.CASCADE)
    avatar = models.ImageField(null=True, blank=True, upload_to=user_avatar_path)

    def __str__(self):
        return '%s | %s %s %s | %s' % (self.username, self.first_name, self.middle_name, self.last_name, self.dept_residence)
'''
# ! Integrity Information for Classroom Model
Classroom has set Classroom_CompleteString as the primary key. No other such as unique at this point.
Why? Because, we can have multiple rooms with the same name. Their difference is only their label
Which only indicates uniqueness, and that includes their floor, building, number and their type.
The reason why we didnt make *those* unique because if that happens, we only let one room to occupy on specific floor,
For instance, classroom #1 takes floor 1, after that, we cannot have another room that resides in floor 1.
So, lets make things unique by their complete form instead of individually unique each of those attributes
# ! That may lead to database issues.
# ! Status: Completed
'''

class Classroom(models.Model):
    class Meta:
         verbose_name = "Classroom Declaration"
         db_table = "classroom_decl"

    Classroom_Name = models.CharField(max_length=50, null=False, blank=False, verbose_name='Classroom Name', help_text='', validators=[MinLengthValidator(5), MaxLengthValidator(50)])
    Classroom_Building = models.PositiveIntegerField(null=False, blank=False, verbose_name='Classroom Building Assignment', help_text='', default=BuildingClassification[0], choices=BuildingClassification)
    Classroom_Floor = models.PositiveIntegerField(null=False, blank=False, verbose_name='Classroom Floor Assignment', help_text='', default=BuildingFloors[0], choices=BuildingFloors)
    Classroom_Number = models.PositiveIntegerField(null=False, blank=False, verbose_name='Classroom Number', help_text='', default=1, validators=[MinValueValidator(1), MaxValueValidator(29)])
    Classroom_Type = models.CharField(max_length=29, null=False, blank=False, verbose_name='Classroom Instructure Type', help_text='', validators=[MinLengthValidator(13), MaxLengthValidator(29)], default=CourseSessionTypes[0], choices=CourseSessionTypes)
    Classroom_CompleteString = models.CharField(max_length=6, null=True, blank=True, unique=True, verbose_name='Classroom Complete CodeName', validators=[MinLengthValidator(6), MaxLengthValidator(6)], help_text="This field is automatically filled when you submit it. Putting any value result to it, being discarded.")

    def __str__(self):
        return '%s — %s | %s' % (self.Classroom_CompleteString, self.get_Classroom_Type_display(), self.Classroom_Name)

    def save(self, *args, **kwargs):
        self.Classroom_CompleteString = 'Q-%s%s%s' % (self.Classroom_Building, self.Classroom_Floor, str(self.Classroom_Number).zfill(2))
        super(Classroom, self).save(*args, **kwargs)

    def clean(self):
        if Classroom.objects.filter(Classroom_Building=self.Classroom_Building, Classroom_Floor=self.Classroom_Floor, Classroom_Number=self.Classroom_Number, Classroom_Type=self.Classroom_Type).exists():
            raise ValidationError("Error, you might be choosing an occupied room! Please choose another one. Or if you're attempting to change the room name and the form save state failed. Adjust any integer fields by 1 or something that doesn't exists and adjust the name then, revert it back to save the configuration.")
        else:
            return super(Classroom, self).clean()

class Course(models.Model):
    class Meta:
         verbose_name = "Course Declaration"
         db_table = "course_decl"

    Course_Name = models.CharField(max_length=100, null=False, blank=False, help_text='Please indicate. We need to know what type of room is it gonna be.', validators=[MinLengthValidator(5), MaxLengthValidator(100)])
    Course_Code = models.CharField(max_length=10, null=False, blank=False, primary_key=True, unique=True, help_text='Provide Course Code with Probable In Relation to Course itself.', validators=[MinLengthValidator(4), MaxLengthValidator(10)])
    Course_Units = models.PositiveIntegerField(help_text='Units is indenpendent and user should know it based on lecture time and classroom type to use.', validators=[MinValueValidator(1), MaxValueValidator(6)])
    Course_Capacity = models.PositiveIntegerField(default=15, help_text='The number of students that can included in the class. Minimum is 15 and Maximum is 45', validators=[MinValueValidator(15), MaxValueValidator(60)])  # Capacity of Room for Students
    Course_Type = models.CharField(max_length=29, null=False, blank=False, help_text='Course Type is dependent, if it needs Laboratory or Technological Only. Please pick properly.', validators=[MinLengthValidator(13), MaxLengthValidator(29)], default=CourseSessionTypes[0], choices=CourseSessionTypes)

    def __str__(self):
        return '{0} — {1} | {2}'.format(self.Course_Code, self.Course_Name, self.get_Course_Type_display())

'''
# ! Integrity Information for SectionGroup Model
We have the same instance of integrity as Classroom Model.
Why? As we have said it earlier, we cannot make those attributes as unique. Because we're not giving the admin
a chance to make another instance of a particular attribute inherited to another data. What do I mean?
Well, for instance, if you have one section as 'CPE22FA1' then if you're about to create another with the same attributes
but with different program branch, such as 'ARch22FA1' then it will not be allowed.

Hence, we conclude that the completed unique field is the one that we only need to be our primary key or well, at least a unique key.
# ! Status: Completed
'''

class SectionGroup(models.Model):
    class Meta:
        verbose_name = "Student Section"
        db_table = "student_sec_decl"

    Section_Program = models.ForeignKey(ProgramBranch, to_field="ProgramBranch_Code", verbose_name='Section Program', help_text='Please refer the program code form where the section resides.', null=False, blank=False, on_delete=models.CASCADE)
    Section_Year = models.PositiveIntegerField(choices=YearBatchClasses, verbose_name='Section Year', help_text='Indicate the section level.', null=False, blank=False)
    Section_Semester = models.PositiveIntegerField(verbose_name='Section Semester', help_text='Indicate the section semester', null=False, blank=False, choices=SemClassification)
    Section_SubUniqueGroup = models.CharField(max_length=3, verbose_name='Section SubUnique Group', help_text='Subunique Group that distinct other section from one another.', null=False, blank=False, choices=SubSectionUniqueKeys, validators=[MinLengthValidator(3), MaxLengthValidator(3)])
    Section_CompleteStringGroup = models.CharField(max_length=10, verbose_name='Section Complete Codename', help_text='Combined Information into one Codename. This cannot be modified nor replaced. This is submit-dependent content value.', null=False, blank=False, unique=True, validators=[MinLengthValidator(1), MaxLengthValidator(5)])

    def __str__(self):
        return 'Section %s' % (self.Section_CompleteStringGroup)

    def save(self, *args, **kwargs):
        self.Section_CompleteStringGroup = '%s%s%s%s' % (self.Section_Program.ProgramBranch_Code, self.Section_Year, self.Section_Semester, self.Section_SubUniqueGroup)
        super(SectionGroup, self).save(*args, **kwargs)

    def checkSGDuplicates(self, program, year, semester, unique_group):
        if SectionGroup.objects.filter(Section_Program=program, Section_Year=year, Section_Semester=semester, Section_SubUniqueGroup=unique_group).exists():
            return True
        else:
            return False

    def clean(self):
        if self.checkSGDuplicates(self.Section_Program, self.Section_Year, self.Section_Semester, self.Section_SubUniqueGroup):
            raise ValidationError("Error, you might be choosing a section that is already declared! Please choose another one. Or if you're attempting to change the room name and the form save state failed. Adjust any integer fields by 1 or something that doesn't exists and adjust the name then, revert it back to save the configuration.")

        else:
            return super(SectionGroup, self).clean()

# ! Add Time Conflict Here
class CourseSchedule(models.Model):
    class Meta:
        verbose_name = "Enlisted Course Schedule"
        db_table = "enlisted_course_scheds"

    CourseSchedule_CourseReference = models.OneToOneField(Course, verbose_name='Course Reference', help_text='Refers to a candidated subject from which allocates the time.', primary_key=True, to_field="Course_Code", null=False, blank=False, unique=True, on_delete=models.CASCADE)
    CourseSchedule_Instructor = models.OneToOneField(UserDataCredentials, verbose_name='Course Instructor', help_text='Refers to an instructor who teach the following course.', to_field="unique_id", null=False, blank=False, on_delete=models.CASCADE)
    CourseSchedule_Room = models.ForeignKey(Classroom, verbose_name='Course Classroom Assignment', help_text='Refers to a classroom that is currently in vacant in which the session takes place.', null=False, blank=False, to_field="Classroom_CompleteString", related_name="ClassRoomMainReference", on_delete=models.CASCADE)
    CourseSchedule_Session_Start = models.TimeField(verbose_name='Course Session Start Time', help_text='Refers to a time start session point.', null=False, blank=False, unique=True)
    CourseSchedule_Session_End = models.TimeField(verbose_name='Course Session End Time', help_text='Refers to a time end session point.', null=False, blank=False, unique=False)
    CourseSchedule_Lecture_Day = models.CharField(max_length=9, verbose_name='Course Lecture Day', help_text='Refers to a day in which the course session takes place.', null=False, blank=False, default=SessionDaysClassification[0], choices=SessionDaysClassification, unique=True, validators=[MinLengthValidator(6), MaxLengthValidator(9)])

    def __str__(self):
        return 'Schedule of %s | Handled by %s | Every %s | Time: %s-%s' % (self.CourseSchedule_CourseReference, self.CourseSchedule_Instructor, self.CourseSchedule_Lecture_Day, self.CourseSchedule_Session_Start, self.CourseSchedule_Session_End)

# ! Required Logging for Admin | Teachers Actions on that Particular Classroom

class ClassroomActionLog(models.Model):
    class Meta:
        verbose_name = "Classroom Recent Log"
        db_table = "classroom_action_logs"

    UserActionTaken = models.CharField(verbose_name='Staff / User Action Message', help_text='A set of action taken by the stuff and user that is recently recorded by the system.', max_length=255, null=False, blank=False, choices=ClassroomActionTypes)
    ActionLevel = models.CharField(verbose_name='Log Action Level', help_text='The level of log indication. This only benefit for actions being filtered.', max_length=255, null=False, blank=False, choices=LevelAlert)
    Course_Reference = models.OneToOneField(CourseSchedule, verbose_name='Schedule Instance Reference', help_text='The course with its schedule referenced into one.', null=False, blank=False, related_name="CourseAssociated", on_delete=models.CASCADE)

    def __str__(self):
        return 'Level %s | Action: %s | Session of %s ' % (self.ActionLevel, self.UserActionTaken, self.Course_Reference,)