# Generated by Django 3.0.3 on 2020-02-08 16:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('SCControlSystem', '0006_auto_20200209_0036'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='classroom',
            options={'permissions': [('classroom_viewable', 'Can view the classroom window. Used for PermissionsRequiredMixin.')], 'verbose_name': 'Classroom Declaration'},
        ),
        migrations.AlterModelOptions(
            name='classroomactionlog',
            options={'permissions': [('classroom_action_log_viewable', 'Can view the classroom action log window. Used for PermissionRequiredMixin.')], 'verbose_name': 'Classroom Recent Log'},
        ),
        migrations.AlterModelOptions(
            name='course',
            options={'permissions': [('course_viewable', 'Can view the course window. Used for PermissionsRequiredMixin.')], 'verbose_name': 'Course Declaration'},
        ),
        migrations.AlterModelOptions(
            name='courseschedule',
            options={'permissions': [('course_schedule_viewable', 'Can view the course schedule window. Used for PermissionRequiredMixin.')], 'verbose_name': 'Enlisted Course Schedule'},
        ),
        migrations.AlterModelOptions(
            name='programbranch',
            options={'permissions': [('program_branch_viewable', 'Can view the program branch window. Used for PermissionsRequiredMixin.')], 'verbose_name': 'Department Program'},
        ),
        migrations.AlterModelOptions(
            name='sectiongroup',
            options={'verbose_name': 'Student Section'},
        ),
    ]