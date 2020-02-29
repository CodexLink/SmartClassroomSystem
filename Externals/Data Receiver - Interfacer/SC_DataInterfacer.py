"""
    ! Smart Classroom IoT Data Receiver
    Local Fork Repo of RGB Name Definition Finder | Python Interfacer Made for Embedded Systems | Prelim Case Study
    # https://github.com/CodexLink/RGBPotentIdentifier

        *  Created by Janrey "CodexLink" Licas
        *  Supported by Janos Angelo Jantoc

    github.com/CodexLink

"""
import json
from subprocess import call as CommandLine
from sys import exit as Terminate
from time import sleep as delay

from requests import get as DataGETReq
from requests.exceptions import RequestException
from SCMySQLDB import MySQLEssentialHelper as SCMySQL


## Main Driver Class
class SC_IoTDriver(SCMySQL):
    # On Starting Point we have to supply the given arguments to __init__() function.
    # ! Because we have to initialize the class from the object itself.
    def __init__(self, COMPort=None, BaudRate=None, TimeoutCheck=2):
        super().__init__(ServerHost='localhost', UCredential='root', PCredential=None, DB_Target='sc_db') # ! We have to initialize superclass 'MySQLEssentialHelper' to gather functions from 'that' class.

        self.TimeoutDevCheck = TimeoutCheck
        return

    # ! First Step | Initialization | We check a list of NodeMCUs to be scanned.
    def checkNodeConn(self, CheckBeforeReQueue=False):
        # ! Add Indicators. User actions will be dependent upon this.
        errCount = 0
        passCount = 0
        devList = self.MySQL_ExecuteState("SELECT Device_Name, Device_IP_Address, Device_Unique_ID from dev_decl", "FetchAll")

        print("Device List | Checking...")
        if not len(devList):
            print('Count Result | There are no NodeMCUs declared from the container! Please check them and correct them if possible!!!')
            Terminate()
        else:
            print("Count Result | The dictionary contains %s devices to be scanned...\n" % (len(devList)))

        print('Additional Step | Setting Timeout Based from CheckBeforeReQueue Parameter.')
        self.TimeoutDevCheck = 1.3 if CheckBeforeReQueue else 2
        print('Addtional Step | Timeout Set.\n')

    # * IF a device is not included to the list but WAS included to the DJango Database then we set their states as Unknown.
        if CheckBeforeReQueue:
            print('Required Reiteration | Device Requeueing...')

        for listCandidates in devList:
            try:

                print('Device %s — %s | Checking... |  ' % (listCandidates['Device_Name'], listCandidates['Device_IP_Address']), end='')
                DevResp = DataGETReq('http://%s/RequestData' % (listCandidates['Device_IP_Address'],), timeout=self.TimeoutDevCheck, auth=(listCandidates['Device_Name'], listCandidates['Device_Unique_ID'].replace("-", "")))
                if DevResp.ok:
                    print('Response Success.')
                    self.MySQL_ExecuteState("UPDATE dev_decl SET Device_Status='Online' WHERE Device_Name='%s' AND Device_IP_Address='%s' AND Device_Unique_ID='%s'" % (listCandidates['Device_Name'], listCandidates['Device_IP_Address'], listCandidates['Device_Unique_ID']))
                    passCount += 1
                else:
                    print('Response Failed / No Content.')
                    errCount += 1

            except RequestException:
                self.MySQL_ExecuteState("UPDATE dev_decl SET Device_Status='Offline' WHERE Device_Name='%s' AND Device_IP_Address='%s' AND Device_Unique_ID='%s'" % (listCandidates['Device_Name'], listCandidates['Device_IP_Address'], listCandidates['Device_Unique_ID']))
                print('Response Failed.')
                errCount += 1
                pass

        print('\nDevice Checking Finished... (Success: %s, Failed: %s)\n' % (passCount, errCount))
        if not CheckBeforeReQueue:
            if passCount and errCount:
                print("There's are some devices that didn't passed from the connection test. Are you sure you want to continue?")
                print("NOTE |> They are still included from querying over but will be ignored or passed if they are still not responding from REQUESTs.")
                userAcc = input(str("Input [Y/N] |> "))
                return True if userAcc in ('Y', 'y') else False

            elif not passCount and errCount:
                print("All devices were not able to pass from the connection test. Please check the device candidate information!")
                Terminate()
        else:
            print("Device Requeue Done.")
            return True


    # ! Step 2 | Connect To Them Individual and Check For Datas
    def getNewData(self):
        devMetaData = self.MySQL_ExecuteState("SELECT Device_Name, Device_IP_Address, Device_Unique_ID from dev_decl WHERE Device_Status = 'Online'", "FetchAll")
        for listCandidates in devMetaData:
            try:
                print('\nJob | Device Currently on Process Query is %s — %s'% (listCandidates['Device_Name'], listCandidates['Device_IP_Address'],))
                DevResp = DataGETReq('http://%s/RequestData' % (listCandidates['Device_IP_Address'],), timeout=self.TimeoutDevCheck, auth=(listCandidates['Device_Name'], listCandidates['Device_Unique_ID'].replace("-", "")))

                if DevResp.ok:
                    print('Response Result for %s — %s was Successful on Request...\n'% (listCandidates['Device_Name'], listCandidates['Device_IP_Address'],))
                    self.processURL(listCandidates['Device_Name'], listCandidates['Device_IP_Address'], DevResp.content)

            except RequestException:
                print('Response Result for %s — %s was Failed on Request, Skipping It!'% (listCandidates['Device_Name'], listCandidates['Device_IP_Address'],))
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
            'DATA_HEADER': {'CR_IDENTITY': 'DEV_CR_ASSIGNMENT',  'CR_SHORT_NAME': 'DEV_CR_SHORT_NAME', 'CR_UUID': 'DEV_CR_UUID', 'DEV_NAME': 'AUTH_DEV_USN' ,'DEV_UUID': 'DEV_UUID'},
            'DATA_SENS': {'CR_TEMP': 'DHT22_Temp', 'CR_HUMD': 'DHT22_Humid', 'CR_HTINX': '',
            'PIR_MOTION':
                {'PIR_MOTION': 'PIR_Bool', 'PIR_OTPT_TIME_TRIGGER': 'PIR_MILLIS_TRIGGER'}
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
            print("DATA_HEADER => ROOM_ASSIGNMENT: %s | ROOM_NAME: %s | ROOM_UID: %s | DEVICE_NAME: %s | DEVICE_UUID: %s" % (URLSterlData['DATA_HEADER']['CR_IDENTITY'], URLSterlData['DATA_HEADER']['CR_SHORT_NAME'], URLSterlData['DATA_HEADER']['CR_UUID'], URLSterlData['DATA_HEADER']['DEV_NAME'], URLSterlData['DATA_HEADER']['DEV_UUID']))
            print("DATA_SENS => TEMP: %s | HUMD: %s | HTINDEX: %s" % (URLSterlData['DATA_SENS']['CR_TEMP'], URLSterlData['DATA_SENS']['CR_HUMD'], URLSterlData['DATA_SENS']['CR_HTINX']))
            print("DATA_SENS => PIR_MOTION => OUTPUT: %s | TIME_TRIGGER: %s" % (URLSterlData['DATA_SENS']['PIR_MOTION']['PIR_OPTPT'], URLSterlData['DATA_SENS']['PIR_MOTION']['PIR_OTPT_TIME_TRIGGER']))
            print("DATA_AUTH => AUTH_ID: %s | AUTH_STATE: %s" % (URLSterlData['DATA_AUTH']['AUTH_ID'], URLSterlData['DATA_AUTH']['AUTH_STATE']))
            print("DATA_STATE => DOOR_STATE: %s | ACCESS_STATE: %s | ELECTRIC_STATE: %s" % (URLSterlData['DATA_STATE']['DOOR_STATE'], URLSterlData['DATA_STATE']['ACCESS_STATE'], URLSterlData['DATA_STATE']['ELECTRIC_STATE']))
        except BaseException as error:
            print('An exception occurred: {}'.format(error))
        return

if __name__ == '__main__':
    CommandLine('CLS', shell=True)
    print('Smart Classroom IoT Data Receiver')
    print("Created by Ronald Langaoan, Janrey Tuazon Licas, Janos Angelo Garcia Jantoc and Johnell Casey Murillo Panotes, and Joshua Santos\n")
    delay(1.3)

    # * We initialize this class with parameters. You can provide your own container by declaring at this scope.
    # ! Means you can change NodeDevCandidate Declaration Here.
    # * This is a reason why it was declared in the first place. Not directly.
    SessionInstance = SC_IoTDriver()

    if SessionInstance.checkNodeConn(): # Test All Connections To The IoT Devices.
        try:
            while 1:
                SessionInstance.getNewData()
                SessionInstance.checkNodeConn(CheckBeforeReQueue=True) # Test All Connections To The IoT Devices.
                print('Timeout | Resting for 30 Seconds...\n')
                # Add Scheduler Checker Now.
                delay(30) # ! 30 Seconds
        except:
            pass
    else:
         Terminate()
    # ! At this point, we keep looping from the device for 5 minutes. That triggers IF and only all scanning to the database were done.
