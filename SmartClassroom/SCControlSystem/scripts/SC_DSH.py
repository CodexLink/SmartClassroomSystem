"""
    ! Smart Classroom IoT Data Stream Handler | SC_DSH.py
    02/29/2020 | Janrey "CodexLink" Licas | http://github.com/CodexLink

    ! In Collaboration with
        - Ronald Langaoan Jr. |> Hardware Designer and Manager
        - Janos Angelo Jantoc |> Hardware Designer and Assistant Programmer
        - Joshua Santos |> Hardware Manager and Builder
        - Johnell Casey Murillo Panotes |> Hardware Assistant

    @required_files: SCMySQLDB.py
    @fork (base work): RGB Name Definition Finder | Python Interfacer Made for Embedded Systems | Prelim Case Study | https://github.com/CodexLink/RGBPotentIdentifier

    @descrip: A Python Program that handles NodeMCU Data in correlation to updating SC DB.
            : It also serves or in another word, monitors them to sync with the data in Django Server.
            : And updates them based from the schedule that is available according to Django Server Time.

    Copyright (C) 2020  Janrey "CodexLink" Licas

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import datetime
import json
from os import system
from subprocess import call as CommandLine
from sys import exit as Terminate
from sys import platform as ReturnedOSName
from time import sleep as delay
from uuid import UUID as StrToValidUUID

from requests import get as DataGETReq
from requests import post as DevDataUpdate
from requests.exceptions import RequestException

from ..models import *


# * We initialize this class with parameters. You can provide your own container by declaring at this scope.
# ! Means you can change NodeDevCandidate Declaration Here.
# * This is a reason why it was declared in the first place. Not directly.
def run():
    SessionInstance = SC_IoTDriver()

    if SessionInstance.checkNodeConn(): # Test All Connections To The IoT Devices.
        try:
            while 1:
                SessionInstance.getNewData()
                SessionInstance.dayCheckScheduleUpdate()
                # Add Scheduler Checker Now.
                print('\nTimeout | Resting for 1 Second Before Device Data Requery!')
                delay(1) # ! 5 Seconds
                SessionInstance.checkNodeConn(CheckBeforeReQueue=True) # Test All Connections To The IoT Devices.
        except:
            pass
    else:
        Terminate()
    # ! At this point, we keep looping from the device endless. That triggers IF and only all scanning to the database were done.


## Main Driver Class
class SC_IoTDriver(object):
    # On Starting Point we have to supply the given arguments to __init__() function.
    # ! Because we have to initialize the class from the object itself.
    def __init__(self, TimeoutCondition=0.3):
        if ReturnedOSName == "win32":
            system("CLS")
            system("title Smart Classroom Data Stream Handler")
        elif ReturnedOSName == "linux":
            system("clear")
        else:
            print("Platform Undetermined!")
            exit(-1)

        print('Smart Classroom IoT Data Stream Handler | SC_DSH.py')
        print('02/29/2020 | By Janrey "CodexLink" Licas | http://github.com/CodexLink\n')
        print('In Collaboration with')
        print('    - Ronald Langaoan Jr. |> Hardware Designer and Manager')
        print('    - Janos Angelo Jantoc |> Hardware Designer and Assistant Programmer')
        print('    - Joshua Santos |> Hardware Manager and Builder')
        print('    - Johnell Casey Murillo Panotes |> Hardware Assistant\n')
        self.TimeoutDevCheck = TimeoutCondition
        self.SubjectOnScope = False
        self.RunTriggerRequestOnce = False
        return

    # ! First Step | Initialization | We check a list of NodeMCUs to be scanned.
    def checkNodeConn(self, CheckBeforeReQueue=False):
        # ! Add Indicators. User actions will be dependent upon this.
        errCount = 0
        passCount = 0
        devList = DeviceInfo.objects.all()

        print("Device List | Checking...")
        if not len(devList):
            print('Count Result | There are no NodeMCUs declared from the container! Please check them and correct them if possible!!!')
            Terminate()
        else:
            print("Count Result | The dictionary contains %s devices to be monitored! \n" % (len(devList)))

    # * IF a device is not included to the list but WAS included to the DJango Database then we set their states as Unknown.
        if CheckBeforeReQueue:
            print('Required Reiteration | Device Requeueing...')

        for deviceCandidateItem in devList:
            try:
                print('Device %s — %s | Checking... |  ' % (deviceCandidateItem.Device_Name, deviceCandidateItem.Device_IP_Address), end='')
                DevResp = DataGETReq('http://%s/RequestData' % (deviceCandidateItem.Device_IP_Address,), timeout=self.TimeoutDevCheck, auth=(deviceCandidateItem.Device_Name, str(deviceCandidateItem.Device_Unique_ID).replace("-", "")))
                if DevResp.ok:
                    print('Response Success.')
                    deviceCandidateItem.Device_Status = 'Online'
                    deviceCandidateItem.save(update_fields=['Device_Status'])
                    passCount += 1
                else:
                    print('Response Failed / No Content.')
                    errCount += 1

            except RequestException:
                deviceCandidateItem.Device_Status = 'Offline'
                deviceCandidateItem.save(update_fields=['Device_Status'])
                print('Response Failed.')
                errCount += 1
                pass

        print('\nDevice Checking Finished... (Success: %s, Failed: %s)\n' % (passCount, errCount))

        if passCount and errCount:
            print("There's are some devices that didn't passed from the connection test!")
            print("NOTE |> They are still included from querying over but will be ignored or passed if they are still not responding from REQUESTs.\n")
            return True

        elif not passCount and errCount:
            print("All devices were not able to pass from the connection test. Please check the device candidate information!\n")
            return True

        print("Device Monitoring Done.")
        return True

    # ! Step 2 | Connect To Them Individual and Check For Datas
    def getNewData(self):
        devMetaData = DeviceInfo.objects.filter(Device_Status='Online')
        for devTargetItem in devMetaData:
            try:
                print('Job | Device Currently on Process Query is %s — %s'% (devTargetItem.Device_Name, devTargetItem.Device_IP_Address,))
                DevResp = DataGETReq('http://%s/RequestData' % (devTargetItem.Device_IP_Address,), timeout=5, auth=(devTargetItem.Device_Name, str(devTargetItem.Device_Unique_ID).replace("-", "")))

                if DevResp.ok:
                    print('Response Result for %s — %s was Successful on Request...\n'% (devTargetItem.Device_Name, devTargetItem.Device_IP_Address,))
                    self.processURL(devTargetItem.Device_Name, devTargetItem.Device_IP_Address, DevResp.content)

            except RequestException:
                print('Response Result for %s — %s was Failed on Request, Skipping It!'% (devTargetItem.Device_Name, devTargetItem.Device_IP_Address,))
        return

    # ! Processes URL given by the NodeMCU into a dictionary for further processing.
    """
        The URL context should have the following:

            - Classroom Assignment
            - Temperature Output
            - Humidity Output
            - Motion Sensor Output
            - Authentication States
                - Recently Opened / Detection / Closed
                - Actual State (Authorized, Unauthorized)
            - Lock States
                - Recently Opened / Closed
        Therefore, the output will be...
        {
            'DATA_HEADER': {'CR_IDENTITY': 'DEV_CR_ASSIGNMENT',  'CR_SHORT_NAME': 'DEV_CR_SHORT_NAME', 'CR_UUID': 'DEV_CR_UUID', 'DEV_NAME': 'AUTH_DEV_USN' ,'DEV_UUID': 'DEV_UUID', 'CURR_COURSE_SESSION': 'CURRENT_COURSE_CODENAME'},
            'DATA_SENS': {'CR_TEMP': 'DHT22_Temp', 'CR_HUMD': 'DHT22_Humid',
            'PIR_MOTION':
                {'PIR_MOTION': 'PIR_Bool', 'PIR_PRESENCE_PRCNT': 'ENV_INST_CONT.PIR_PRESENCE_PERCENTAGE'}
            },
            'DATA_AUTH': {'AUTH_ID':'-1', 'AUTH_STATE': 'AUTH_FGPRT_STATE'},
            'DATA_STATE': {
                'DOOR_STATE': 'AUTH_CR_DOOR', 'ACCESS_STATE': 'AUTH_CR_ACCESS', 'ELECTRIC_STATE': 'NON_AUTH_ELECTRIC_STATE'
            },
        }

    """
    def processURL(self, DevTarget_Name, DevTarget_IP, urlStr):
        print("Processing Context from URL Response for %s | %s..." % (DevTarget_Name, DevTarget_IP,))
        convIoTData = json.loads(urlStr.decode('utf-8').replace("'", "\""))
        print("Context Was Sterelized for %s | %s..." % (DevTarget_Name, DevTarget_IP,))
        return self.interpretData(DevTarget_Name, DevTarget_IP, **convIoTData)

    # ! Interpret Data from the URL by reading them as a dictionary and Take Action about it.
    def interpretData(self, DevInterpret_Name, DevInterpret_IP, **URLSterlData):
        try:
            print('Interpreting Given Context for %s | %s...\n' % (DevInterpret_Name, DevInterpret_IP))
            print("DATA_HEADER => ROOM_ASSIGNMENT: %s | ROOM_NAME: %s | ROOM_UID: %s | DEVICE_NAME: %s | DEVICE_UUID: %s | CURR_COURSE_SESSION: %s" % (URLSterlData['DATA_HEADER']['CR_IDENTITY'], URLSterlData['DATA_HEADER']['CR_SHORT_NAME'], URLSterlData['DATA_HEADER']['CR_UUID'], URLSterlData['DATA_HEADER']['DEV_NAME'], URLSterlData['DATA_HEADER']['DEV_UUID'], URLSterlData['DATA_HEADER']['CURR_COURSE_SESSION']))
            print("DATA_SENS => TEMP: %s | HUMD: %s" % (URLSterlData['DATA_SENS']['CR_TEMP'], URLSterlData['DATA_SENS']['CR_HUMD']))
            print("DATA_SENS => PIR_MOTION => OUTPUT: %s | CALCULATED_PRESENCE: %s" % (URLSterlData['DATA_SENS']['PIR_MOTION']['PIR_OPTPT'], URLSterlData['DATA_SENS']['PIR_MOTION']['PIR_PRESENCE_PRCNT']))
            print("DATA_AUTH => AUTH_ID: %s | AUTH_STATE: %s" % (URLSterlData['DATA_AUTH']['AUTH_ID'], URLSterlData['DATA_AUTH']['AUTH_STATE']))
            print("DATA_STATE => DOOR_STATE: %s | ACCESS_STATE: %s | ELECTRIC_STATE: %s" % (URLSterlData['DATA_STATE']['DOOR_STATE'], URLSterlData['DATA_STATE']['ACCESS_STATE'], URLSterlData['DATA_STATE']['ELECTRIC_STATE']))

            # Get the time first and the day itself.
            timeCurrent = datetime.datetime.now().time()
            dayCurrent = datetime.datetime.now().strftime('%A')

            # First we check if the device is currently associated with one of the rooms. Index 0 to make things clearer that we only need one. And easy to unpack the data.
            classroomPointer = Classroom.objects.filter(Classroom_Dev__Device_Unique_ID=StrToValidUUID(URLSterlData['DATA_HEADER']['DEV_UUID'])).values('Classroom_Unique_ID')[0]

            roomStatusInstance = Classroom.objects.filter(Classroom_Unique_ID=StrToValidUUID(URLSterlData['DATA_HEADER']['CR_UUID'])).distinct()[0]
            roomStatusInstance.Classroom_State = ClassroomStates[0][0] if not URLSterlData['DATA_STATE']['DOOR_STATE'] else ClassroomStates[1][0]
            roomStatusInstance.Classroom_AccessState = ClassroomAccessStates[0][0] if not URLSterlData['DATA_STATE']['ACCESS_STATE'] else ClassroomAccessStates[1][0]
            roomStatusInstance.save(update_fields=['Classroom_State', 'Classroom_AccessState'])

            print('\nQuery | Classroom with %s Found!\n' % URLSterlData['DATA_HEADER']['DEV_UUID'])
            if classroomPointer:
                enlistedScheduleCandidates = CourseSchedule.objects.filter(CourseSchedule_Room__Classroom_Unique_ID=classroomPointer['Classroom_Unique_ID'], CourseSchedule_Lecture_Day=dayCurrent).order_by('CourseSchedule_Session_Start')
                print('Schedule Check | Checking Course Schedules for All Classroom Candidates To %s...\n' % (URLSterlData['DATA_HEADER']['DEV_NAME'],))
                for CourseScheduleItem in enlistedScheduleCandidates:
                    print("Schedule Check | Checking Course's %s Time Scope for Today (%s)..." % (CourseScheduleItem.CourseSchedule_CourseReference.Course_Code, dayCurrent))
                    if timeCurrent >= CourseScheduleItem.CourseSchedule_Session_Start and timeCurrent <= CourseScheduleItem.CourseSchedule_Session_End:
                        #print(timeCurrent, '>=', CourseScheduleItem.CourseSchedule_Session_Start, 'and', timeCurrent,'<=', CourseScheduleItem.CourseSchedule_Session_End)
                        if CourseScheduleItem.CourseSchedule_Availability == 'Not Available' or CourseScheduleItem.CourseSchedule_Availability == None or URLSterlData['DATA_HEADER']['CURR_COURSE_SESSION'] == "Unknown":
                            print('Schedule Override | Overriding Device Configuration...')

                            courseTimeOnScope = CourseScheduleItem.CourseSchedule_CourseReference.Course_Code
                            courseInstructorOnScope = CourseScheduleItem.CourseSchedule_Instructor.fp_id
                            try:
                                devTargetUpdate = DataGETReq('http://%s/RequestInstance?dev_sched_user_course_replace=%s&dev_sched_user_assign_replace=%s&cr_access=%s' % (DevInterpret_IP, courseTimeOnScope, courseInstructorOnScope, True), timeout=5, auth=(URLSterlData['DATA_HEADER']['DEV_NAME'], URLSterlData['DATA_HEADER']['DEV_UUID']))
                                if devTargetUpdate.ok:
                                    CourseScheduleItem.CourseSchedule_Availability='Available'
                                    CourseScheduleItem.save(update_fields=['CourseSchedule_Availability'])
                                    print('Schedule Override | Done!')
                                    self.SubjectOnScope = True
                                    break
                                else:
                                    print('Schedule Override | Failed! Response may be Unauthorized or Forbidden! Retrying At Next Query... Info: %s' % (devTargetUpdate,))

                            except RequestException as Err:
                                print('Error While Requesting Replacement... Info: %s' % Err)
                        else:
                            print('Schedule Override | Override Process was done already! Ignoring it!\n')
                            self.SubjectOnScope = True
                            break
                    else:
                        if CourseScheduleItem.CourseSchedule_Availability == 'Available':
                            CourseScheduleItem.CourseSchedule_Availability = 'Not Available'
                            CourseScheduleItem.save(update_fields=['CourseSchedule_Availability'])

                        #devTargetUpdate = DataGETReq('http://%s/RequestInstance?dev_sched_user_course_replace=%s&dev_sched_user_assign_replace=%s&cr_access=%s' % (DevInterpret_IP, "Unknown", 0, False), timeout=5, auth=(URLSterlData['DATA_HEADER']['DEV_NAME'], URLSterlData['DATA_HEADER']['DEV_UUID']))
                        #self.SubjectOnScope = False
                        print('Schedule Override | Time Scope for Course %s is not on scope within this time!\n' % (CourseScheduleItem.CourseSchedule_CourseReference.Course_Code,))
                else:
                    if not self.SubjectOnScope:
                        devTargetUpdate = DataGETReq('http://%s/RequestInstance?dev_sched_user_course_replace=%s&dev_sched_user_assign_replace=%s&cr_access=%s' % (DevInterpret_IP, "Unknown", 0, False), timeout=5, auth=(URLSterlData['DATA_HEADER']['DEV_NAME'], URLSterlData['DATA_HEADER']['DEV_UUID']))
                        print('Schedule Override | No Other Such Subject Candidates! Device Access Disabled.')
                    else:
                        print("Schedule Override | There's a subject currently on schedule runtime! Device Access Enabled.")


            print('Schedule Check | Course Schedules Availability Updated!')
            # Next, we get all the schedule based on time scope and should be matched with the classroom associated device.

        except BaseException as error:
            print('Exception: An error occurred: %s' % (error,))
        return

    def dayCheckScheduleUpdate(self):
        return

if __name__ == '__main__':
    CommandLine('CLS', shell=True)
    delay(0.5)
    run()
