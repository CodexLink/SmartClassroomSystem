from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator, MaxLengthValidator
from .externs.subject_types import *
from django.core.exceptions import ValidationError
from django.db import IntegrityError

class Classroom(models.Model):
    Classroom_Name = models.CharField(max_length=50, null=False, blank=False, unique=True, validators=[MinLengthValidator(5), MaxLengthValidator(50)])
    Classroom_Building = models.PositiveIntegerField(null=False, blank=False, default=BuildingClassification[0], choices=BuildingClassification)
    Classroom_Floor = models.PositiveIntegerField(null=False, blank=False, default=BuildingFloors[0], choices=BuildingFloors)
    Classroom_Number = models.PositiveIntegerField(null=False, blank=False, default=1, validators=[MinValueValidator(1), MaxValueValidator(29)])
    Classroom_Type = models.CharField(max_length=29, null=False, blank=False, unique=True, validators=[MinLengthValidator(13), MaxLengthValidator(29)], default=CourseSessionTypes[0], choices=CourseSessionTypes)
    Classroom_CompleteString = models.CharField(max_length=6, null=True, blank=True, unique=True, validators=[MinLengthValidator(6), MaxLengthValidator(6)])

    def __str__(self):
        return 'Room Q-%s%s%s | %s Type | %s | Complete Unique: %s' % (self.Classroom_Building, self.Classroom_Floor, str(self.Classroom_Number).zfill(2), self.get_Classroom_Type_display(), self.Classroom_Name, self.Classroom_CompleteString)


    def save(self, *args, **kwargs):
        self.Classroom_CompleteString = 'Q-%s%s%s' % (self.Classroom_Building, self.Classroom_Floor, str(self.Classroom_Number).zfill(2))
        super(Classroom, self).save(*args, **kwargs)

    def checkDuplicates(self, building, floor, number):
        if Classroom.objects.filter(Classroom_Building=building, Classroom_Floor=floor, Classroom_Number=number).exists():
            return True
        else:
            return False

    def clean(self):
        if self.checkDuplicates(self.Classroom_Building, self.Classroom_Floor, self.Classroom_Number):
            raise ValidationError('Error, you choosed the same room! Please choose another one.')
        else:
            return super(Classroom, self).clean()

    class Meta:
        unique_together = ('Classroom_Type', 'Classroom_CompleteString')

class Course(models.Model):
    Course_Name = models.CharField(max_length=100, null=False, blank=False, validators=[MinLengthValidator(5), MaxLengthValidator(100)])
    Course_Code = models.CharField(max_length=10, null=False, blank=False, primary_key=True, unique=True, validators=[MinLengthValidator(4), MaxLengthValidator(10)])
    Course_Units = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(6)])
    Course_Capacity = models.PositiveIntegerField(default=15, validators=[MinValueValidator(15), MaxValueValidator(60)])  # Capacity of Room for Students
    Course_Type = models.CharField(max_length=29, null=False, blank=False, validators=[MinLengthValidator(13), MaxLengthValidator(29)], default=CourseSessionTypes[0], choices=CourseSessionTypes)

    def __str__(self):
        return 'Course | {0} — {1} | {2} Type | Units: {3} | Capacity: {4}'.format(self.Course_Code, self.Course_Name, self.get_Course_Type_display(), self.Course_Units, self.Course_Capacity)

class ProgramBranch(models.Model):
    ProgramBranch_Name = models.CharField(max_length=50, null=False, blank=False, unique=True, validators=[MinLengthValidator(5), MaxLengthValidator(50)])
    ProgramBranch_Description = models.TextField(max_length=255, null=True, blank=True, validators=[MinLengthValidator(10), MaxLengthValidator(255)])
    ProgramBranch_Code = models.CharField(max_length=4, primary_key=True, null=False, blank=False, validators=[MinLengthValidator(2), MaxLengthValidator(4)], choices=CEAProgamCCode, unique=True)

    def __str__(self):
        return 'Program | %s — %s | %s' % (self.get_ProgramBranch_Code_display(), self.ProgramBranch_Name, self.ProgramBranch_Description)

    class Meta:
        unique_together = ('ProgramBranch_Name', 'ProgramBranch_Code')

