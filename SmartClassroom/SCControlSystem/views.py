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
        "title_page": "Welcome",
        "page_title": "Home",
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
        "title_page": "Dashboard",
        "page_title": "Dashboard",
        "page_type": "Admin",
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
        "title_page": "Classroom List",
        "page_title": "List of Classrooms",
        "page_type": "Admin",
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
        "title_page": "Classroom",
        "page_title": "Classroom",
        "page_type": "Admin",
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
        "title_page": "Classroom",
        "page_title": "Your Class Schedules",
        "page_type": "Admin",
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
        "title_page": "Override",
        "page_title": "Override System",
        "page_type": "Admin",
        "ClassInstance": str(__qualname__),
    }

    def get(self, request):
        return render(request, template_view, self.view_context)

    def post(self, request):
        pass


class SystemSettingsView(TemplateView):
    path_action = None

    view_context = {
        "title_page": "System Overview",
        "page_title": "System Settings",
        "page_type": "Admin",
        "ClassInstance": str(__qualname__),
    }

    def get(self, request):
        return render(request, template_view, self.view_context)

    def post(self, request):
        pass

# ! Authentication Classes

class AuthUserView(LoginView):
    view_context = {
        "title_page": "Login View",
        "page_title": "Login",
        "page_type": None,
        "ClassInstance": str(__qualname__),
    }

    def get(self, request, *args, **kwargs):
        return render(request, template_view, self.view_context)


    def post(self, request, *args, **kwargs):
        pass


class DeauthUserView(LoginView):

    view_context = {
        "title_page": "Logout View",
        "page_title": "Logout",
        "page_type": None,
        "ClassInstance": str(__qualname__),
    }
    def get(self, request, *args, **kwargs):
        pass

    def post(self, request, *args, **kwargs):
        pass


class RedirectPerspective(RedirectView):
    view_context = {
        "title_page": "Redirect View",
        "page_title": "Redirect",
        "page_type": None,
        "ClassInstance": str(__qualname__),
    }
    def get(self, request, *args, **kwargs):
        pass

    def post(self, request, *args, **kwargs):
        pass
