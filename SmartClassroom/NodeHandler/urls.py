from django.contrib import admin
from django.urls import include, path
from .views import *

urlpatterns = [
    #path('migrate_node/<int:>/<str:>/<int:>/<str:>', MigrationScheduler.as_view(), name='node_migration_processor'),
    #path('/lockRemoteCall/', NodeMultiAuthenticator.as_view(), name='node_locker_processor'),
    #path('/nodeMigrationer/', MigrationScheduler.as_view(), name='node_migration_processor'),
    # ! This path has been called by lock. When nodemcu lock was on, then electricity and lock are both triggered.
    path('lockRemoteCall/<str:NodeDevUUID>/<str:ClassroomUUID>/<int:user_fngrprnt_id>/LockState=<int:GivenContextLockState>', NodeMultiAuthenticator.as_view(), name='node_locker_processor'),
]
