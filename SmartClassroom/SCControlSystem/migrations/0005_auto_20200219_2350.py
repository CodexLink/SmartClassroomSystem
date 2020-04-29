# Generated by Django 3.0.3 on 2020-02-19 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SCControlSystem', '0004_auto_20200219_2217'),
    ]

    operations = [
        migrations.AddField(
            model_name='classroom',
            name='Classroom_AccessState',
            field=models.CharField(
                blank=True,
                choices=[('Enabled', 'Enabled'), ('Disabled', 'Disabled')],
                default='Disabled',
                help_text=
                'The current state of the classroom. This is very different from classroom device status.',
                max_length=8,
                null=True,
                verbose_name='Classroom Access State'),
        ),
        migrations.AlterField(
            model_name='classroomactionlog',
            name='UserActionTaken',
            field=models.CharField(
                choices=[('Classroom was Opened by Toggle Lock.',
                          'Classroom was Opened by Toggle Lock.'),
                         ('Classroom was Closed by Toggle Lock.',
                          'Classroom was Closed by Toggle Lock.'),
                         ('Action: Set Room Automate to ON.',
                          'Action: Set Room Automate to ON.'),
                         ('Action: Set Room Automate to OFF.',
                          'Action: Set Room Automate to OFF.'),
                         ('Unauthorized Access Detected.',
                          'Unauthorized Access Detected.'),
                         ('Authorized Access Passed.',
                          'Authorized Access Passed.'),
                         ('Classroom Access was set to Disabled.',
                          'Classroom Access was set to Disabled.'),
                         ('Classroom Access was set to Enable.',
                          'Classroom Access was set to Enable.')],
                help_text=
                'A set of action taken by the stuff and user that is recently recorded by the system.',
                max_length=255,
                verbose_name='Staff / User Action Message'),
        ),
    ]
