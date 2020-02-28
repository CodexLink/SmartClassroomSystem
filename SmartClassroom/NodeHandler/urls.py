from django.contrib import admin
from django.urls import include, path
from .views import *

urlpatterns = [
    #path('authenticate_node/<>/<>', AuthenticateNode.as_view(), name='auth_node_class'),

    # This view is correlated at changing EEPRO of a targeted node.
    #path('migrate_node/<int:>/<str:>/<int:>/<str:>', MigrationScheduler.as_view(), name='auth_user_view'),
    #path(' /', .as_view(), name='deauth_user_view'),

]
