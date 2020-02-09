# Generated by Django 3.0.3 on 2020-02-07 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SCControlSystem', '0003_auto_20200207_2332'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courseschedule',
            name='CourseSchedule_Session_End',
            field=models.TimeField(default=None, help_text='Refers to a time end session point.', verbose_name='Course Session End Time'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='courseschedule',
            name='CourseSchedule_Session_Start',
            field=models.TimeField(default=None, help_text='Refers to a time start session point.', unique=True, verbose_name='Course Session Start Time'),
            preserve_default=False,
        ),
    ]