from django.views.generic.base import TemplateView
from django.views.generic import ListView, RedirectView
from django.contrib.auth.views import LoginView, LogoutView, logout_then_login
from django.contrib.auth import login, logout
from django.shortcuts import render
from requests import get
from .models import UserDataCredentials
from .forms import UserAuthForm
from requests.exceptions import ConnectionError
from django.urls import reverse_lazy

# ! Global Variables !
template_view = 'elem_inst_view.html'

# ! A Class That Just Loads the Default "home.html"
class HomeView(TemplateView):

    more_context = {
        "title_view": "Welcome",
        "ClassInstance": str(__qualname__),
    }

    def get(self, request):
        return render(request, template_view, self.more_context)

    def sendMCUData(self):
        try:
            return requests.get("http://192.168.100.41/RequestSens", timeout=.1)
        except ConnectionError as Err:
            return None
            #self.response.text = None
            pass


class DashboardView(TemplateView):
    more_context = {
        "title_view": "Dashboard",
        "user_class": "Admin",
        "user_instance_name": "Janrey Licas",
        "ClassInstance": str(__qualname__),
    }

    # ! User Instance Type is already passable so creating variable is useless.

    def get(self, request):
        return render(request, template_view, self.more_context)

    def post(self, request):
        pass

    def sendMCUData(self):
        try:
            return requests.get("http://192.168.100.41/RequestSens", timeout=.1)
        except ConnectionError as Err:
            return None
            #self.response.text = None
            pass


class ClassroomView(ListView):
    path_action = None  # ! Unknown Usage Yet.
    as_modular_view = None  # ! Optional and limited only to logs and info.

    more_context = {
        "title_view": "Classroom List",
        "user_class": "Admin",
        "ClassInstance": str(__qualname__),
    }


    def get(self, request):
        return render(request, template_view, self.more_context)

    def post(self, request):
        pass


class SelectableClassroomView(TemplateView):
    # ! Optional, but mostly used. The 3rd part of URL is the one that is being used.
    path_action = None
    as_modular_view = None  # ! Optional and limited only to logs and info.


    more_context = {
        "title_view": "Classroom",
        "user_class": "Admin",
        "ClassInstance": str(__qualname__),
    }


    def get(self, request, classRoomID=None):
        return render(request, template_view, self.more_context)

    def post(self, request, classRoomID=None):
        pass


class ScheduleListView(ListView):
    path_action = None
    as_modular_view = None  # ! Optional and limited only to logs and info.

    more_context = {
        "title_view": "Classroom",
        "user_class": "Admin",
        "ClassInstance": str(__qualname__),
    }

    def get(self, request):
        return render(request, template_view, self.more_context)

    def post(self, request):
        pass


class OverrideControlView(TemplateView):
    path_action = None
    as_modular_view = None  # ! Optional and limited only to logs and info.

    more_context = {
        "title_view": "Override",
        "user_class": "Admin",
        "ClassInstance": str(__qualname__),
    }

    def get(self, request):
        return render(request, template_view, self.more_context)

    def post(self, request):
        pass


class SystemSettingsView(TemplateView):
    path_action = None

    more_context = {
        "title_view": "System Overview",
        "user_class": "Admin",
        "ClassInstance": str(__qualname__),
    }

    def get(self, request):
        return render(request, template_view, self.more_context)

    def post(self, request):
        pass

# ! Authentication Classes

# ! AuthUserView Requires LoginView To Provide Minimal Configuration
class AuthUserView(LoginView):
    form = UserAuthForm # ! Declare Our Form To Be Used.
    template_name = template_view # * Use Global Variable Later
    success_url = reverse_lazy('dashboard_user_view') # ! This renders URL later when login is success.
    redirect_authenticated_user = True

    # ! We provide more context to the form when it request by GET.
    more_context = {
        "title_view": "Login View",
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

class DeauthUserView(LogoutView):

    more_context = {
        "title_view": "Logout View",
        "ClassInstance": str(__qualname__),
    }

    template_name = 'login.html'
    login_url = reverse_lazy('dashboard_user_view')

    #def get_context_data(self, **kwargs):
    #    view_context = super(DeauthUserView, self).get_context_data(**kwargs) # * Get the default context to override to.
    #    view_context['title_view'] = self.more_context['title_view'] # ! Add Extra Field Called "TITLE_VIEW" and insert data to it.
    #    view_context['ClassInstance'] = self.more_context['ClassInstance'] # ! And so on.
#
    #    return view_context # ! Return the Context to be rendered later on.

    def logout_then_login(request, *args, **kwargs):
        return super(DeauthUserView, self).logout_then_login(*args, **kwargs)


class RedirectPerspective(RedirectView):
    more_context = {
        "title_view": "Redirect View",
        "user_class": None,
        "ClassInstance": str(__qualname__),
    }
    def get(self, request, *args, **kwargs):
        pass

    def post(self, request, *args, **kwargs):
        pass
