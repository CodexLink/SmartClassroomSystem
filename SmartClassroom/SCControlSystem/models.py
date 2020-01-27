from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator, MaxLengthValidator
from .externs.subject_types import *
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.contrib.auth.models import AbstractUser
from uuid import uuid4
from django.utils.crypto import get_random_string
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
    Classroom_Name = models.CharField(max_length=50, null=False, blank=False, validators=[
                                      MinLengthValidator(5), MaxLengthValidator(50)])
    Classroom_Building = models.PositiveIntegerField(
        null=False, blank=False, default=BuildingClassification[0], choices=BuildingClassification)
    Classroom_Floor = models.PositiveIntegerField(
        null=False, blank=False, default=BuildingFloors[0], choices=BuildingFloors)
    Classroom_Number = models.PositiveIntegerField(null=False, blank=False, default=1, validators=[
                                                   MinValueValidator(1), MaxValueValidator(29)])
    Classroom_Type = models.CharField(max_length=29, null=False, blank=False, validators=[MinLengthValidator(
        13), MaxLengthValidator(29)], default=CourseSessionTypes[0], choices=CourseSessionTypes)
    Classroom_CompleteString = models.CharField(max_length=6, null=True, blank=True, unique=True, validators=[MinLengthValidator(6), MaxLengthValidator(
        6)], help_text="This field will be automatically filled when you submit it. Putting any value will result to it, discarded.")

    def __str__(self):
        return 'Room Q-%s%s%s | %s Type | %s | Complete Unique: %s' % (self.Classroom_Building, self.Classroom_Floor, str(self.Classroom_Number).zfill(2), self.get_Classroom_Type_display(), self.Classroom_Name, self.Classroom_CompleteString)

    def save(self, *args, **kwargs):
        self.Classroom_CompleteString = 'Q-%s%s%s' % (
            self.Classroom_Building, self.Classroom_Floor, str(self.Classroom_Number).zfill(2))
        super(Classroom, self).save(*args, **kwargs)

    def checkCRDuplicates(self, building, floor, number):
        if Classroom.objects.filter(Classroom_Building=building, Classroom_Floor=floor, Classroom_Number=number).exists():
            return True
        else:
            return False

    def clean(self):
        if self.checkCRDuplicates(self.Classroom_Building, self.Classroom_Floor, self.Classroom_Number):
            raise ValidationError(
                'Error, you''re choosing an occupied room! Please choose another one. Or, if you saved it without any pending changes, please ignore this message if it is.')
        else:
            return super(Classroom, self).clean()


class Course(models.Model):
    Course_Name = models.CharField(max_length=100, null=False, blank=False, validators=[
                                   MinLengthValidator(5), MaxLengthValidator(100)])
    Course_Code = models.CharField(max_length=10, null=False, blank=False, primary_key=True, unique=True, validators=[
                                   MinLengthValidator(4), MaxLengthValidator(10)])
    Course_Units = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(6)])
    Course_Capacity = models.PositiveIntegerField(default=15, validators=[
                                                  MinValueValidator(15), MaxValueValidator(60)])  # Capacity of Room for Students
    Course_Type = models.CharField(max_length=29, null=False, blank=False, validators=[MinLengthValidator(
        13), MaxLengthValidator(29)], default=CourseSessionTypes[0], choices=CourseSessionTypes)

    def __str__(self):
        return 'Course | {0} — {1} | {2} Type | Units: {3} | Capacity: {4}'.format(self.Course_Code, self.Course_Name, self.get_Course_Type_display(), self.Course_Units, self.Course_Capacity)


'''
# ! Integrity Information for ProgramBranch Model
We only have one field here. Why? Because, you dont want to see someone
choosing Architecture and assigned to CpE. That's pretty much stupid if you think about it.
# ! Status: Completed
'''


class ProgramBranch(models.Model):
    ProgramBranch_Code = models.CharField(max_length=4, primary_key=True, null=False, blank=False, validators=[
                                          MinLengthValidator(2), MaxLengthValidator(4)], choices=CEAProgamCCode, unique=True)

    def __str__(self):
        return '%s | %s Program' % (self.ProgramBranch_Code, self.get_ProgramBranch_Code_display())


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
    Section_Program = models.ForeignKey(
        ProgramBranch, to_field="ProgramBranch_Code", null=False, blank=False, on_delete=models.CASCADE)
    Section_Year = models.PositiveIntegerField(
        choices=YearBatchClasses, null=False, blank=False)
    Section_Semester = models.PositiveIntegerField(
        null=False, blank=False, choices=SemClassification)
    Section_SubUniqueGroup = models.CharField(max_length=3, null=False, blank=False, choices=SubSectionUniqueKeys, validators=[
                                              MinLengthValidator(3), MaxLengthValidator(3)])
    Section_CompleteStringGroup = models.CharField(max_length=10, null=False, blank=False, unique=True, validators=[
                                                   MinLengthValidator(1), MaxLengthValidator(5)])

    def __str__(self):
        return 'Section %s | %s | %s — %s | Subgroup of %s' % (self.Section_CompleteStringGroup, self.Section_Program, self.get_Section_Year_display(), self.get_Section_Semester_display(), self.Section_SubUniqueGroup)

    def save(self, *args, **kwargs):
        self.Section_CompleteStringGroup = '%s%s%s%s' % (
            self.Section_Program.ProgramBranch_Code, self.Section_Year, self.Section_Semester, self.Section_SubUniqueGroup)
        print(self.Section_CompleteStringGroup)
        super(SectionGroup, self).save(*args, **kwargs)

    def checkSGDuplicates(self, program, year, semester, unique_group):
        if SectionGroup.objects.filter(Section_Program=program, Section_Year=year, Section_Semester=semester, Section_SubUniqueGroup=unique_group).exists():
            return True
        else:
            return False

    def clean(self):
        if self.checkSGDuplicates(self.Section_Program, self.Section_Year, self.Section_Semester, self.Section_SubUniqueGroup):
            raise ValidationError(
                'Error, you''re choosing a section that is already declared! Please choose another one. Or, if you saved it without any pending changes, please ignore this message if it is.')
        else:
            return super(SectionGroup, self).clean()


