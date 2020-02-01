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
    title_page = "Welcome"
    InstanceClassName = str(__qualname__)  # ! Qualified Class Name

    def get(self, request):
        return render(request, template_view, {"InstanceCaller": self.InstanceClassName, "page_title": "Home"})

    def sendMCUData(self):
        try:
            return requests.get("http://192.168.100.41/RequestSens", timeout=.1)
        except ConnectionError as Err:
            return None
            #self.response.text = None
            pass


class DashboardView(TemplateView):
    title_page = 'Dashboard'
    InstanceClassName = str(__qualname__)  # ! Qualified Class Name

    # ! User Instance Type is already passable so creating variable is useless.

    def get(self, request):
        return render(request, template_view, {"InstanceCaller": self.InstanceClassName, "page_title": self.title_page, "page_type": "Admin"})

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
    page_title = "List of Classrooms"
    # ! Optional, but mostly used. The 3rd part of URL is the one that is being used.
    path_action = None
    as_modular_view = None  # ! Optional and limited only to logs and info.
    InstanceClassName = str(__qualname__)  # ! Qualified Class Name

    def get(self, request):
        return render(request, template_view, {"InstanceCaller": self.InstanceClassName, "page_title": self.page_title, "page_type": "Admin"})

    def post(self, request):
        pass


class SelectableClassroomView(TemplateView):

    page_title = "Classroom"
    InstanceClassName = str(__qualname__)
    # *page_title_secondary is the classroom name.

    # ! Optional, but mostly used. The 3rd part of URL is the one that is being used.
    path_action = None
    as_modular_view = None  # ! Optional and limited only to logs and info.

    def get(self, request, classRoomID=None):
        return render(request, template_view, {"InstanceCaller": self.InstanceClassName, "page_title": self.page_title, "page_type": "Admin"})

    def post(self, request, classRoomID=None):
        pass


class ScheduleListView(ListView):
    page_title = "Your Class Schedules"
    # ! Optional, but mostly used. The 3rd part of URL is the one that is being used.
    path_action = None
    as_modular_view = None  # ! Optional and limited only to logs and info.
    InstanceClassName = str(__qualname__)

    def get(self, request):
        return render(request, template_view, {"InstanceCaller": self.InstanceClassName, "page_title": self.page_title, "page_type": "Admin"})

    def post(self, request):
        pass


class OverrideControlView(TemplateView):
    page_title = "Override System"
    # ! Optional, but mostly used. The 3rd part of URL is the one that is being used.
    path_action = None
    as_modular_view = None  # ! Optional and limited only to logs and info.
    InstanceClassName = str(__qualname__)

    def get(self, request):
        return render(request, template_view, {"InstanceCaller": self.InstanceClassName, "page_title": self.page_title, "page_type": "Admin"})

    def post(self, request):
        pass


class SystemSettingsView(TemplateView):
    page_title = "System Settings"
    # ! Optional, but mostly used. The 3rd part of URL is the one that is being used.
    path_action = None
    InstanceClassName = str(__qualname__)

    def get(self, request):
        return render(request, template_view, {"InstanceCaller": self.InstanceClassName, "page_title": self.page_title, "page_type": "Admin"})

    def post(self, request):
        pass

# ! Authentication Classes


class AuthUserView(LoginView):
    InstanceClassName = str(__qualname__)
    page_title = "Login"

    def get(self, request, *args, **kwargs):
        return render(request, template_view, {"InstanceCaller": self.InstanceClassName, "page_title": self.page_title})


    def post(self, request, *args, **kwargs):
        pass


class DeauthUserView(LoginView):
    template_view = 'logout.html'

    def get(self, request, *args, **kwargs):
        pass

    def post(self, request, *args, **kwargs):
        pass


class RedirectPerspective(RedirectView):
    template_view = 'dashboard.html'

    def get(self, request, *args, **kwargs):
        pass

    def post(self, request, *args, **kwargs):
        pass
