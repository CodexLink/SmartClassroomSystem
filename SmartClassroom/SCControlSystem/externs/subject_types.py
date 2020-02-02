# ! Multiple Subjected Declared Types by Janrey "CodexLink" Licas
# * Created o 01/025/2020

# * For Course Lecture Classification.
CourseSessionTypes = (
    ('Technological Only', 'Technological Only'),
    ('Laboratory Only', 'Laboratory Only'),
    ('External Only', 'External Only'),
    ('Technological and Laboratory', 'Technological and Laboratory'),
    ('Technological and External', 'Technological and External'),
    ('Laboratory and Technological', 'Technological and Laboratory'),
    ('Laboratory and External', 'External and Laboratory'),
)

YearBatchClasses = (
    (1, '1st Year'),
    (2, '2nd Year'),
    (3, '3rd Year'),
    (4, '4th Year'),
    (5, '5th Year')
)

# ! Based from https://www.tip.edu.ph/Engineering_and_Architecture_QC_Branch
# ! CEA Only, I'm doing over-effort, please stop thanks.
CEAProgamCCode = (
    ('ARch', 'Architecture'),
    ('CE', 'Civil Engineering'),
    ('CpE', 'Computer Engineering'),
    ('EE', 'Electrical Engineering'),
    ('ECE', 'Electronics Engineering'),
    ('EnSE', 'Environment and Sanitary Engineering'),
    ('IE', 'Industrial Engineering'),
    ('ME', 'Mechanical Engineering')
)

# * For Semester Indication Only.
SemClassification = (
    (1, '1st Semester'),
    (2, '2nd Semester')
)

# ! Declared Weekdays and Weekends for Proper Declaration at DB
SessionDaysClassification = (
    ('Monday', 'Monday'),
    ('Tuesday', 'Tuesday'),
    ('Wednesdy', 'Wednesday'),
    ('Thursday', 'Thursday'),
    ('Friday', 'Friday'),
    ('Saturday', 'Saturday'),
    ('Sunday', 'Sunday')
)

BuildingClassification = (
    (1, 'Building 1'),
    (2, 'Building 2'),
    (3, 'Building 3'),
    (4, 'Building 4'),
    (5, 'Building 5'),
    (6, 'Building 6'),
    (7, 'Building 7'),
    (8, 'Building 8'),
    (9, 'Building 9'),
    (10, 'PE CNTR 1'),
    (11, 'PE CNTR 2')
)

BuildingFloors = (
    (1, 'Ground Floor'),
    (2, '2nd Floor'),
    (3, '3rd Floor'),
    (4, '4th Floor'),
    (5, '5th Floor')
)

# ! Classroom Action Logs
ClassroomActionTypes = (
    ('Opened Classroom', 'Opened Classroom'),
    ('Closed Classroom', 'Closed Classroom'),
    ('Action: Automatically Set as Open on Time',
     'Action: Automatically Set as Open on Time'),
    ('Action: Automatically Set as Closed on Time',
     'Action: Automatically Set as Closed on Time'),
    ('Authorized Staff Entry', 'Authorized Staff Entry'),
    ('Authorized Teacher Entry', 'Authorized Teacher Entry'),
    ('Disabled Access Entry', 'Disabled Access Entry'),
    ('Enabled Access Entry', 'Enabled Access Entry'),
    ('Classroom Access is set to Disabled.',
     'Classroom Access is set to Disabled.'),
    ('Classroom Access is Disabled.', 'Classroom Access is Disabled.'),
    ('Forbidden Attempt To Entry Detected.',
     'Forbidden Attempt To Entry Detected.'),
    ('Unauthorized Access Detected.', 'Unauthorized Access Detected.'),
)

# * Included Only Possible Class Occupation
SubSectionUniqueKeys = (
    ('FA1', 'FA1'),
    ('FA2', 'FA2'),
    ('FA3', 'FA3'),
    ('FA4', 'FA4'),
    ('FA5', 'FA5'),
    ('FA6', 'FA6'),
    ('FA7', 'FA7'),
    ('FA8', 'FA8'),
    ('FA9', 'FA9'),
    ('FB1', 'FB1'),
    ('FB2', 'FB2'),
    ('FB3', 'FB3'),
    ('FB4', 'FB4'),
    ('FB5', 'FB5'),
    ('FB6', 'FB6'),
    ('FB7', 'FB7'),
    ('FB8', 'FB8'),
    ('FB9', 'FB9'),
    ('FC1', 'FC1'),
    ('FC2', 'FC2'),
    ('FC3', 'FC3'),
    ('FC4', 'FC4'),
    ('FC5', 'FC5'),
    ('FC6', 'FC6'),
    ('FC7', 'FC7'),
    ('FC8', 'FC8'),
    ('FC9', 'FC9'),
)

'''
# ! Human Declared Types
* ### Concept Roles To Be Used in DJango. Confirmed correlated with Group Model.
# ! Will still be used on Database-Level.
'''
RoleDeclaredTypes = (
    ("Project Owner", "Project Owner"),
    ("Project Member", "Project Member"),
    ("ITSO Administrator", "ITSO Administrator"),
    ("ITSO Member", "ITSO Member"),
    ("Professor Staff", "Professor Staff"),
    ("Student Staff", "Student Staff"),
)

# ! Group Name Definition based Human Roles
GroupDefinitionRoles = (
    "Project Owner",
    "Project Members",
    "ITSO Administrators",
    "ITSO Members",
    "Professors",
    "Students"
)
