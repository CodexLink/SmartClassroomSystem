from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import (AccessMixin, LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.contrib.auth.views import LoginView, LogoutView, logout_then_login
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, RedirectView, DetailView
from django.views.generic.base import TemplateView
from requests import get
from requests.exceptions import ConnectionError

from .forms import UserAuthForm
from .models import UserDataCredentials, CourseSchedule, ClassroomActionLog, Classroom

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

    permission_required = ('SCControlSystem.view_classroom',
                          'SCControlSystem.view_classroomactionlog',
                          'SCControlSystem.view_course',
                          'SCControlSystem.view_courseschedule',
                          'SCControlSystem.view_programbranch',
                          'SCControlSystem.view_sectiongroup')

    more_context = {
        "title_view": "Dashboard",
        "ClassInstance": str(__qualname__)
    }

    def get_context_data(self, **kwargs): # ! Override Get_Context_Data by adding more data.
        current_user = self.request.user
        view_context = super(DashboardView, self).get_context_data(**kwargs) # * Get the default context to override to.
        view_context['title_view'] = self.more_context['title_view']
        view_context['user_instance_name'] = '%s %s %s' % (current_user.first_name, current_user.Middle_Name if current_user.Middle_Name is not None else '', current_user.last_name)
        view_context['user_class'] = current_user.User_Role
        view_context['ClassInstance'] = self.more_context['ClassInstance']

        print(view_context)

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
        return super(DashboardView, self).handle_no_permission()

class ClassroomView(PermissionRequiredMixin, ListView):
    login_url = reverse_lazy('auth_user_view')
    template_name = template_view
    model = Classroom

    permission_required = ('SCControlSystem.view_classroom',
                          'SCControlSystem.view_classroomactionlog',
                          'SCControlSystem.view_course',
                          'SCControlSystem.view_courseschedule',
                          'SCControlSystem.view_programbranch',
                          'SCControlSystem.view_sectiongroup')

    more_context = {
        "title_view": "Classroom List",
        "ClassInstance": str(__qualname__),
    }

    def get_context_data(self, **kwargs): # ! Override Get_Context_Data by adding more data.
        current_user = self.request.user
        view_context = super(ClassroomView, self).get_context_data(**kwargs) # * Get the default context to override to.
        view_context['title_view'] = self.more_context['title_view']
        view_context['user_instance_name'] = '%s %s %s' % (current_user.first_name, current_user.Middle_Name if current_user.Middle_Name is not None else '', current_user.last_name)
        view_context['user_class'] = current_user.User_Role
        view_context['ClassInstance'] = self.more_context['ClassInstance']

        return view_context

    #def sendMCUData(self):
    #    try:
    #        return requests.get("http://192.168.100.41/RequestSens", timeout=.1)
    #    except ConnectionError as Err:
    #        return None
    #        #self.response.text = None
    #        pass

class SelectableClassroomView(PermissionRequiredMixin, DetailView):
    login_url = reverse_lazy('auth_user_view')
    template_name = template_view
    model = Classroom
    permission_required = ('SCControlSystem.view_classroom',
                          'SCControlSystem.view_course',
                          'SCControlSystem.view_courseschedule',
                          'SCControlSystem.view_programbranch',
                          'SCControlSystem.view_sectiongroup')

    more_context = {
        "title_view": "Classroom Control View",
        "ClassInstance": str(__qualname__),
    }

    def get_context_data(self, **kwargs): # ! Override Get_Context_Data by adding more data.
        current_user = self.request.user
        view_context = super(SelectableClassroomView, self).get_context_data(**kwargs) # * Get the default context to override to.
        view_context['title_view'] = self.more_context['title_view']
        view_context['user_instance_name'] = '%s %s %s' % (current_user.first_name, current_user.Middle_Name if current_user.Middle_Name is not None else '', current_user.last_name)
        view_context['user_class'] = current_user.User_Role
        view_context['ClassInstance'] = self.more_context['ClassInstance']

        print(view_context)

        return view_context # ! Return the Context to be rendered later on.




    def get(self, request, classRoomID=None):
        return render(request, template_view, self.more_context)

    def post(self, request, classRoomID=None):
        pass


class ScheduleListView(PermissionRequiredMixin, ListView):
    login_url = reverse_lazy('auth_user_view')
    template_name = template_view
    model = CourseSchedule

    permission_required = ('SCControlSystem.view_classroom',
                      'SCControlSystem.view_course',
                      'SCControlSystem.view_courseschedule',
                      'SCControlSystem.view_programbranch',
                      'SCControlSystem.view_sectiongroup')

    more_context = {
        "title_view": "Your Schedules",
        "ClassInstance": str(__qualname__),
    }

    def get_context_data(self, **kwargs): # ! Override Get_Context_Data by adding more data.
        current_user = self.request.user
        view_context = super(ScheduleListView, self).get_context_data(**kwargs) # * Get the default context to override to.
        view_context['title_view'] = self.more_context['title_view']
        view_context['user_instance_name'] = '%s %s %s' % (current_user.first_name, current_user.Middle_Name if current_user.Middle_Name is not None else '', current_user.last_name)
        view_context['user_class'] = current_user.User_Role
        view_context['ClassInstance'] = self.more_context['ClassInstance']

        print(view_context)

        return view_context # ! Return the Context to be rendered later on.

# ! Authentication Classes

# ! AuthUserView Requires LoginView To Provide Minimal Configuration
class AuthUserView(LoginView):
    form = UserAuthForm # ! Declare Our Form To Be Used.
    template_name = template_view # * Use Global Variable Later
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

    permission_required = ('SCControlSystem.view_classroom',
                      'SCControlSystem.view_course',
                      'SCControlSystem.view_courseschedule',
                      'SCControlSystem.view_programbranch',
                      'SCControlSystem.view_sectiongroup')

    more_context = {
        "title_view": "Actions Data Log",
        "ClassInstance": str(__qualname__),
    }

    def get_context_data(self, **kwargs): # ! Override Get_Context_Data by adding more data.
        current_user = self.request.user
        view_context = super(StaffActionsListView, self).get_context_data(**kwargs) # * Get the default context to override to.
        view_context['title_view'] = self.more_context['title_view']
        view_context['user_instance_name'] = '%s %s %s' % (current_user.first_name, current_user.Middle_Name if current_user.Middle_Name is not None else '', current_user.last_name)
        view_context['user_class'] = current_user.User_Role
        view_context['ClassInstance'] = self.more_context['ClassInstance']

        print(view_context)

        return view_context # ! Return the Context to be rendered later on.
