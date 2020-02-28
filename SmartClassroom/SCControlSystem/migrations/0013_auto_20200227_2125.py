# Generated by Django 3.0.3 on 2020-02-27 13:25

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('SCControlSystem', '0012_delete_sensoutput'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courseschedule',
            name='CourseSchedule_Instructor',
            field=models.ForeignKey(blank=True, help_text='Refers to an instructor who teach the following course.', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, to_field='unique_id', verbose_name='Course Instructor'),
        ),
        migrations.AlterField(
            model_name='courseschedule',
            name='CourseSchedule_Lecture_Day',
            field=models.CharField(blank=True, choices=[('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'), ('Friday', 'Friday'), ('Saturday', 'Saturday'), ('Sunday', 'Sunday')], default=('Monday', 'Monday'), help_text='Refers to a day in which the course session takes place.', max_length=9, null=True, validators=[django.core.validators.MinLengthValidator(6), django.core.validators.MaxLengthValidator(9)], verbose_name='Course Lecture Day'),
        ),
        migrations.AlterField(
            model_name='courseschedule',
            name='CourseSchedule_Room',
            field=models.ForeignKey(blank=True, help_text='Refers to a classroom that is currently in vacant in which the session takes place.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ClassRoomMainReference', to='SCControlSystem.Classroom', to_field='Classroom_CompleteString', verbose_name='Course Classroom Assignment'),
        ),
        migrations.AlterField(
            model_name='courseschedule',
            name='CourseSchedule_Session_End',
            field=models.TimeField(blank=True, help_text='Refers to a time end session point.', null=True, verbose_name='Course Session End Time'),
        ),
        migrations.AlterField(
            model_name='courseschedule',
            name='CourseSchedule_Session_Start',
            field=models.TimeField(blank=True, help_text='Refers to a time start session point.', null=True, verbose_name='Course Session Start Time'),
        ),
    ]