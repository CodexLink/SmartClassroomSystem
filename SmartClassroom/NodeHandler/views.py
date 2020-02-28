from django.shortcuts import render
from request import get as FetchData
from requests.exceptions import RequestException
from SCControlSystem.models import *
from django.views.generic import DetailView


class AuthenticateNode(DetailView):
    template_name = None

    def get_queryset(self):
        return

class MigrationScheduler(DetailView):
    template_name = None
    
    def get_queryset(self):
        return
"""
class (DetailView):
    template_name = None

    def get_queryset(self):
        return

class (DetailView):
    template_name = None

    def get_queryset(self):
        return

class (DetailView):
    template_name = None
    def get_queryset(self):
        return
"""