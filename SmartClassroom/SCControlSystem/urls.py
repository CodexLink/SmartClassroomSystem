"""SmartClassroom URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from .views import *

urlpatterns = [
    path('', HomeView.as_view(), name='front_project_view'),
    path('login/', AuthUserView.as_view(), name='auth_user_view'),
    path('logout/', DeauthUserView.as_view(), name='deauth_user_view'),
    path('dashboard/', DashboardView.as_view(), name='dashboard_user_view'),
    path('classroom/', ClassroomView.as_view(), name='classroom_user_view'),
    # ! Check for possible options here, URL Parameters.
    path('logs/', StaffActionsListView.as_view(), name='staff_action_logs_view'),
    # ! Not confirmed yet.
    path('classroom/<str:classRoomID>/logs/', SelectableClassroomView.as_view(path_action='check_log', as_modular_view=False), name='classroom_log_extensible_view'), # ! Extensible means usable as whole page or modular component.
    path('classroom/<str:classRoomID>/info/', SelectableClassroomView.as_view(path_action='show_info'), name='classroom_info_view'),
    path('classroom/<str:classRoomID>/schedule/', SelectableClassroomView.as_view(path_action='show_selected_schedule'), name='classroom_schedule_view'),
    path('classroom/<str:classRoomID>/actions/', SelectableClassroomView.as_view(path_action='get_actions'), name='classroom_action_view'),
    path('schedule/', ScheduleListView.as_view(), name='schedule_exclusive_view'), # ! For teachers only.
    path('override/', OverrideControlView.as_view(), name='override_exclusive_view'),
    path('system/', SystemSettingsView.as_view(), name='syssettings_exclusive_view')
]
