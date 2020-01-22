from django.views.generic.base import TemplateView
from django.shortcuts import render
import requests

# ! A Class That Just Loads the Default "home.html"
class HomeFrameView(TemplateView):

    title_page = None
    response = requests.get("http://192.168.100.41/RequestSens")

    def get(self, request):
        return render(request, 'home.html', {"page_title": self.response.text, "page_type": "Admin"})