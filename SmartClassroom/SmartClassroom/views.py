from django.views.generic.base import TemplateView
from django.shortcuts import render


# ! A Class That Just Loads the Default "home.html"
class HomeFrameView(TemplateView):

    title_page = None

    def get(self, request):
        return render(request, 'home.html', {"page_title": self.title_page, "page_type": "Home"})
