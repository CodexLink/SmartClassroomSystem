from django.views.generic.base import TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
import requests
from requests.exceptions import ConnectionError

# ! A Class That Just Loads the Default "home.html"

class HomeView(TemplateView):
    template_view = 'elem_inst_view.html'

    title_page = None

    def get(self, request):
        return render(request, self.template_view, {"page_title": "Dashboard", "page_type": "Teacher"})

    def sendMCUData(self):
        try:
            return requests.get("http://192.168.100.41/RequestSens", timeout=.1)
        except ConnectionError as Err:
            return None
            #self.response.text = None
            pass

class DashboardView(TemplateView):
    template_view = 'home.html'

    def get(self, request):
        return render(request, self.template_view, {"page_title": "Dashboard", "page_type": "Teacher"})

    def post(self, request, classRoomID):
        pass

    def sendMCUData(self):
        try:
            return requests.get("http://192.168.100.41/RequestSens", timeout=.1)
        except ConnectionError as Err:
            return None
            #self.response.text = None
            pass
    pass

class ClassroomView(TemplateView):
    page_title = None
    path_action = None # ! Optional, but mostly used. The 3rd part of URL is the one that is being used.
    as_modular_view = None # ! Optional and limited only to logs and info.

    def get(self, request, classRoomID):
        pass

    def post(self, request, classRoomID):
        pass

class SelectableClassroomView(TemplateView):
    page_title = None
    path_action = None # ! Optional, but mostly used. The 3rd part of URL is the one that is being used.
    as_modular_view = None # ! Optional and limited only to logs and info.

    def get(self, request, classRoomID):
        pass

    def post(self, request, classRoomID):
        pass

class ScheduleView(TemplateView):
    page_title = None
    path_action = None # ! Optional, but mostly used. The 3rd part of URL is the one that is being used.
    as_modular_view = None # ! Optional and limited only to logs and info.

    def get(self, request, classRoomID):
        pass

    def post(self, request, classRoomID):
        pass

class OverrideView(TemplateView):
    page_title = None
    path_action = None # ! Optional, but mostly used. The 3rd part of URL is the one that is being used.
    as_modular_view = None # ! Optional and limited only to logs and info.

    def get(self, request):
        pass

    def post(self, request):
        pass

class SystemView(TemplateView):
    page_title = None
    path_action = None # ! Optional, but mostly used. The 3rd part of URL is the one that is being used.

    def get(self, request):
        pass

    def post(self, request):
        pass

# ! Authentication Classes
class AuthUserView(LoginView):
    template_view = 'login.html'

    def get(self, request, *args, **kwargs):
        pass


    def post(self, request, *args, **kwargs):
        pass


class DeauthUserView(LoginView):
    template_view = 'logout.html'


class RedirectPerspective(TemplateView):
    template_view = 'dashboard.html'