class SectionGroup(models.Model):
    import random
    Section_Program = models.ForeignKey(ProgramBranch, to_field="ProgramBranch_Code" ,null=False, blank=False, unique=False, on_delete=models.CASCADE)
    Section_Year = models.CharField(max_length=8, choices=YearBatchClasses, null=False, blank=False, unique=False, validators=[MinLengthValidator(8), MaxLengthValidator(8)])
    Section_Semester = models.CharField(max_length=12, null=False, blank=False, choices=SemClassification, unique=False, validators=[MinLengthValidator(12), MaxLengthValidator(12)])
    Section_SubUniqueGroup = models.CharField(max_length=3, null=False, blank=False, choices=SubSectionUniqueKeys, unique=False, validators=[MinLengthValidator(3), MaxLengthValidator(3)])

    # ! Concatenation is needed.
    Section_CompleteStringGroup = models.CharField(max_length=5, null=False, blank=False, unique=True, default=random.randint(0, 999), validators=[MinLengthValidator(1), MaxLengthValidator(5)])


    #print(SectionGroup.objects.all, Section_Year, Section_Semester)
    # default=str_section_data_concat(Section_Program, Section_Year, Section_Semester, Section_SubUniqueGroup)

    def __str__(self):
        return 'Section | %s %s — %s | Subgroup of %s | Summary: %s' % (self.Section_Program, self.Section_Year, self.Section_Semester, self.Section_SubUniqueGroup, print(self.Section_CompleteStringGroup))

    #class Meta:
    #    unique_together = ('Section_Program', 'Section_Year', 'Section_Semester', 'Section_SubUniqueGroup')

class CourseSchedule(models.Model):
    CourseSchedule_CourseCode = models.OneToOneField(Course, primary_key=True, to_field="Course_Code", null=False, blank=False, unique=True, on_delete=models.CASCADE)
    CourseSchedule_Instructor = models.CharField(max_length=50, null=False, blank=False, unique=True, validators=[MinLengthValidator(4), MaxLengthValidator(50)])
    CourseSchedule_LectureDay_Tech = models.CharField(max_length=9, null=False, blank=False, default=SessionDaysClassification[0], choices=SessionDaysClassification, unique=True, validators=[MinLengthValidator(6), MaxLengthValidator(9)])
    CourseSchedule_SessionStart_Tech = models.TimeField(null=True, blank=True, unique=True)
    CourseSchedule_SessionEnd_Tech = models.TimeField(null=True, blank=True, unique=False)
    CourseSchedule_LectureDay_Lab = models.CharField(max_length=9, null=True, blank=True, default=SessionDaysClassification[0], choices=SessionDaysClassification, unique=True, validators=[MinLengthValidator(6), MaxLengthValidator(9)])
    CourseSchedule_SessionStart_Lab = models.TimeField(null=True, blank=True, unique=False)
    CourseSchedule_SessionEnd_Lab = models.TimeField(null=True, blank=True, unique=False)
    CourseSchedule_LectureDay_Ext = models.CharField(max_length=9, null=True, blank=True, default=SessionDaysClassification[0], choices=SessionDaysClassification, unique=True, validators=[MinLengthValidator(6), MaxLengthValidator(9)])
    CourseSchedule_SessionStart_Ext = models.TimeField(null=True, blank=True, unique=False)
    CourseSchedule_SessionEnd_Ext = models.TimeField(null=True, blank=True, unique=False)

    def __str__(self):
        return 'Schedule of %s | Handled by %s | Every %s | Time: %s-%s' % (self.CourseSchedule_CourseCode, self.CourseSchedule_Instructor, print(self.get_CourseSchedule_LectureDay_display()), self.CourseSchedule_SessionStart, self.CourseSchedule_SessionEnd)

    # ! Need more if and else statement here.
    def clean(self):
        if not ((self.CourseSchedule_LectureDay_Tech and self.CourseSchedule_SessionStart_Tech and self.CourseSchedule_SessionEnd_Tech) or (self.CourseSchedule_LectureDay_Lab and self.CourseSchedule_SessionStart_Lab and self.CourseSchedule_SessionEnd_Lab) or (self.CourseSchedule_LectureDay_Ext and self.CourseSchedule_SessionStart_Ext and self.CourseSchedule_SessionEnd_Ext)):
            raise ValidationError("You must specify either Technological, Laboratory or External Times. It must be complete in details.")

# ! Required Logging for Admin | Teachers Actions on that Particular Classroom
class ClassroomActionLog(models.Model):
    UserActionTaken = models.CharField(max_length=255, null=False, blank=False, choices=ClassroomActionTypes)
    ClassRoom_Reference = models.ForeignKey(Classroom, null=False, blank=False, to_field="Classroom_CompleteString", related_name="RoomClassReference", on_delete=models.CASCADE)
    ClassType_Reference = models.OneToOneField(Classroom, null=False, blank=False, to_field="Classroom_Type", related_name="TypeClassReference", on_delete=models.CASCADE)
    Course_Reference = models.OneToOneField(CourseSchedule, null=False, blank=False, to_field="CourseSchedule_CourseCode", related_name="CourseAssociated", on_delete=models.CASCADE)
    Section_Reference = models.ForeignKey(SectionGroup, null=False, blank=False, to_field="Section_CompleteStringGroup", related_name="StudentGroupAssociate", on_delete=models.CASCADE)
    ClassInstructor_Reference = models.ForeignKey(CourseSchedule, null=False, blank=False, to_field="CourseSchedule_Instructor", related_name="InstructorAssociate", on_delete=models.CASCADE)
    # Added later. By Request Process.
    LectureTimeStart_Reference = models.TimeField(null=False, blank=False)
    LectureTimeEnd_Reference = models.TimeField(null=False, blank=False)