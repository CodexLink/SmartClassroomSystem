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
    # ! Universal Accesible URLs
    path('', HomeView.as_view(), name='front_project_view'),
    path('login/', AuthUserView.as_view(), name='auth_user_view'),
    path('logout/', DeauthUserView.as_view(), name='deauth_user_view'),
    path('dashboard/', DashboardView.as_view(), name='dashboard_user_view'),
    path('logs/', StaffActionsListView.as_view(), name='staff_action_logs_view'),
    # ! Staff Only Accesible URLs
    path('classroom/<uuid:classUniqueID>/control/', SelectableClassroomView.as_view(), name='classroom_info_view'),
    path('schedule/', ScheduleListView.as_view(), name='schedule_exclusive_view'), # ! For teachers only.
    # ! Admin Only URLs
    path('classroom/', ClassroomView.as_view(), name='classroom_user_view'),
    path('override/', admin.site.urls),
]
