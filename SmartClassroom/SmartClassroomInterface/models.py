from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator, MaxLengthValidator
from .externs.subject_types import *

class Classroom(models.Model):
    Classroom_Name = models.CharField(max_length=50, null=False, blank=False, validators=[MinLengthValidator(5), MaxLengthValidator(50)])
    Classroom_Building = models.PositiveIntegerField(null=False, blank=False, default=BuildingClassification[0], choices=BuildingClassification)
    Classroom_Floor = models.PositiveIntegerField(null=False, blank=False, default=BuildingFloors[0], choices=BuildingFloors)
    Classroom_Number = models.PositiveIntegerField(null=False, blank=False, default=1, validators=[MinValueValidator(1), MaxValueValidator(29)])
    Classroom_Type = models.PositiveIntegerField(null=False, blank=False, unique=True, default=CourseSessionTypes[0], choices=CourseSessionTypes)
    Classroom_CompleteString = models.CharField(max_length=6, null=False, blank=False, unique=True, validators=[MinLengthValidator(6), MaxLengthValidator(6)])

    def __str__(self):
        return 'Room Q-{0}{1}{2} | {3} Type | {4}'.format(self.roomClassBuilding, self.roomClassFloor, str(self.roomClassNumber).zfill(2), self.get_roomClassType_display(), self.roomClassName)

class Course(models.Model):
    Course_Name = models.CharField(max_length=100, null=False, blank=False, validators=[MinLengthValidator(5), MaxLengthValidator(100)])
    Course_Code = models.CharField(max_length=10, null=False, blank=False, unique=True, primary_key=True, validators=[MinLengthValidator(4), MaxLengthValidator(10)])
    Course_Units = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(6)])
    Course_Capacity = models.PositiveIntegerField(default=15, validators=[MinValueValidator(15), MaxValueValidator(60)])  # Capacity of Room for Students
    Course_Type = models.CharField(max_length=15, null=False, blank=False, unique=True, default=CourseSessionTypes[0], choices=CourseSessionTypes)

    def __str__(self):
        return 'Course {0} — {1} | Units: {2} | '.format(self.courseSts_Code, self.courseSts_Name, self.courseSts_Units)

    class Meta:
        unique_together = ('Course_Code', 'Course_Type')

class ProgramBranch(models.Model):
    ProgramBranch_Name = models.CharField(max_length=50, null=False, blank=False, validators=[MinLengthValidator(5), MaxLengthValidator(50)])
    ProgramBranch_Description = models.TextField(max_length=255, null=True, blank=True, validators=[MinLengthValidator(10), MaxLengthValidator(255)])
    ProgramBranch_Code = models.PositiveIntegerField(primary_key=True, null=False, blank=False, choices=CEAProgamCCode, unique=True)

class SectionGroup(models.Model):
    Section_Name = models.CharField(max_length=50, null=False, blank=False, validators=[MinLengthValidator(5), MaxLengthValidator(50)])
    Section_Descrip = models.TextField(max_length=255, null=False, blank=True, validators=[MinLengthValidator(10), MaxLengthValidator(255)])
    Section_Program = models.OneToOneField(ProgramBranch, primary_key=True, to_field="ProgramBranch_Code" ,null=False, blank=False, unique=True, on_delete=models.CASCADE)
    Section_Year = models.PositiveIntegerField(choices=YearBatchClasses, null=False, blank=False, unique=True)
    Section_Semester = models.CharField(max_length=15, null=False, blank=False, choices=SemClassification, unique=True)
    Section_SubUniqueGrop = models.CharField(max_length=3, null=False, blank=False, choices=SubSectionUniqueKeys, unique=True)
    Section_CompleteStringGroup = models.CharField(max_length=5, null=False, blank=False, unique=True, validators=[MinLengthValidator(1), MaxLengthValidator(5)])

    def __str__(self):
        return 'Section {0}{1}{2}{3} | {4}, {5}'.format(self.secBaseProg, self.secYear, self.secSem, self.secSubUniqueSec, self.secBaseName, self.secBaseDescrip)

    class Meta:
        unique_together = ('Section_Program', 'Section_Year', 'Section_Semester', 'Section_SubUniqueGrop')

class CourseSchedule(models.Model):
    CourseSchedule_CourseCode = models.OneToOneField(Course, primary_key=True, to_field="Course_Code", null=False, blank=False, unique=True, on_delete=models.CASCADE)
    CourseSchedule_Instructor = models.CharField(max_length=50, null=False, blank=False, unique=True, validators=[MinLengthValidator(4), MaxLengthValidator(50)])
    CourseSchedule_LectureDay = models.CharField(max_length=10, null=False, blank=False, default=SessionDaysClassification[0], choices=SessionDaysClassification, unique=True)
    CourseSchedule_SessionStart = models.TimeField(null=False, blank=False, unique=True)
    CourseSchedule_SessionEnd = models.TimeField(null=False, blank=False, unique=True)

    def __str__(self):
        return 'Schedule of {0} | Handled by {1} | Every {2} | Time: {3}-{4}'.format(self.courseSch_CourseCode, self.courseSch_Instructor, self.courseSch_DayLect, self.courseSch_sched_startTime, self.courseSch_sched_startEnd)

    class Meta:
        unique_together = ('CourseSchedule_Instructor', 'CourseSchedule_LectureDay', 'CourseSchedule_SessionStart', 'CourseSchedule_SessionEnd')


# ! Required Logging for Admin | Teachers Actions on that Particular Classroom
class ClassroomLogger(models.Model):
    UserActionTaken = models.CharField(max_length=255, null=False, blank=False, choices=ClassroomActionTypes)
    ClassRoom_Reference = models.ForeignKey(Classroom, null=False, blank=False, to_field="Classroom_CompleteString", related_name="RoomClassReference", on_delete=models.CASCADE)
    ClassType_Reference = models.OneToOneField(Classroom, null=False, blank=False, to_field="Classroom_Type", related_name="TypeClassReference", on_delete=models.CASCADE)
    Course_Reference = models.OneToOneField(CourseSchedule, null=False, blank=False, to_field="CourseSchedule_CourseCode", related_name="CourseAssociated", on_delete=models.CASCADE)
    Section_Reference = models.ForeignKey(SectionGroup, null=False, blank=False, to_field="Section_CompleteStringGroup", related_name="StudentGroupAssociate", on_delete=models.CASCADE)
    ClassInstructor_Reference = models.ForeignKey(CourseSchedule, null=False, blank=False, to_field="CourseSchedule_Instructor", related_name="InstructorAssociate", on_delete=models.CASCADE)
    LectureTimeStart_Reference = models.ForeignKey(CourseSchedule, null=False, blank=False, to_field="CourseSchedule_SessionStart", related_name="TimeStartEvent", on_delete=models.CASCADE)
    LectureTimeEnd_Reference = models.ForeignKey(CourseSchedule, null=False, blank=False, to_field="CourseSchedule_SessionEnd", related_name="TimeEndEvent", on_delete=models.CASCADE)