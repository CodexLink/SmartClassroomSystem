# Generated by Django 3.0.3 on 2020-02-25 09:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('SCControlSystem', '0009_auto_20200221_2326'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userdatacredentials',
            name='fp_primary',
        ),
        migrations.RemoveField(
            model_name='userdatacredentials',
            name='fp_secondary',
        ),
        migrations.RemoveField(
            model_name='userdatacredentials',
            name='fp_tertiary',
        ),
        migrations.AddField(
            model_name='userdatacredentials',
            name='fp_id',
            field=models.PositiveIntegerField(blank=True, help_text='A Unique User FingerPrint. Required for All Classroom that has User Detection. Keep in mind that, with this ID, it must be registered to all Fingerprints in which the user goes into!!!', null=True, unique=True, verbose_name='User Fingerprint ID'),
        ),
        migrations.AlterField(
            model_name='courseschedule',
            name='CourseSchedule_Instructor',
            field=models.ForeignKey(help_text='Refers to an instructor who teach the following course.', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, to_field='unique_id', verbose_name='Course Instructor'),
        ),
    ]