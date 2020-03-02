from django.shortcuts import render
from requests import get as FetchData
from requests.exceptions import RequestException
from SCControlSystem.models import *
from SCControlSystem.externs.subject_types import *

from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import HttpResponse, HttpResponseNotAllowed
from uuid import UUID as ReturnValidableUUID

@method_decorator(csrf_exempt, name='dispatch')
class NodeMultiAuthenticator(TemplateView):
    template_name = 'noContextReponseOnly.html'

    def dispatch(self, *args, **kwargs):
        return super(NodeMultiAuthenticator, self).dispatch(*args, **kwargs)

    def post(self, *args, **kwargs):
        print("Backend | Lock Authentication Callback Accessed!")
        print("Process | Cleansing Given Context...\n")
        print("Given Context | Device UUID |> %s" % self.kwargs['NodeDevUUID'])
        print("Given Context | Classroom UUID |> %s\n" % self.kwargs['ClassroomUUID'])

        validable_NodeUUID = ReturnValidableUUID(self.kwargs['NodeDevUUID'])
        validable_CRUUID = ReturnValidableUUID(self.kwargs['ClassroomUUID'])
        context_RoomLockState = self.kwargs['GivenContextLockState']

        print("Cleansed Context | Device UUID |> %s" % validable_NodeUUID)
        print("Cleansed Context | Classroom UUID |> %s\n" % validable_CRUUID)

            # Then get user.
        print("Query | Obtaining User...")
        userInstance = UserDataCredentials.objects.get(fp_id=self.kwargs['GivenContextLockState'])

        if userInstance:
            print("Query | User Found with ID: %s!" % (self.kwargs['GivenContextLockState']))
        else:
            print("Query | User Not Found with ID: %s!" % (self.kwargs['GivenContextLockState']))
            print("Termination | This Action Request will be Dropped!!!")
            return HttpResponseNotAllowed('NODEMCU POST REQ |> LOCK AUTHENTICATION | FAILED | USER NOT FOUND')

        print("Query | Checking for Classroom and Device from UUID |> %s and %s" % (validable_CRUUID, validable_NodeUUID))
        classInstance = Classroom.objects.get(Classroom_Unique_ID=validable_CRUUID, Classroom_Dev__Device_Unique_ID=validable_NodeUUID)

        if classInstance:
            print("Query | Found %s and %s " % (validable_NodeUUID, validable_CRUUID))
            print("Execution | Altering Classroom State with Parameter of LockState (Equals to: %s)" % ("Locked" if context_RoomLockState else "UnLocked",))
            classInstance.Classroom_State = "Unlocked" if context_RoomLockState else "Locked"
            classInstance.save(update_fields=['Classroom_State'])

            print("Execution | Classroom State Alteration Done...\n")
            print("Execution | Recording This Action to User ID: %s" % (self.kwargs['GivenContextLockState'],))

            classroomPointerInstance = Classroom.objects.filter(Classroom_Unique_ID=validable_CRUUID, Classroom_Dev__Device_Unique_ID=validable_NodeUUID).values('Classroom_CompleteString').distinct()
            professorReference = CourseSchedule.objects.filter(CourseSchedule_Instructor__first_name=userInstance.first_name, CourseSchedule_Instructor__middle_name=userInstance.middle_name, CourseSchedule_Instructor__last_name=userInstance.last_name, CourseSchedule_Room=classroomPointerInstance[0]['Classroom_CompleteString'])[0]
            recordInstance = ClassroomActionLog.objects.create(UserActionTaken=ClassroomActionTypes[2][0] if context_RoomLockState else ClassroomActionTypes[3][0], ActionLevel=LevelAlert[0][0], Course_Reference=professorReference)

            print("Execution | Action Recorded to User ID: %s" % (self.kwargs['GivenContextLockState'],))
            print("Process | All Done!!!")
            return HttpResponse('NODEMCU POST REQ |> LOCK AUTHENTICATION | OKAY')

        else:
            print("Query | %s or %s does not exists!!!" % (validable_NodeUUID, validable_CRUUID))
            print("Termination | This Action Request will be Dropped!!!")
            return HttpResponseNotAllowed('NODEMCU POST REQ |> LOCK AUTHENTICATION | FAILED | CLASSROOM NOT FOUND')


class MigrationScheduler(TemplateView):
    template_name = None

    def get_queryset(self):
        return
