from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator, MaxLengthValidator
from .externs.subject_types import *

class Classroom(models.Model):
    roomClassName = models.CharField(max_length=50, null=False, blank=False, validators=[MinLengthValidator(5), MaxLengthValidator(50)])
    roomClassBuilding = models.PositiveIntegerField(null=False, blank=False, choices=BuildingClassification, validators=[MinValueValidator(1), MaxValueValidator(11)])
    roomClassFloor = models.PositiveIntegerField(null=False, blank=False, default=BuildingFloors[0], choices=BuildingFloors, validators=[MinValueValidator(0), MaxValueValidator(5)])
    roomClassNumber = models.PositiveIntegerField(null=False, blank=False, default=1, validators=[MinValueValidator(0), MaxValueValidator(29)])
    roomClassType = models.CharField(max_length=15, null=False, blank=False, default=CourseSessionTypes[0], choices=CourseSessionTypes)
    roomClassReferrable = models.CharField(max_length=6, null=False, blank=False, unique=True, validators=[MinLengthValidator(6), MaxLengthValidator(6)])

    def __str__(self):
        return 'Room Q-{0}{1}{2}{3} | {4} Type | {5}'.format(self.roomClassBuilding, self.roomClassFloor, self.roomClassNumber, self.roomClassType, self.roomClassName)

class CourseSets(models.Model):
    courseSts_Name = models.CharField(max_length=100, null=False, blank=False, validators=[MinLengthValidator(5), MaxLengthValidator(100)])
    courseSts_Code = models.CharField(max_length=10, null=False, blank=False, unique=True, primary_key=True, validators=[MinLengthValidator(4), MaxLengthValidator(10)])
    courseSts_Units = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(6)])
    courseSts_Capacity = models.PositiveIntegerField(default=15, validators=[MinValueValidator(15), MaxValueValidator(60)])  # Capacity of Room for Students
    courseSts_Type = models.CharField(max_length=15, null=False, blank=False, unique=True, default=CourseSessionTypes[0], choices=CourseSessionTypes)

    def __str__(self):
        return 'Course {0} — {1} | Units: {2} | '.format(self.courseSts_Code, self.courseSts_Name, self.courseSts_Units)

    class Meta:
        unique_together = ('courseSts_Code', 'courseSts_Type')

class ProgramClasses(models.Model):
    prog_name = models.CharField(max_length=50, null=False, blank=False, validators=[MinLengthValidator(5), MaxLengthValidator(50)])
    prog_description = models.TextField(max_length=255, null=True, blank=True, validators=[MinLengthValidator(10), MaxLengthValidator(255)])
    prog_code = models.CharField(primary_key=True, max_length=10, choices=CEAProgamCCode, unique=True, validators=[MinLengthValidator(4), MaxLengthValidator(10)])

class SectionGroups(models.Model):
    secBaseName = models.CharField(max_length=50, null=False, blank=False, validators=[MinLengthValidator(5), MaxLengthValidator(50)])
    secBaseDescrip = models.TextField(max_length=255, null=False, blank=True, validators=[MinLengthValidator(10), MaxLengthValidator(255)])
    secBaseProg = models.OneToOneField(ProgramClasses, primary_key=True, to_field="prog_code" ,null=False, blank=False, unique=True, on_delete=models.CASCADE)
    secYear = models.PositiveIntegerField(choices=YearBatchClasses, null=False, blank=False, unique=True)
    secSem = models.CharField(max_length=15, null=False, blank=False, choices=SemClassification, unique=True)
    secSubUniqueSec = models.CharField(max_length=3, null=False, blank=False, choices=SubSectionUniqueKeys, unique=True)
    secSubReferrable = models.CharField(max_length=5, null=False, blank=False, unique=True, validators=[MinLengthValidator(1), MaxLengthValidator(5)])

    def __str__(self):
        return 'Section {0}{1}{2}{3} | {4}, {5}'.format(self.secBaseProg, self.secYear, self.secSem, self.secSubUniqueSec, self.secBaseName, self.secBaseDescrip)

    class Meta:
        unique_together = ('secBaseProg', 'secYear', 'secSem', 'secSubUniqueSec')

class CourseSchedules(models.Model):
    courseSch_CourseCode = models.OneToOneField(CourseSets, primary_key=True, to_field="courseSts_Code", null=False, blank=False, unique=True, on_delete=models.CASCADE)
    courseSch_Handler = models.CharField(max_length=50, null=False, blank=False, unique=True, validators=[MinLengthValidator(4), MaxLengthValidator(50)])
    courseSch_DayLect = models.CharField(max_length=10, null=False, blank=False, default=SessionDaysClassification[0], choices=SessionDaysClassification, unique=True)
    courseSch_sched_startTime = models.TimeField(null=False, blank=False, unique=True)
    courseSch_sched_startEnd = models.TimeField(null=False, blank=False, unique=True)

    def __str__(self):
        return 'Schedule of {0} | Handled by {1} | Every {2} | Time: {3}-{4}'.format(self.courseSch_CourseCode, self.courseSch_Handler, self.courseSch_DayLect, self.courseSch_sched_startTime, self.courseSch_sched_startEnd)

    class Meta:
        unique_together = ('courseSch_Handler', 'courseSch_DayLect', 'courseSch_sched_startTime', 'courseSch_sched_startEnd')


# ! Required Logging for Admin | Teachers Actions on that Particular Classroom
class ClassroomLogger(models.Model):
    ActionTaken = models.CharField(max_length=255, null=False, blank=False, choices=ClassroomActionTypes)
    ClassroomRefer = models.ForeignKey(Classroom, null=False, blank=False, to_field="roomClassReferrable", on_delete=models.CASCADE)
    CourseRefer = models.OneToOneField(CourseSchedules, null=False, blank=False, to_field="courseSch_CourseCode", related_name="CourseAssociated", on_delete=models.CASCADE)
    SectionRefer = models.ForeignKey(SectionGroups, null=False, blank=False, to_field="secSubReferrable", related_name="StudentGroupAssociate", on_delete=models.CASCADE)
    HandlerRefer = models.ForeignKey(CourseSchedules, null=False, blank=False, to_field="courseSch_Handler", related_name="HandlerAssociate", on_delete=models.CASCADE)
    TimeStartRefer = models.ForeignKey(CourseSchedules, null=False, blank=False, to_field="courseSch_sched_startTime", related_name="TimeStartEvent", on_delete=models.CASCADE)
    TimeEndRefer = models.ForeignKey(CourseSchedules, null=False, blank=False, to_field="courseSch_sched_startEnd", related_name="TimeEndEvent", on_delete=models.CASCADE)