class CourseSchedule(models.Model):
    CourseSchedule_CourseCode = models.OneToOneField(
        Course, primary_key=True, to_field="Course_Code", null=False, blank=False, unique=True, on_delete=models.CASCADE)
    CourseSchedule_Instructor = models.CharField(max_length=50, null=False, blank=False, unique=True, validators=[
                                                 MinLengthValidator(4), MaxLengthValidator(50)])
    CourseSchedule_LectureDay_Tech = models.CharField(max_length=9, null=False, blank=False, default=SessionDaysClassification[
                                                      0], choices=SessionDaysClassification, unique=True, validators=[MinLengthValidator(6), MaxLengthValidator(9)])
    CourseSchedule_SessionStart_Tech = models.TimeField(
        null=True, blank=True, unique=True)
    CourseSchedule_SessionEnd_Tech = models.TimeField(
        null=True, blank=True, unique=False)
    CourseSchedule_LectureDay_Lab = models.CharField(max_length=9, null=True, blank=True, default=SessionDaysClassification[
                                                     0], choices=SessionDaysClassification, unique=True, validators=[MinLengthValidator(6), MaxLengthValidator(9)])
    CourseSchedule_SessionStart_Lab = models.TimeField(
        null=True, blank=True, unique=False)
    CourseSchedule_SessionEnd_Lab = models.TimeField(
        null=True, blank=True, unique=False)
    CourseSchedule_LectureDay_Ext = models.CharField(max_length=9, null=True, blank=True, default=SessionDaysClassification[
                                                     0], choices=SessionDaysClassification, unique=True, validators=[MinLengthValidator(6), MaxLengthValidator(9)])
    CourseSchedule_SessionStart_Ext = models.TimeField(
        null=True, blank=True, unique=False)
    CourseSchedule_SessionEnd_Ext = models.TimeField(
        null=True, blank=True, unique=False)

    def __str__(self):
        return 'Schedule of %s | Handled by %s | Every %s | Time: %s-%s' % (self.CourseSchedule_CourseCode, self.CourseSchedule_Instructor, print(self.get_CourseSchedule_LectureDay_display()), self.CourseSchedule_SessionStart, self.CourseSchedule_SessionEnd)

    # ! Need more if and else statement here.
    def clean(self):
        if not ((self.CourseSchedule_LectureDay_Tech and self.CourseSchedule_SessionStart_Tech and self.CourseSchedule_SessionEnd_Tech) or (self.CourseSchedule_LectureDay_Lab and self.CourseSchedule_SessionStart_Lab and self.CourseSchedule_SessionEnd_Lab) or (self.CourseSchedule_LectureDay_Ext and self.CourseSchedule_SessionStart_Ext and self.CourseSchedule_SessionEnd_Ext)):
            raise ValidationError(
                "You must specify either Technological, Laboratory or External Times. It must be complete in details.")

# ! Required Logging for Admin | Teachers Actions on that Particular Classroom


class ClassroomActionLog(models.Model):
    UserActionTaken = models.CharField(
        max_length=255, null=False, blank=False, choices=ClassroomActionTypes)
    ClassRoom_Reference = models.ForeignKey(
        Classroom, null=False, blank=False, to_field="Classroom_CompleteString", related_name="RoomClassReference", on_delete=models.CASCADE)
    Course_Reference = models.OneToOneField(CourseSchedule, null=False, blank=False,
                                            to_field="CourseSchedule_CourseCode", related_name="CourseAssociated", on_delete=models.CASCADE)
    Section_Reference = models.ForeignKey(SectionGroup, null=False, blank=False,
                                          to_field="Section_CompleteStringGroup", related_name="StudentGroupAssociate", on_delete=models.CASCADE)
    ClassInstructor_Reference = models.ForeignKey(
        CourseSchedule, null=False, blank=False, to_field="CourseSchedule_Instructor", related_name="InstructorAssociate", on_delete=models.CASCADE)
    # Added later. By Request Process.
    LectureTimeStart_Reference = models.TimeField(null=False, blank=False)
    LectureTimeEnd_Reference = models.TimeField(null=False, blank=False)

# ! Extending DJango's Default User Model by Subclassing AbstractUser
# ! User DataSet Information
class UserDataCredentials(AbstractUser):
    # ! These commented fields has been already existing in the User Model. So by extending it, we have only few fields to declare right now.
    #AdminInfo_First_Name = models.CharField(max_length=20,null=False,blank=False)
    #AdminInfo_Last_Name = models.CharField(max_length=50,null=False,blank=False)
    # AdminInfo_UserName = models.CharField(max_length=)
    # AdminInfo_Password = models.PasswordField(max_length=)
    middleName = models.CharField(max_length=20, null=True, blank=True)
    uniqueId = models.UUIDField(max_length=32, default=uuid4, editable=False)
    commonId = models.CharField(max_length=32, null=False, blank=False, default=get_random_string(32))
    role = models.CharField(max_length=27, null=False, blank=False, choices=RoleDeclaredTypes, default=RoleDeclaredTypes[0])
    lastCreated = models.DateTimeField(auto_now_add=True)