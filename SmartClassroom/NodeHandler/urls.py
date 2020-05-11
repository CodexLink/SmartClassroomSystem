from django.urls import path
from .views import *

urlpatterns = [
    # ! This path has been called by lock. When NodeMCU lock state is set to on, then electricity and lock are both triggered.
    path(
        "lockRemoteCall/<str:NodeDevUUID>/<str:ClassroomUUID>/<int:user_fngrprnt_id>/LockState=<int:GivenContextLockState>",
        NodeMultiAuthenticator.as_view(),
        name="node_locker_processor",
    ),
]
