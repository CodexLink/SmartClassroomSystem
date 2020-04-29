# ! Multiple Subjected Declared Types by Janrey "CodexLink" Licas
# * Created o 01/025/2020

# * For Course Lecture Classification.
CourseSessionTypes = (
    ("Technological Only", "Technological Only"),
    ("Laboratory Only", "Laboratory Only"),
    ("External Only", "External Only"),
    ("Technological and Laboratory", "Technological and Laboratory"),
    ("Technological and External", "Technological and External"),
    ("Laboratory and Technological", "Technological and Laboratory"),
    ("Laboratory and External", "External and Laboratory"),
)

YearBatchClasses = (
    (1, "1st Year"),
    (2, "2nd Year"),
    (3, "3rd Year"),
    (4, "4th Year"),
    (5, "5th Year"),
)

# ! Based from https://www.tip.edu.ph/Engineering_and_Architecture_QC_Branch
# ! CEA Only, I'm doing over-effort, please stop thanks.
CEAProgramCCode = (
    ("ARch", "Architecture"),
    ("CE", "Civil Engineering"),
    ("CpE", "Computer Engineering"),
    ("EE", "Electrical Engineering"),
    ("ECE", "Electronics Engineering"),
    ("EnSE", "Environment and Sanitary Engineering"),
    ("IE", "Industrial Engineering"),
    ("ME", "Mechanical Engineering"),
    ("NA", "Administrative Account"),
)

# * For Semester Indication Only.
SemClassification = ((1, "1st Semester"), (2, "2nd Semester"))

# ! Declared Weekdays and Weekends for Proper Declaration at DB
SessionDaysClassification = (
    ("Monday", "Monday"),
    ("Tuesday", "Tuesday"),
    ("Wednesday", "Wednesday"),
    ("Thursday", "Thursday"),
    ("Friday", "Friday"),
    ("Saturday", "Saturday"),
    ("Sunday", "Sunday"),
)

BuildingClassification = (
    (1, "Building 1"),
    (2, "Building 2"),
    (3, "Building 3"),
    (4, "Building 4"),
    (5, "Building 5"),
    (6, "Building 6"),
    (7, "Building 7"),
    (8, "Building 8"),
    (9, "Building 9"),
    (10, "PE CNTR 1"),
    (11, "PE CNTR 2"),
)

BuildingFloors = (
    (1, "Ground Floor"),
    (2, "2nd Floor"),
    (3, "3rd Floor"),
    (4, "4th Floor"),
    (5, "5th Floor"),
)

# ! Classroom Action Logs
ClassroomActionTypes = (
    (
        "Classroom was Opened by Toggle Lock.",
        "Classroom was Opened by Toggle Lock.",
    ),  # 0
    (
        "Classroom was Closed by Toggle Lock.",
        "Classroom was Closed by Toggle Lock.",
    ),  # 1
    (
        "Classroom was Opened by Fingerprint.",
        "Classroom was Opened by Fingerprint.",
    ),  # 2
    (
        "Classroom was Closed by Fingerprint.",
        "Classroom was Closed by Fingerprint.",
    ),  # 3
    (
        "Classroom Electricity was Turned On.",
        "Classroom Electricity was Turned On.",
    ),  # 4
    (
        "Classroom Electricity was Turned Off.",
        "Classroom Electricity was Turned Off.",
    ),  # 5
    ("Device was Reset by a Staff.", "Device was reset by a Staff."),  # 6
    (
        "Classroom Access was set to Disabled.",
        "Classroom Access was set to Disabled.",
    ),  # 7
    (
        "Classroom Access was set to Enabled.",
        "Classroom Access was set to Enabled.",
    ),  # 8
    ("Unauthorized Device Reset Detected", "Unauthorized Device Reset Detected"),  # 9
    (
        "Unauthorized Access Change Detected",
        "Unauthorized Access Change Detected",
    ),  # 10
    ("Unauthorized Access Detected.", "Unauthorized Access Detected."),  # 11
    ("Authorized Access Passed.", "Authorized Access Passed."),  # 12
)

# ! Logging Level Declarations
LevelAlert = (("Info", "Info"), ("Warning", "Warning"), ("Alert", "Alert"))

# * Included Only Possible Class Occupation
SubSectionUniqueKeys = (
    ("FA1", "FA1"),
    ("FA2", "FA2"),
    ("FA3", "FA3"),
    ("FA4", "FA4"),
    ("FA5", "FA5"),
    ("FA6", "FA6"),
    ("FA7", "FA7"),
    ("FA8", "FA8"),
    ("FA9", "FA9"),
    ("FB1", "FB1"),
    ("FB2", "FB2"),
    ("FB3", "FB3"),
    ("FB4", "FB4"),
    ("FB5", "FB5"),
    ("FB6", "FB6"),
    ("FB7", "FB7"),
    ("FB8", "FB8"),
    ("FB9", "FB9"),
    ("FC1", "FC1"),
    ("FC2", "FC2"),
    ("FC3", "FC3"),
    ("FC4", "FC4"),
    ("FC5", "FC5"),
    ("FC6", "FC6"),
    ("FC7", "FC7"),
    ("FC8", "FC8"),
    ("FC9", "FC9"),
)
"""
# ! Human Declared Types
* ### Concept Roles To Be Used in DJango. Confirmed correlated with Group Model.
# ! Will still be used on Database-Level.
"""
RoleDeclaredTypes = (
    ("Project Owner", "Project Owner"),
    ("Project Administrator", "Project Administrator"),
    ("ITSO Administrator", "ITSO Administrator"),
    ("ITSO Supervisor", "ITSO Supervisor"),
    ("Professor", "Professor"),
)

# ! Group Name Definition based Human Roles, Unrelated to Model ATM.
GroupDefinitionRoles = (
    "Project Owners",
    "Project Administrators",
    "ITSO Administrators",
    "ITSO Supervisors",
    "Professors",
)

# ! Device Types Declaration
DevDeclarationTypes = (
    ("Digital Device", "Digital Device"),
    ("Analog Device", "Analog Device"),
    ("Security Device", "Security Device"),
)

ClassroomStates = (
    ("Unlocked", "Unlocked"),
    ("Locked", "Locked"),
)

ClassroomAccessStates = (
    ("Enabled", "Enabled"),
    ("Disabled", "Disabled"),
)

ClassrooAvailabilityStates = (
    ("Undetermined", "Undetermined"),
    ("Available", "Available"),
    ("Not Available", "Not Available"),
)

DeviceStates = (
    ("Online", "Online"),
    ("Offline", "Offline"),
)
