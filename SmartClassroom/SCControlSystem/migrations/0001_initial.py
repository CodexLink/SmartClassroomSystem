# Generated by Django 3.0.3 on 2020-02-15 17:36

import SCControlSystem.models
from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='Classroom',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Classroom_Name', models.CharField(help_text='Name of the classroom. Can be same from any other classrooms as long as they are placed differently and uniquely.', max_length=50, validators=[django.core.validators.MinLengthValidator(5), django.core.validators.MaxLengthValidator(50)], verbose_name='Classroom Name')),
                ('Classroom_Building', models.PositiveIntegerField(choices=[(1, 'Building 1'), (2, 'Building 2'), (3, 'Building 3'), (4, 'Building 4'), (5, 'Building 5'), (6, 'Building 6'), (7, 'Building 7'), (8, 'Building 8'), (9, 'Building 9'), (10, 'PE CNTR 1'), (11, 'PE CNTR 2')], default=(1, 'Building 1'), help_text='The building from where the classroom resides.', verbose_name='Classroom Building Assignment')),
                ('Classroom_Floor', models.PositiveIntegerField(choices=[(1, 'Ground Floor'), (2, '2nd Floor'), (3, '3rd Floor'), (4, '4th Floor'), (5, '5th Floor')], default=(1, 'Ground Floor'), help_text='The floor of the building from where the classroom resides.', verbose_name='Classroom Floor Assignment')),
                ('Classroom_Number', models.PositiveIntegerField(default=1, help_text='The room number assignment of the classroom.', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(29)], verbose_name='Classroom Number')),
                ('Classroom_Type', models.CharField(choices=[('Technological Only', 'Technological Only'), ('Laboratory Only', 'Laboratory Only'), ('External Only', 'External Only'), ('Technological and Laboratory', 'Technological and Laboratory'), ('Technological and External', 'Technological and External'), ('Laboratory and Technological', 'Technological and Laboratory'), ('Laboratory and External', 'External and Laboratory')], default=('Technological Only', 'Technological Only'), help_text='The type of the classroom.', max_length=29, validators=[django.core.validators.MinLengthValidator(13), django.core.validators.MaxLengthValidator(29)], verbose_name='Classroom Instructure Type')),
                ('Classroom_State', models.CharField(choices=[('In-Use', 'In-Use'), ('Unlocked', 'Unlocked'), ('Locked', 'Locked')], default='Locked', help_text='The current state of the classroom. This is very different from classroom device status.', max_length=8, verbose_name='Classroom State')),
                ('Classroom_CompleteString', models.CharField(blank=True, help_text='This field is automatically filled when you submit it. Putting any value result to it, being discarded.', max_length=6, null=True, unique=True, validators=[django.core.validators.MinLengthValidator(6), django.core.validators.MaxLengthValidator(6)], verbose_name='Classroom Complete CodeName')),
                ('Classroom_Unique_ID', models.UUIDField(default=uuid.uuid4, help_text='A Unique Identifier for the classrooms. Required for unique identity for the same subject instance with different properties.', unique=True, verbose_name='Classroom Unique ID')),
            ],
            options={
                'verbose_name': 'Classroom Declaration',
                'db_table': 'classroom_decl',
                'permissions': [('classroom_viewable', 'Can view the classroom window. Used for PermissionsRequiredMixin.')],
            },
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('Course_Name', models.CharField(help_text='Please indicate. We need to know what type of room is it gonna be.', max_length=100, validators=[django.core.validators.MinLengthValidator(5), django.core.validators.MaxLengthValidator(100)], verbose_name='Course Name')),
                ('Course_Code', models.CharField(help_text='Provide Course Code with Probable In Relation to Course itself.', max_length=10, primary_key=True, serialize=False, unique=True, validators=[django.core.validators.MinLengthValidator(4), django.core.validators.MaxLengthValidator(10)], verbose_name='Course Code')),
                ('Course_Units', models.PositiveIntegerField(help_text='Units is indenpendent and user should know it based on lecture time and classroom type to use.', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(6)], verbose_name='Course Units')),
                ('Course_Capacity', models.PositiveIntegerField(default=15, help_text='The number of students that can included in the class. Minimum is 15 and Maximum is 45', validators=[django.core.validators.MinValueValidator(15), django.core.validators.MaxValueValidator(60)], verbose_name='Course Student Capacity')),
                ('Course_Type', models.CharField(choices=[('Technological Only', 'Technological Only'), ('Laboratory Only', 'Laboratory Only'), ('External Only', 'External Only'), ('Technological and Laboratory', 'Technological and Laboratory'), ('Technological and External', 'Technological and External'), ('Laboratory and Technological', 'Technological and Laboratory'), ('Laboratory and External', 'External and Laboratory')], default=('Technological Only', 'Technological Only'), help_text='Course Type is dependent, if it needs Laboratory or Technological Only. Please pick properly.', max_length=29, validators=[django.core.validators.MinLengthValidator(13), django.core.validators.MaxLengthValidator(29)], verbose_name='Course Type')),
            ],
            options={
                'verbose_name': 'Course Declaration',
                'db_table': 'course_decl',
            },
        ),
        migrations.CreateModel(
            name='DeviceInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Device_Name', models.CharField(help_text='Please indicate. We need to know what kind of device is it gonna be to communicate with the server.', max_length=100, unique=True, validators=[django.core.validators.MinLengthValidator(5), django.core.validators.MaxLengthValidator(100)], verbose_name='Device Name')),
                ('Device_Unique_ID', models.UUIDField(default=uuid.uuid4, editable=False, help_text='A Unique Identifier for the Device. This is used classroom assignment unique identity of the device.', unique=True, verbose_name='Device Unique ID')),
                ('Device_Status', models.CharField(choices=[('Online', 'Online'), ('Offline', 'Offline'), ('Unknown', 'Unknown')], default='Unknown', help_text='Status Indication of the device. Required. Basically this must match from the classroom status that is currently assigned with.', max_length=15, validators=[django.core.validators.MinLengthValidator(6), django.core.validators.MaxLengthValidator(15)], verbose_name='Device Status')),
                ('Device_IP_Address', models.GenericIPAddressField(protocol='ipv4', unique=True)),
            ],
            options={
                'verbose_name': 'Classroom MCU Device',
                'db_table': 'dev_decl',
            },
        ),
        migrations.CreateModel(
            name='ProgramBranch',
            fields=[
                ('ProgramBranch_Code', models.CharField(help_text='Declare the program code in shortest way possible', max_length=20, primary_key=True, serialize=False, unique=True, verbose_name='Program Code')),
                ('ProgramBranch_Name', models.CharField(blank=True, help_text='Declare proper names according to the typical standards in relation to Program Name.', max_length=60, null=True, verbose_name='Program Name')),
            ],
            options={
                'verbose_name': 'Department Program',
                'db_table': 'dept_programs',
            },
        ),
        migrations.CreateModel(
            name='UserDataCredentials',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('middle_name', models.CharField(blank=True, help_text='A Name that is not supplied by User Model. Added for Unique User Purposes.', max_length=20, null=True)),
                ('unique_id', models.UUIDField(default=uuid.uuid4, editable=False, help_text='A Unique Identifier for your Account. This is used for DB authentication and references. Please DO NOT SHARE IT OUTSIDE.', unique=True)),
                ('user_role', models.CharField(choices=[('Project Owner', 'Project Owner'), ('Project Administrator', 'Project Administrator'), ('ITSO Administrator', 'ITSO Administrator'), ('ITSO Member', 'ITSO Member'), ('Professor', 'Professor')], default=('Project Owner', 'Project Owner'), help_text='Roles Defined that gives users multiple actions to do. Pick one with RISK.', max_length=27)),
                ('avatar', models.ImageField(blank=True, null=True, upload_to=SCControlSystem.models.user_avatar_path)),
                ('dept_residence', models.ForeignKey(blank=True, help_text='Please refer the program code form where this staff resides.', null=True, on_delete=django.db.models.deletion.CASCADE, to='SCControlSystem.ProgramBranch', verbose_name='Staff Department Residence')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'User Credential',
                'db_table': 'user_auth_crendentials',
                'permissions': [('dashboard_viewable', 'Can view the dashboard itself. This must be allowed for everyone.'), ('user_high_level_required', 'A custom permission that can be used to distinct users from their roles. Higher level are the only available to access a particualr view.')],
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='SensOutput',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Sens_Name', models.CharField(help_text='Please indicate. We need to know what kind of sensors is it gonna be to communicate with the app.', max_length=100, validators=[django.core.validators.MinLengthValidator(5), django.core.validators.MaxLengthValidator(100)], verbose_name='Sensors Name')),
                ('Sens_Type', models.CharField(choices=[('Digital Device', 'Digital Device'), ('Analog Device', 'Analog Device'), ('Security Device', 'Security Device')], default=('Digital Device', 'Digital Device'), help_text='The type of the sensors. This needs to be indicated to properly identify what kind of output it returns.', max_length=29, validators=[django.core.validators.MinLengthValidator(13), django.core.validators.MaxLengthValidator(15)], verbose_name='Sensors Type')),
                ('Sens_Output', models.CharField(help_text='The output of the sensors can be a string, integer, float, or boolean.', max_length=255, verbose_name='Sensors Referred Output')),
                ('Sens_Date_Committed', models.DateTimeField(auto_now_add=True, help_text='The date and time from where the the output of the sensors is committed. ', verbose_name='Sensors Date Committed')),
                ('Sens_Ref', models.ForeignKey(help_text='Indication of where the data comes from.', on_delete=django.db.models.deletion.CASCADE, to='SCControlSystem.DeviceInfo', to_field='Device_Unique_ID', verbose_name='Sensors Unique Reference')),
            ],
            options={
                'verbose_name': 'Classroom Device Sensor Output',
                'db_table': 'dev_sens_output',
            },
        ),
        migrations.CreateModel(
            name='SectionGroup',
            fields=[
                ('Section_Year', models.PositiveIntegerField(choices=[(1, '1st Year'), (2, '2nd Year'), (3, '3rd Year'), (4, '4th Year'), (5, '5th Year')], help_text='Indicate the section level.', verbose_name='Section Year')),
                ('Section_Semester', models.PositiveIntegerField(choices=[(1, '1st Semester'), (2, '2nd Semester')], help_text='Indicate the section semester', verbose_name='Section Semester')),
                ('Section_SubUniqueGroup', models.CharField(choices=[('FA1', 'FA1'), ('FA2', 'FA2'), ('FA3', 'FA3'), ('FA4', 'FA4'), ('FA5', 'FA5'), ('FA6', 'FA6'), ('FA7', 'FA7'), ('FA8', 'FA8'), ('FA9', 'FA9'), ('FB1', 'FB1'), ('FB2', 'FB2'), ('FB3', 'FB3'), ('FB4', 'FB4'), ('FB5', 'FB5'), ('FB6', 'FB6'), ('FB7', 'FB7'), ('FB8', 'FB8'), ('FB9', 'FB9'), ('FC1', 'FC1'), ('FC2', 'FC2'), ('FC3', 'FC3'), ('FC4', 'FC4'), ('FC5', 'FC5'), ('FC6', 'FC6'), ('FC7', 'FC7'), ('FC8', 'FC8'), ('FC9', 'FC9')], help_text='Subunique Group that distinct other section from one another.', max_length=3, validators=[django.core.validators.MinLengthValidator(3), django.core.validators.MaxLengthValidator(3)], verbose_name='Section SubUnique Group')),
                ('Section_CompleteStringGroup', models.CharField(help_text='Combined Information into one Codename. This cannot be modified nor replaced. This is submit-dependent content value.', max_length=10, primary_key=True, serialize=False, unique=True, validators=[django.core.validators.MinLengthValidator(1), django.core.validators.MaxLengthValidator(5)], verbose_name='Section Complete Codename')),
                ('Section_Program', models.ForeignKey(help_text='Please refer the program code form where the section resides.', on_delete=django.db.models.deletion.CASCADE, to='SCControlSystem.ProgramBranch', verbose_name='Section Program')),
            ],
            options={
                'verbose_name': 'Student Section',
                'db_table': 'student_sec_decl',
            },
        ),
        migrations.CreateModel(
            name='CourseSchedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('CourseSchedule_Session_Start', models.TimeField(help_text='Refers to a time start session point.', verbose_name='Course Session Start Time')),
                ('CourseSchedule_Session_End', models.TimeField(help_text='Refers to a time end session point.', verbose_name='Course Session End Time')),
                ('CourseSchedule_Lecture_Day', models.CharField(choices=[('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesdy', 'Wednesday'), ('Thursday', 'Thursday'), ('Friday', 'Friday'), ('Saturday', 'Saturday'), ('Sunday', 'Sunday')], default=('Monday', 'Monday'), help_text='Refers to a day in which the course session takes place.', max_length=9, validators=[django.core.validators.MinLengthValidator(6), django.core.validators.MaxLengthValidator(9)], verbose_name='Course Lecture Day')),
                ('CourseSchedule_CourseReference', models.ForeignKey(help_text='Refers to a candidated subject from which allocates the time.', on_delete=django.db.models.deletion.CASCADE, to='SCControlSystem.Course', verbose_name='Course Reference')),
                ('CourseSchedule_Instructor', models.ForeignKey(help_text='Refers to an instructor who teach the following course.', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, to_field='unique_id', verbose_name='Course Instructor')),
                ('CourseSchedule_Room', models.ForeignKey(help_text='Refers to a classroom that is currently in vacant in which the session takes place.', on_delete=django.db.models.deletion.CASCADE, related_name='ClassRoomMainReference', to='SCControlSystem.Classroom', to_field='Classroom_CompleteString', verbose_name='Course Classroom Assignment')),
                ('CourseSchedule_Section', models.ForeignKey(blank=True, help_text='Refers to a section who partakes to this course.', null=True, on_delete=django.db.models.deletion.CASCADE, to='SCControlSystem.SectionGroup', verbose_name='Section Course Assignment')),
                ('CourseSchedule_Unique_ID', models.OneToOneField(blank=True, help_text='A Unique Identifier for the course schedule. Required for the unique identity which will be referenced later.', max_length=32, null=True, on_delete=django.db.models.deletion.CASCADE, to='SCControlSystem.Classroom', to_field='Classroom_Unique_ID', verbose_name='Course Schedule Unique ID')),
            ],
            options={
                'verbose_name': 'Enlisted Course Schedule',
                'db_table': 'enlisted_course_scheds',
                'permissions': [('course_schedule_viewable', 'Can view the course schedule window. Used for PermissionRequiredMixin.')],
            },
        ),
        migrations.CreateModel(
            name='ClassroomActionLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('UserActionTaken', models.CharField(choices=[('Classroom is Opened.', 'Classroom is Opened.'), ('Classroom is Closed.', 'Classroom is Closed.'), ('Action: Automatically Set as Open on Time', 'Action: Automatically Set as Open on Time'), ('Action: Automatically Set as Closed on Time', 'Action: Automatically Set as Closed on Time'), ('Authorized Staff Entry', 'Authorized Staff Entry'), ('Authorized Teacher Entry', 'Authorized Teacher Entry'), ('Disabled Access Entry', 'Disabled Access Entry'), ('Enabled Access Entry', 'Enabled Access Entry'), ('Classroom Access is set to Disabled.', 'Classroom Access is set to Disabled.'), ('Classroom Access is Disabled.', 'Classroom Access is Disabled.'), ('Forbidden Attempt To Entry Detected.', 'Forbidden Attempt To Entry Detected.'), ('Unauthorized Access Detected.', 'Unauthorized Access Detected.')], help_text='A set of action taken by the stuff and user that is recently recorded by the system.', max_length=255, verbose_name='Staff / User Action Message')),
                ('ActionLevel', models.CharField(choices=[('Info', 'Info'), ('Warning', 'Warning'), ('Alert', 'Alert')], help_text='The level of log indication. This only benefit for actions being filtered.', max_length=255, verbose_name='Log Action Level')),
                ('TimeRecorded', models.DateTimeField(auto_now_add=True, help_text="Refers to a time from where the log recorded someone's actions.", verbose_name='Log Action Recorded Time')),
                ('Course_Reference', models.ForeignKey(help_text='The course with its schedule referenced into one.', on_delete=django.db.models.deletion.CASCADE, to='SCControlSystem.CourseSchedule', verbose_name='Schedule Instance Reference')),
            ],
            options={
                'verbose_name': 'Classroom Recent Log',
                'db_table': 'classroom_action_logs',
                'permissions': [('classroom_action_log_viewable', 'Can view the classroom action log window. Used for PermissionRequiredMixin.')],
            },
        ),
        migrations.AddField(
            model_name='classroom',
            name='Classroom_Dev',
            field=models.OneToOneField(blank=True, help_text='Indication of where the device resides.', null=True, on_delete=django.db.models.deletion.CASCADE, to='SCControlSystem.DeviceInfo', verbose_name='Classroom Assigned Device'),
        ),
    ]
