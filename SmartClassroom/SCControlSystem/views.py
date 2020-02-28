import datetime
from json import loads as DictSerialize

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import (AccessMixin, LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.contrib.auth.views import LoginView, LogoutView, logout_then_login
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.views.generic import FormView, ListView, RedirectView
from django.views.generic.base import TemplateView
from requests import get as FetchLiveData
from django.http import HttpResponseRedirect
from requests.exceptions import RequestException
from .externs.subject_types import *

from .forms import UserAuthForm
from .models import *

# ! Global Variables !
template_view = 'elem_inst_view.html'

class DashboardView(PermissionRequiredMixin, TemplateView):
    login_url = reverse_lazy('auth_user_view')
    template_name = template_view
    redirect_field_name = reverse_lazy('deauth_user_view')

    permission_required = 'SCControlSystem.dashboard_viewable'

    more_context = {
        "title_view": "Dashboard",
        "ClassInstance": str(__qualname__)
    }

    def get_context_data(self, **kwargs): # ! Override Get_Context_Data by adding more data.
        current_user = self.request.user
        view_context = super(DashboardView, self).get_context_data(**kwargs) # * Get the default context to override to.
        view_context['title_view'] = self.more_context['title_view']
        view_context['user_instance_name'] = '%s %s %s' % (current_user.first_name, current_user.middle_name if current_user.middle_name is not None else '', current_user.last_name)
        view_context['user_class'] = current_user.user_role
        view_context['user_branch'] = current_user.dept_residence

        view_context['ClassInstance'] = self.more_context['ClassInstance']
        view_context['refresh_recent_time'] = datetime.datetime.now().time().strftime('%I:%M%p')

        # ! More Objects To Display at.
        if not current_user.user_role == "Professor":
            view_context['cr_unlocked_count'] = Classroom.objects.filter(Classroom_State='Unlocked').count()
            view_context['cr_locked_count'] = Classroom.objects.filter(Classroom_State='Locked').count()

            view_context['dev_offline_count'] = DeviceInfo.objects.filter(Device_Status='Offline').count()
            view_context['dev_online_count'] = DeviceInfo.objects.filter(Device_Status='Locked').count()

            # ! Admin View for Classroom Systems
            view_context['dev_offline_candidates'] = DeviceInfo.objects.filter(Device_Status='Offline').select_related('classroom')
            view_context['dev_online_candidates'] = DeviceInfo.objects.filter(Device_Status='Online').select_related('classroom')

            view_context['classroom_logs'] = ClassroomActionLog.objects.all().order_by('-TimeRecorded')[:5]

        else:
            view_context['schedule_weekday_name'] = datetime.datetime.today().strftime('%A')
            # ! We currently looking at foreign key here.
            view_context['schedule_candidates'] = CourseSchedule.objects.filter(CourseSchedule_Instructor__first_name=current_user.first_name, CourseSchedule_Instructor__middle_name=current_user.middle_name, CourseSchedule_Instructor__last_name=current_user.last_name, CourseSchedule_Lecture_Day=view_context['schedule_weekday_name']).order_by('CourseSchedule_Session_Start')
            view_context['classroom_logs'] = ClassroomActionLog.objects.filter(Course_Reference__CourseSchedule_Instructor__first_name=current_user.first_name, Course_Reference__CourseSchedule_Instructor__middle_name=current_user.middle_name, Course_Reference__CourseSchedule_Instructor__last_name=current_user.last_name).order_by('-TimeRecorded')[:5]

        return view_context # ! Return the Context to be rendered later on.

    # ! Here, we have to determine if user is authenticated at this point.
    # * If it is, then DO NOT redirect to login page.
    # * Else, then DO redirect to login page.
    def handle_no_permission(self):
        self.raise_exception = self.request.user.is_authenticated
        if self.raise_exception:
            messages.error(self.request, "InsufficientPermission")
        else:
            messages.error(self.request, "PermissionAccessDenied")
        return super(DashboardView, self).handle_no_permission()

class ClassroomView(PermissionRequiredMixin, ListView):
    login_url = reverse_lazy('auth_user_view')
    template_name = template_view
    model = Classroom
    queryset = Classroom.objects.all().order_by('Classroom_CompleteString')

    permission_required = ('SCControlSystem.user_high_level_required', 'SCControlSystem.classroom_viewable')

    more_context = {
        "title_view": "Classroom List",
        "ClassInstance": str(__qualname__),
    }

    def get_context_data(self, **kwargs): # ! Override Get_Context_Data by adding more data.
        current_user = self.request.user
        view_context = super(ClassroomView, self).get_context_data(**kwargs) # * Get the default context to override to.
        view_context['title_view'] = self.more_context['title_view']
        view_context['user_instance_name'] = '%s %s %s' % (current_user.first_name, current_user.middle_name if current_user.middle_name is not None else '', current_user.last_name)
        view_context['user_class'] = current_user.user_role
        view_context['ClassInstance'] = self.more_context['ClassInstance']
        return view_context

    def handle_no_permission(self):
        self.raise_exception = self.request.user.is_authenticated
        if self.raise_exception:
            messages.error(self.request, "InsufficientPermission")
        else:
            messages.error(self.request, "PermissionAccessDenied")
        return super(ClassroomView, self).handle_no_permission()

class SelectableClassroomView(PermissionRequiredMixin, ListView):
    login_url = reverse_lazy('auth_user_view')
    template_name = template_view
    ActionState = None
    model = CourseSchedule # ! We use CourseSchedule Model Instead of Classroom. Because Inheritance
    sendOnce = False

    slug_url_kwarg = 'classUniqueID'

    # ! ADD SCHEDULE VIEWABLE
    permission_required = ('SCControlSystem.classroom_viewable',
                          'SCControlSystem.classroom_action_log_viewable',
                          )

    more_context = {
        "title_view": "Classroom Control View",
        "ClassInstance": str(__qualname__),
    }

    def get_context_data(self, **kwargs): # ! Override Get_Context_Data by adding more data.
        current_user = self.request.user
        view_context = super(SelectableClassroomView, self).get_context_data(**kwargs) # * Get the default context to override to.
        view_context['title_view'] = self.more_context['title_view']
        view_context['user_instance_name'] = '%s %s %s' % (current_user.first_name, current_user.middle_name if current_user.middle_name is not None else '', current_user.last_name)
        view_context['user_class'] = current_user.user_role
        view_context['ClassInstance'] = self.more_context['ClassInstance']
        view_context['refresh_recent_time'] = datetime.datetime.now().time().strftime('%I:%M%p')
        view_context['Class_UID_Literal'] = self.kwargs['classUniqueID']

        # We wanna set the status of the device with its live sensor literally.
        try:
            Device_MetaData_Name = CourseSchedule.objects.filter(CourseSchedule_Room__Classroom_Unique_ID=self.kwargs['classUniqueID']).values('CourseSchedule_Room__Classroom_Dev__Device_Name')[0]
            Device_MetaData_IP = CourseSchedule.objects.filter(CourseSchedule_Room__Classroom_Unique_ID=self.kwargs['classUniqueID']).values('CourseSchedule_Room__Classroom_Dev__Device_IP_Address')[0]

            Device_MetaData_UUID = CourseSchedule.objects.filter(CourseSchedule_Room__Classroom_Unique_ID=self.kwargs['classUniqueID']).values('CourseSchedule_Room__Classroom_Dev__Device_Unique_ID')[0]
            passUniqueID = str(Device_MetaData_UUID['CourseSchedule_Room__Classroom_Dev__Device_Unique_ID']).replace('-', '')

            dev_metadata = FetchLiveData('http://%s/RequestData' % (Device_MetaData_IP['CourseSchedule_Room__Classroom_Dev__Device_IP_Address']), auth=(str(Device_MetaData_Name['CourseSchedule_Room__Classroom_Dev__Device_Name']), passUniqueID), timeout=5)

            if dev_metadata.ok:
                finalMetaData = DictSerialize((dev_metadata.content).decode('utf-8').replace("'", "\""))
                view_context['TempOutput'] = finalMetaData['DATA_SENS']['CR_TEMP']
                view_context['HumidOutput'] = finalMetaData['DATA_SENS']['CR_HUMD']
                view_context['HeatInxOutput'] = finalMetaData['DATA_SENS']['CR_HTINX']
                view_context['PIRTTOutput'] = finalMetaData['DATA_SENS']['PIR_MOTION']['PIR_OTPT_TIME_TRIGGER'] # Time Trigger Output

                view_context['ClassAccessState'] = 'Enabled' if int(finalMetaData['DATA_STATE']['ACCESS_STATE']) else 'Disabled'
                view_context['LockState'] = 'Unlocked' if int(finalMetaData['DATA_STATE']['DOOR_STATE']) else 'Locked'
                view_context['ElectricityState'] = 'On' if int(finalMetaData['DATA_STATE']['ELECTRIC_STATE']) else 'Off'
                view_context['AuthCRState'] = 'Authenticated' if int(finalMetaData['DATA_AUTH']['AUTH_STATE']) else 'Not Authenticated'
                view_context['UserScheduledID'] = finalMetaData['DATA_AUTH']['AUTH_ID']
                view_context['DeviceState'] = "Online"

        except RequestException:
            messages.info(self.request, 'DeviceRequestFailed')
            pass

        if not current_user.user_role == "Professor":
            view_context['ClassLogs'] = ClassroomActionLog.objects.filter(Course_Reference__CourseSchedule_Room__Classroom_Unique_ID=self.kwargs['classUniqueID']).order_by('-TimeRecorded')
            view_context['SubjectsInvolved'] = CourseSchedule.objects.filter(CourseSchedule_Room__Classroom_Unique_ID=self.kwargs['classUniqueID']).order_by('-CourseSchedule_Session_Start').values('CourseSchedule_Instructor__first_name', 'CourseSchedule_Instructor__middle_name', 'CourseSchedule_Instructor__last_name', 'CourseSchedule_CourseReference__Course_Name', 'CourseSchedule_CourseReference__Course_Code' , 'CourseSchedule_Section__Section_CompleteStringGroup').distinct()
        else:
            # ! Add More Context. Do not really output all, just on classlogs
            view_context['ClassLogs'] = ClassroomActionLog.objects.filter(Course_Reference__CourseSchedule_Instructor__first_name=current_user.first_name, Course_Reference__CourseSchedule_Instructor__middle_name=current_user.middle_name, Course_Reference__CourseSchedule_Instructor__last_name=current_user.last_name, Course_Reference__CourseSchedule_Room__Classroom_Unique_ID=self.kwargs['classUniqueID']).order_by('-TimeRecorded')

        if self.ActionState:
            messages.info(self.request, 'DeviceRequestSuccess')
            classroomPointer = Classroom.objects.filter(Classroom_Unique_ID=self.kwargs['classUniqueID']).values('Classroom_CompleteString').distinct()

            if self.ActionState == "CRAccess":
                dataFetchState = FetchLiveData('http://%s/RequestInstance?cr_access=%s' % (Device_MetaData_IP['CourseSchedule_Room__Classroom_Dev__Device_IP_Address'], StateResponseContext), auth=(str(Device_MetaData_Name['CourseSchedule_Room__Classroom_Dev__Device_Name']), passUniqueID), timeout=5)
                
                if not current_user.user_role in ("Professor", "ITSO Supervisor"):
                    StateResponseContext = False if view_context['ClassAccessState'] == 'Enabled' else True
                    if dataFetchState.status_code.ok:
                        adminReference = CourseSchedule.objects.get(CourseSchedule_CourseReference__Course_Name="Admin Control Management", CourseSchedule_Room=classroomPointer[0]['Classroom_CompleteString'])
                        objectInstance = ClassroomActionLog.objects.create(UserActionTaken=ClassroomActionTypes[13][0] if StateResponseContext else ClassroomActionTypes[12][0], ActionLevel=LevelAlert[2][0], Course_Reference=adminReference)
                        objectInstance.save()

                        view_context['ResponseMessage'] = 'RequestChangeSet'
                        messages.info(self.request, 'CRAccessRequestChange')
                        return view_context
                    else:
                        view_context['DeviceState'] = None
                        return view_context

                else:
                    if dataFetchState.status_code.ok:
                        view_context['ResponseMessage'] = 'RequestChangeSet'
                        messages.info(self.request, 'InvalidCommand')
                        return view_context
                    else:
                        view_context['DeviceState'] = None
                        messages.info(self.request, 'InvalidCommand')
                        return view_context



            elif self.ActionState == "LockState":
                StateResponseContext = False if view_context['LockState'] == 'Locked' else True
                dataFetchState = FetchLiveData('http://%s/RequestInstance?lock_state=%s' % (Device_MetaData_IP['CourseSchedule_Room__Classroom_Dev__Device_IP_Address'], StateResponseContext), auth=(str(Device_MetaData_Name['CourseSchedule_Room__Classroom_Dev__Device_Name']), passUniqueID), timeout=5)

                if dataFetchState.status_code.ok:
                    if not current_user.user_role in ("Professor", "ITSO Supervisor"):
                        adminReference = CourseSchedule.objects.get(CourseSchedule_CourseReference__Course_Name="Admin Control Management", CourseSchedule_Room=classroomPointer[0]['Classroom_CompleteString'])

                    else:
                        adminReference = CourseSchedule.objects.get(CourseSchedule_Instructor__first_name=current_user.first_name, CourseSchedule_Instructor__middle_name=current_user.middle_name, CourseSchedule_Instructor__last_name=current_user.last_name, CourseSchedule_Room=classroomPointer[0]['Classroom_CompleteString'])

                    objectInstance = ClassroomActionLog.objects.create(UserActionTaken=ClassroomActionTypes[1][0] if StateResponseContext else ClassroomActionTypes[0][0], ActionLevel=LevelAlert[0][0], Course_Reference=adminReference)
                    objectInstance.save()
                    view_context['ResponseMessage'] = 'RequestChangeSet'
                    messages.info(self.request, 'LockStateRequestChange')
                    return view_context

                else:
                    view_context['ResponseMessage'] = None
                    return view_context

            elif self.ActionState == "ElectricState":
                StateResponseContext = False if view_context['ElectricityState'] == 'On' else True
                dataFetchState = FetchLiveData('http://%s/RequestInstance?electric_state=%s' % (Device_MetaData_IP['CourseSchedule_Room__Classroom_Dev__Device_IP_Address'], StateResponseContext), auth=(str(Device_MetaData_Name['CourseSchedule_Room__Classroom_Dev__Device_Name']), passUniqueID), timeout=5)

                if dataFetchState.status_code.ok:
                    if not current_user.user_role in ("Professor", "ITSO Supervisor"):
                        adminReference = CourseSchedule.objects.get(CourseSchedule_CourseReference__Course_Name="Admin Control Management", CourseSchedule_Room=classroomPointer[0]['Classroom_CompleteString'])

                    else:
                        adminReference = CourseSchedule.objects.get(CourseSchedule_Instructor__first_name=current_user.first_name, CourseSchedule_Instructor__middle_name=current_user.middle_name, CourseSchedule_Instructor__last_name=current_user.last_name, CourseSchedule_Room=classroomPointer[0]['Classroom_CompleteString'])

                    objectInstance = ClassroomActionLog.objects.create(UserActionTaken=ClassroomActionTypes[3][0] if StateResponseContext else ClassroomActionTypes[4][0], ActionLevel=LevelAlert[1][0], Course_Reference=adminReference)
                    objectInstance.save()

                    view_context['ResponseMessage'] = 'RequestChangeSet'
                    messages.info(self.request, 'ElectricStateRequestChange')
                    return view_context

                else:
                    view_context['ResponseMessage'] = None
                    return view_context

            elif self.ActionState == "DevRestart":
                dataFetchState = FetchLiveData('http://%s/RequestInstance?dev_rstrt=initiate' % (Device_MetaData_IP['CourseSchedule_Room__Classroom_Dev__Device_IP_Address']), auth=(str(Device_MetaData_Name['CourseSchedule_Room__Classroom_Dev__Device_Name']), passUniqueID), timeout=5)
                
                if dataFetchState.status_code.ok:
                    if not current_user.user_role in ("Professor", "ITSO Supervisor"):

                        adminReference = CourseSchedule.objects.get(CourseSchedule_CourseReference__Course_Name="Admin Control Management", CourseSchedule_Room=classroomPointer[0]['Classroom_CompleteString'])
                        objectInstance = ClassroomActionLog.objects.create(UserActionTaken=ClassroomActionTypes[7][0], ActionLevel=LevelAlert[2][0], Course_Reference=adminReference)
                        objectInstance.save()

                        messages.info(self.request, 'DevRestartRequestChange')
                        view_context['ResponseMessage'] = 'RequestChangeSet'
                        return view_context

                    else:
                        view_context['ResponseMessage'] = 'RequestChangeSet'
                        messages.info(self.request, 'InvalidCommand')
                        return view_context
                else:
                    view_context['ResponseMessage'] = None
                    messages.info(self.request, 'InvalidCommand')
                    return view_context
                    
        else:
            if self.sendOnce != True:
                messages.info(self.request, 'DeviceRequestSuccess')

            view_context['ResponseMessage'] = None
            return view_context # ! Return the Context to be rendered later on.

    def get_queryset(self):
        return CourseSchedule.objects.filter(CourseSchedule_Room__Classroom_Unique_ID=self.kwargs['classUniqueID'])

    def handle_no_permission(self):
        self.raise_exception = self.request.user.is_authenticated
        if self.raise_exception:
            messages.error(self.request, "InsufficientPermission")
        else:
            messages.error(self.request, "PermissionAccessDenied")
        return super(SelectableClassroomView, self).handle_no_permission()

class ScheduleListView(PermissionRequiredMixin, ListView):
    login_url = reverse_lazy('auth_user_view')
    template_name = template_view
    model = CourseSchedule

    permission_required = 'SCControlSystem.course_schedule_viewable'

    more_context = {
        "title_view": "Your Schedules",
        "ClassInstance": str(__qualname__),
    }

    def get_queryset(self):
        return CourseSchedule.objects.filter(CourseSchedule_Instructor__first_name=self.request.user.first_name, CourseSchedule_Instructor__middle_name=self.request.user.middle_name, CourseSchedule_Instructor__last_name=self.request.user.last_name).order_by('CourseSchedule_Session_Start')

    def get_context_data(self, **kwargs): # ! Override Get_Context_Data by adding more data.
        current_user = self.request.user
        view_context = super(ScheduleListView, self).get_context_data(**kwargs) # * Get the default context to override to.
        view_context['title_view'] = self.more_context['title_view']
        view_context['user_instance_name'] = '%s %s %s' % (current_user.first_name, current_user.middle_name if current_user.middle_name is not None else '', current_user.last_name)
        view_context['user_class'] = current_user.user_role
        view_context['ClassInstance'] = self.more_context['ClassInstance']
        view_context['schedule_weekday_name'] = datetime.datetime.today().strftime('%A')
        return view_context # ! Return the Context to be rendered later on.

    def handle_no_permission(self):
        self.raise_exception = self.request.user.is_authenticated
        if self.raise_exception:
            messages.error(self.request, "InsufficientPermission")
        else:
            messages.error(self.request, "PermissionAccessDenied")
        return super(ScheduleListView, self).handle_no_permission()
# ! Authentication Classes

# ! AuthUserView Requires LoginView To Provide Minimal Configuration
class AuthUserView(LoginView):
    template_name = template_view # * Use Global Variable Later
    form_class = UserAuthForm # ! Declare Our Form To Be Used.
    success_url = reverse_lazy('dashboard_user_view') # ! This renders URL later when login is success.
    redirect_authenticated_user = True

    # ! We provide more context to the form when it request by GET.
    more_context = {
        "title_view": "User Login",
        "ClassInstance": str(__qualname__),
    }


    # ! Override Get_Context_Data by adding more data.
    def get_context_data(self, **kwargs):
        view_context = super(AuthUserView, self).get_context_data(**kwargs) # * Get the default context to override to.
        view_context['title_view'] = self.more_context['title_view'] # ! Add Extra Field Called "TITLE_VIEW" and insert data to it.
        view_context['ClassInstance'] = self.more_context['ClassInstance'] # ! And so on.

        return view_context # ! Return the Context to be rendered later on.

    def get_success_url(self):
        return self.success_url # * We get redirect to the value of this attribute.

# ! DeauthUserView Requires LogoutView To Provide Minimal Configuration
# * This view is literally the same as AuthUserView except it is very minimal because it only displays few things.
# * And it automatically logs out user that is currently logged in the session.
# ! This does not go back if user is not authenticated anymore, so this class is casted with LoginRequiredMixin.
class DeauthUserView(LoginRequiredMixin, LogoutView):
    template_name = template_view # ! We use the same as always except we render it with different view.

    # *Bit of redundant here, login_url used by LogoutView and next_page was used by LoginRequiredMixins
    login_url = reverse_lazy('auth_user_view')
    next_page = login_url

    # ! We override this function upon page load.
    def dispatch(self, request):
        # ! Message outputs the same when user tries to log out.
        # * To filter things out, we have to check if user really is authenticated before outputting message that is added below.
        if request.user.is_authenticated:
            messages.success(self.request, "UserLoggedOut")
        return super(DeauthUserView, self).dispatch(request)

    # ! Handle This To Render from Login
    def handle_no_permission(self):
        # ! We output message if user attempts to access this page.
        messages.error(self.request, "UserAlreadyLoggedOut")
        return super(DeauthUserView ,self).handle_no_permission()

# ! Contains multiple logs that can is subjected for review.
class StaffActionsListView(PermissionRequiredMixin, ListView):
    login_url = reverse_lazy('auth_user_view')
    template_name = template_view
    model = ClassroomActionLog

    permission_required = 'SCControlSystem.classroom_action_log_viewable'

    more_context = {
        "title_view": "Action Logs",
        "ClassInstance": str(__qualname__),
    }

    def get_queryset(self):
        if not self.request.user.user_role == "Professor":
            return ClassroomActionLog.objects.all().order_by('-TimeRecorded')
        else:
            return ClassroomActionLog.objects.filter(Course_Reference__CourseSchedule_Instructor__first_name=self.request.user.first_name, Course_Reference__CourseSchedule_Instructor__middle_name=self.request.user.middle_name, Course_Reference__CourseSchedule_Instructor__last_name=self.request.user.last_name).order_by('-TimeRecorded')

    def get_context_data(self, **kwargs): # ! Override Get_Context_Data by adding more data.
        current_user = self.request.user
        view_context = super(StaffActionsListView, self).get_context_data(**kwargs) # * Get the default context to override to.
        view_context['title_view'] = self.more_context['title_view']
        view_context['user_instance_name'] = '%s %s %s' % (current_user.first_name, current_user.middle_name if current_user.middle_name is not None else '', current_user.last_name)
        view_context['user_class'] = current_user.user_role
        view_context['ClassInstance'] = self.more_context['ClassInstance']
        return view_context # ! Return the Context to be rendered later on.

    def handle_no_permission(self):
        self.raise_exception = self.request.user.is_authenticated
        if self.raise_exception:
            messages.error(self.request, "InsufficientPermission")
        else:
            messages.error(self.request, "PermissionAccessDenied")
        return super(StaffActionsListView, self).handle_no_permission()
