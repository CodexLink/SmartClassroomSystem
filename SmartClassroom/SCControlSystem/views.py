from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import (AccessMixin, LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.contrib.auth.views import LoginView, LogoutView, logout_then_login
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, RedirectView, DetailView, FormView
from django.views.generic.base import TemplateView
from requests import get
from requests.exceptions import ConnectionError

from .forms import UserAuthForm
from .models import *
import datetime

# ! Global Variables !
template_view = 'elem_inst_view.html'

# ! A Class That Just Loads the Default "home.html"
class HomeView(TemplateView):
    template_name = template_view

    more_context = {
        "title_view": "Welcome",
        "ClassInstance": str(__qualname__),
    }

    # ! Override Get_Context_Data by adding more data.
    def get_context_data(self, **kwargs):
        view_context = super(HomeView, self).get_context_data(**kwargs) # * Get the default context to override to.
        view_context['title_view'] = self.more_context['title_view']
        view_context['ClassInstance'] = self.more_context['ClassInstance']

        return view_context # ! Return the Context to be rendered later on.

class DashboardView(PermissionRequiredMixin, TemplateView):
    login_url = reverse_lazy('auth_user_view')
    template_name = template_view
    redirect_field_name = reverse_lazy('deauth_user_view')

    permission_required = 'SCControlSystem.dashboard_viewable'

    more_context = {
        "title_view": "Dashboard",
        "ClassInstance": str(__qualname__)
    }

    def get_context_data(self, **kwargs): # ! Override Get_Context_Data by adding more data.
        current_user = self.request.user
        view_context = super(DashboardView, self).get_context_data(**kwargs) # * Get the default context to override to.
        view_context['title_view'] = self.more_context['title_view']
        view_context['user_instance_name'] = '%s %s %s' % (current_user.first_name, current_user.middle_name if current_user.middle_name is not None else '', current_user.last_name)
        view_context['user_class'] = current_user.user_role
        view_context['ClassInstance'] = self.more_context['ClassInstance']
        view_context['refresh_recent_time'] = datetime.datetime.now().time().strftime('%I:%M%p')

        # ! More Objects To Display at.
        if not current_user.user_role == "Professor":
            view_context['cr_unlocked_count'] = DeviceInfo.objects.filter(Device_Status='Unlocked').count()
            view_context['cr_locked_count'] = DeviceInfo.objects.filter(Device_Status='Locked').count()
            view_context['cr_in_use_count'] = DeviceInfo.objects.filter(Device_Status='In-Use').count()

            view_context['dev_offline_count'] = DeviceInfo.objects.filter(Device_Status='Offline').count()
            view_context['dev_online_count'] = DeviceInfo.objects.filter(Device_Status='Locked').count()
            view_context['dev_unknown_count'] = DeviceInfo.objects.filter(Device_Status='Unknown').count()

            # ! Admin View for Classroom Systems
            view_context['dev_offline_candidates'] = DeviceInfo.objects.filter(Device_Status='Offline').select_related('classroom')
            view_context['dev_online_candidates'] = DeviceInfo.objects.filter(Device_Status='Online').select_related('classroom')
            view_context['dev_unknown_candidates'] = DeviceInfo.objects.filter(Device_Status='Unknown').select_related('classroom')

            view_context['classroom_logs'] = ClassroomActionLog.objects.all().order_by('-TimeRecorded')[:5]

        elif current_user.user_role == "Professor":
            view_context['schedule_weekday_name'] = datetime.datetime.today().strftime('%A')
            # ! We currently looking at foreign key here.
            view_context['schedule_candidates'] = CourseSchedule.objects.filter(CourseSchedule_Instructor__first_name=current_user.first_name, CourseSchedule_Instructor__middle_name=current_user.middle_name, CourseSchedule_Instructor__last_name=current_user.last_name, CourseSchedule_Lecture_Day=view_context['schedule_weekday_name']).order_by('CourseSchedule_Session_Start')
            view_context['classroom_logs'] = ClassroomActionLog.objects.filter(Course_Reference__CourseSchedule_Instructor__first_name=current_user.first_name, Course_Reference__CourseSchedule_Instructor__middle_name=current_user.middle_name, Course_Reference__CourseSchedule_Instructor__last_name=current_user.last_name).order_by('-TimeRecorded')[:5]

        return view_context # ! Return the Context to be rendered later on.

    # ! Here, we have to determine if user is authenticated at this point.
    # * If it is, then DO NOT redirect to login page.
    # * Else, then DO redirect to login page.
    def handle_no_permission(self):
        self.raise_exception = self.request.user.is_authenticated
        if self.raise_exception:
            messages.error(self.request, "InsufficientPermission")
        else:
            messages.error(self.request, "PermissionAccessDenied")
        print(self.get_permission_required())
        return super(DashboardView, self).handle_no_permission()

class ClassroomView(PermissionRequiredMixin, ListView):
    login_url = reverse_lazy('auth_user_view')
    template_name = template_view
    model = Classroom
    queryset = Classroom.objects.all().order_by('Classroom_CompleteString')

    permission_required = ('SCControlSystem.user_high_level_required', 'SCControlSystem.classroom_viewable')

    more_context = {
        "title_view": "Classroom List",
        "ClassInstance": str(__qualname__),
    }

    def get_context_data(self, **kwargs): # ! Override Get_Context_Data by adding more data.
        current_user = self.request.user
        view_context = super(ClassroomView, self).get_context_data(**kwargs) # * Get the default context to override to.
        view_context['title_view'] = self.more_context['title_view']
        view_context['user_instance_name'] = '%s %s %s' % (current_user.first_name, current_user.middle_name if current_user.middle_name is not None else '', current_user.last_name)
        view_context['user_class'] = current_user.user_role
        view_context['ClassInstance'] = self.more_context['ClassInstance']
        return view_context

class SelectableClassroomView(PermissionRequiredMixin, ListView):
    login_url = reverse_lazy('auth_user_view')
    template_name = template_view
    model = CourseSchedule # ! We use CourseSchedule Model Instead of Classroom. Because Inheritance

    slug_url_kwarg = 'classUniqueID'

    # ! ADD SCHEDULE VIEWABLE
    permission_required = ('SCControlSystem.classroom_viewable',
                          'SCControlSystem.classroom_action_log_viewable',
                          )

    more_context = {
        "title_view": "Classroom Control View",
        "ClassInstance": str(__qualname__),
    }

    def get_queryset(self):
        return CourseSchedule.objects.filter(CourseSchedule_Room__Classroom_Unique_ID=self.kwargs['classUniqueID'])

    def get_context_data(self, **kwargs): # ! Override Get_Context_Data by adding more data.
        current_user = self.request.user
        view_context = super(SelectableClassroomView, self).get_context_data(**kwargs) # * Get the default context to override to.
        view_context['title_view'] = self.more_context['title_view']
        view_context['user_instance_name'] = '%s %s %s' % (current_user.first_name, current_user.middle_name if current_user.middle_name is not None else '', current_user.last_name)
        view_context['user_class'] = current_user.user_role
        view_context['ClassInstance'] = self.more_context['ClassInstance']
        view_context['refresh_recent_time'] = datetime.datetime.now().time().strftime('%I:%M%p')

        if not current_user.user_role == "Professor":
            view_context['ClassLogs'] = ClassroomActionLog.objects.filter(Course_Reference__CourseSchedule_Room__Classroom_Unique_ID=self.kwargs['classUniqueID']).order_by('-TimeRecorded')
            view_context['SubjectsInvolved'] = CourseSchedule.objects.filter(CourseSchedule_Room__Classroom_Unique_ID=self.kwargs['classUniqueID']).order_by('-CourseSchedule_Session_Start')
        else:
            # ! Add More Context. Do not really just on classlogs
            view_context['ClassLogs'] = ClassroomActionLog.objects.filter(Course_Reference__CourseSchedule_Instructor__first_name=current_user.first_name, Course_Reference__CourseSchedule_Instructor__middle_name=current_user.middle_name, Course_Reference__CourseSchedule_Instructor__last_name=current_user.last_name, Course_Reference__CourseSchedule_Room__Classroom_Unique_ID=self.kwargs['classUniqueID']).order_by('-TimeRecorded')


        print(self.kwargs['classUniqueID']) # ! Return the Context to be rendered later on.
        print(view_context['SubjectsInvolved']) # ! Return the Context to be rendered later on.
        return view_context # ! Return the Context to be rendered later on.

class ScheduleListView(PermissionRequiredMixin, ListView):
    login_url = reverse_lazy('auth_user_view')
    template_name = template_view
    model = CourseSchedule

    permission_required = 'SCControlSystem.course_schedule_viewable'

    more_context = {
        "title_view": "Your Schedules",
        "ClassInstance": str(__qualname__),
    }

    def get_queryset(self):
        return CourseSchedule.objects.filter(CourseSchedule_Instructor__first_name=self.request.user.first_name, CourseSchedule_Instructor__middle_name=self.request.user.middle_name, CourseSchedule_Instructor__last_name=self.request.user.last_name).order_by('-CourseSchedule_Session_Start')

    def get_context_data(self, **kwargs): # ! Override Get_Context_Data by adding more data.
        current_user = self.request.user
        view_context = super(ScheduleListView, self).get_context_data(**kwargs) # * Get the default context to override to.
        view_context['title_view'] = self.more_context['title_view']
        view_context['user_instance_name'] = '%s %s %s' % (current_user.first_name, current_user.middle_name if current_user.middle_name is not None else '', current_user.last_name)
        view_context['user_class'] = current_user.user_role
        view_context['ClassInstance'] = self.more_context['ClassInstance']
        view_context['schedule_weekday_name'] = datetime.datetime.today().strftime('%A')
        return view_context # ! Return the Context to be rendered later on.

# ! Authentication Classes

# ! AuthUserView Requires LoginView To Provide Minimal Configuration
class AuthUserView(LoginView):
    template_name = template_view # * Use Global Variable Later
    form_class = UserAuthForm # ! Declare Our Form To Be Used.
    success_url = reverse_lazy('dashboard_user_view') # ! This renders URL later when login is success.
    redirect_authenticated_user = True

    # ! We provide more context to the form when it request by GET.
    more_context = {
        "title_view": "User Login",
        "ClassInstance": str(__qualname__),
    }


    # ! Override Get_Context_Data by adding more data.
    def get_context_data(self, **kwargs):
        view_context = super(AuthUserView, self).get_context_data(**kwargs) # * Get the default context to override to.
        view_context['title_view'] = self.more_context['title_view'] # ! Add Extra Field Called "TITLE_VIEW" and insert data to it.
        view_context['ClassInstance'] = self.more_context['ClassInstance'] # ! And so on.

        return view_context # ! Return the Context to be rendered later on.

    def get_success_url(self):
        return self.success_url # * We get redirect to the value of this attribute.

# ! DeauthUserView Requires LogoutView To Provide Minimal Configuration
# * This view is literally the same as AuthUserView except it is very minimal because it only displays few things.
# * And it automatically logs out user that is currently logged in the session.
# ! This does not go back if user is not authenticated anymore, so this class is casted with LoginRequiredMixin.
class DeauthUserView(LoginRequiredMixin, LogoutView):
    template_name = template_view # ! We use the same as always except we render it with different view.

    # *Bit of redundant here, login_url used by LogoutView and next_page was used by LoginRequiredMixins
    login_url = reverse_lazy('auth_user_view')
    next_page = login_url

    # ! We override this function upon page load.
    def dispatch(self, request):
        # ! Message outputs the same when user tries to log out.
        # * To filter things out, we have to check if user really is authenticated before outputting message that is added below.
        if request.user.is_authenticated:
            messages.success(self.request, "UserLoggedOut")
        return super(DeauthUserView, self).dispatch(request)

    # ! Handle This To Render from Login
    def handle_no_permission(self):
        # ! We output message if user attempts to access this page.
        messages.error(self.request, "UserAlreadyLoggedOut")
        return super(DeauthUserView ,self).handle_no_permission()

# ! Contains multiple logs that can is subjected for review.
class StaffActionsListView(PermissionRequiredMixin, ListView):
    login_url = reverse_lazy('auth_user_view')
    template_name = template_view
    model = ClassroomActionLog

    permission_required = 'SCControlSystem.classroom_action_log_viewable'

    more_context = {
        "title_view": "Action Logs",
        "ClassInstance": str(__qualname__),
    }

    def get_queryset(self):
        if not self.request.user.user_role == "Professor":
            return ClassroomActionLog.objects.all().order_by('-TimeRecorded')
        else:
            return ClassroomActionLog.objects.filter(Course_Reference__CourseSchedule_Instructor__first_name=self.request.user.first_name, Course_Reference__CourseSchedule_Instructor__middle_name=self.request.user.middle_name, Course_Reference__CourseSchedule_Instructor__last_name=self.request.user.last_name).order_by('-TimeRecorded')

    def get_context_data(self, **kwargs): # ! Override Get_Context_Data by adding more data.
        current_user = self.request.user
        view_context = super(StaffActionsListView, self).get_context_data(**kwargs) # * Get the default context to override to.
        view_context['title_view'] = self.more_context['title_view']
        view_context['user_instance_name'] = '%s %s %s' % (current_user.first_name, current_user.middle_name if current_user.middle_name is not None else '', current_user.last_name)
        view_context['user_class'] = current_user.user_role
        view_context['ClassInstance'] = self.more_context['ClassInstance']
        return view_context # ! Return the Context to be rendered later on.