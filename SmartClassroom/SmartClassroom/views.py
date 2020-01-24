from django.views.generic.base import TemplateView
from django.shortcuts import render
import requests
from requests.exceptions import ConnectionError

# ! A Class That Just Loads the Default "home.html"


class HomeFrameView(TemplateView):

    title_page = None

    def get(self, request):
        return render(request, 'home.html', {"page_title": self.sendMCUData(), "page_type": "Teacher"})

    def sendMCUData(self):
        try:
            return requests.get("http://192.168.100.41/RequestSens", timeout=.1)
        except ConnectionError as Err:
            return None
            #self.response.text = None
            pass
