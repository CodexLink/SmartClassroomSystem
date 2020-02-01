from django.views.generic.base import TemplateView
from django.views.generic import ListView, RedirectView
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
import requests
from requests.exceptions import ConnectionError

# ! Global Variables !
template_view = 'elem_inst_view.html'

# ! A Class That Just Loads the Default "home.html"
class HomeView(TemplateView):

    view_context = {
        "title_view": "Welcome",
        "page_view": "Home",
        "ClassInstance": str(__qualname__),
    }

    def get(self, request):
        return render(request, template_view, self.view_context)

    def sendMCUData(self):
        try:
            return requests.get("http://192.168.100.41/RequestSens", timeout=.1)
        except ConnectionError as Err:
            return None
            #self.response.text = None
            pass


class DashboardView(TemplateView):
    view_context = {
        "title_view": "Dashboard",
        "page_view": "Dashboard",
        "user_class": "Admin",
        "ClassInstance": str(__qualname__),
    }

    # ! User Instance Type is already passable so creating variable is useless.

    def get(self, request):
        return render(request, template_view, self.view_context)

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

    view_context = {
        "title_view": "Classroom List",
        "page_view": "List of Classrooms",
        "user_class": "Admin",
        "ClassInstance": str(__qualname__),
    }


    def get(self, request):
        return render(request, template_view, self.view_context)

    def post(self, request):
        pass


class SelectableClassroomView(TemplateView):
    # ! Optional, but mostly used. The 3rd part of URL is the one that is being used.
    path_action = None
    as_modular_view = None  # ! Optional and limited only to logs and info.


    view_context = {
        "title_view": "Classroom",
        "page_view": "Classroom",
        "user_class": "Admin",
        "ClassInstance": str(__qualname__),
    }


    def get(self, request, classRoomID=None):
        return render(request, template_view, self.view_context)

    def post(self, request, classRoomID=None):
        pass


class ScheduleListView(ListView):
    path_action = None
    as_modular_view = None  # ! Optional and limited only to logs and info.

    view_context = {
        "title_view": "Classroom",
        "page_view": "Your Class Schedules",
        "user_class": "Admin",
        "ClassInstance": str(__qualname__),
    }

    def get(self, request):
        return render(request, template_view, self.view_context)

    def post(self, request):
        pass


class OverrideControlView(TemplateView):
    path_action = None
    as_modular_view = None  # ! Optional and limited only to logs and info.

    view_context = {
        "title_view": "Override",
        "page_view": "Override System",
        "user_class": "Admin",
        "ClassInstance": str(__qualname__),
    }

    def get(self, request):
        return render(request, template_view, self.view_context)

    def post(self, request):
        pass


class SystemSettingsView(TemplateView):
    path_action = None

    view_context = {
        "title_view": "System Overview",
        "page_view": "System Settings",
        "user_class": "Admin",
        "ClassInstance": str(__qualname__),
    }

    def get(self, request):
        return render(request, template_view, self.view_context)

    def post(self, request):
        pass

# ! Authentication Classes

class AuthUserView(LoginView):
    view_context = {
        "title_view": "Login View",
        "page_view": "Login",
        "user_class": None,
        "ClassInstance": str(__qualname__),
    }

    def get(self, request, *args, **kwargs):
        return render(request, template_view, self.view_context)


    def post(self, request, *args, **kwargs):
        pass


class DeauthUserView(LoginView):

    view_context = {
        "title_view": "Logout View",
        "page_view": "Logout",
        "user_class": None,
        "ClassInstance": str(__qualname__),
    }
    def get(self, request, *args, **kwargs):
        pass

    def post(self, request, *args, **kwargs):
        pass


class RedirectPerspective(RedirectView):
    view_context = {
        "title_view": "Redirect View",
        "page_view": "Redirect",
        "user_class": None,
        "ClassInstance": str(__qualname__),
    }
    def get(self, request, *args, **kwargs):
        pass

    def post(self, request, *args, **kwargs):
        pass
