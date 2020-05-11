from django.urls import include, path
from django.contrib import admin
from .views import *

urlpatterns = [
    # ! Universal Accesible URLs
    path("", DashboardView.as_view(), name="dashboard_user_view"),
    path("login/", AuthUserView.as_view(), name="auth_user_view"),
    path("logout/", DeauthUserView.as_view(), name="deauth_user_view"),
    path("logs/", StaffActionsListView.as_view(), name="staff_action_logs_view"),
    # ! Staff Only Accesible URLs
    path(
        "classroom/<uuid:classUniqueID>/",
        include(
            [
                path(
                    "control/",
                    SelectableClassroomView.as_view(),
                    name="classroom_info_view",
                ),
                path(
                    "control/crUpdate/",
                    SelectableClassroomView.as_view(ActionState="ClassroomAccess"),
                    name="classroom_take_action_cr_access",
                ),
                path(
                    "control/lockInitiate/",
                    SelectableClassroomView.as_view(ActionState="LockDoorAccess"),
                    name="classroom_take_action_lock_state",
                ),
                path(
                    "control/electricStateUpdate/",
                    SelectableClassroomView.as_view(ActionState="ElectricityAccess"),
                    name="classroom_take_action_electric_state",
                ),
                path(
                    "control/devReset/",
                    SelectableClassroomView.as_view(ActionState="DevRestart"),
                    name="classroom_take_action_device_reset",
                ),
            ]
        ),
    ),
    path(
        "classroom/schedule/",
        ScheduleListView.as_view(),
        name="schedule_exclusive_view",
    ),  # ! For teachers only.
    # ! Admin Only URLs
    path("classroom/", ClassroomView.as_view(), name="classroom_user_view"),
    path("override/", admin.site.urls),
]
