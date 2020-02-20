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
from requests.exceptions import ConnectionError
from SC_NodeCandidates import NodeDevCandidates  # NodeMCU Candidates
from SCMySQLDB import MySQLEssentialHelper as SCMySQL


## Main Driver Class
class SC_IoTDriver(SCMySQL):
    # On Starting Point we have to supply the given arguments to __init__() function.
    # ! Because we have to initialize the class from the object itself.
    def __init__(self, COMPort=None, BaudRate=None, TimeoutCheck=3, **NodeCandidates):
        super().__init__(ServerHost='localhost', UCredential='root', PCredential=None, DB_Target='sc_db') # ! We have to initialize superclass 'MySQLEssentialHelper' to gather functions from 'that' class.

        self.TimeoutDevCheck = TimeoutCheck
        return

    # ! First Step | Initialization | We check a list of NodeMCUs to be scanned.
    def checkNodeConn(self, **NodeDict):
        # ! Add Indicators. User actions will be dependent upon this.
        errCount = 0
        passCount = 0

        print("Device List | Checking...")
        if not len(NodeDict):
            print('Count Result | There are no NodeMCU declared from the container! Please check them and correct them if possible!!!')
            Terminate()
        else:
            print("Count Result | The dictionary contains %s Devices to be scanned...\n" % (len(NodeDict)))

    # * IF a device is not included to the list but WAS included to the DJango Database then we set their states as Unknown.
        for DevNumber, (DevName, DevIP) in enumerate(NodeDevCandidates.items()):
            try:
                print('Device #%s | %s — %s | Connection Checking... |  '% (DevNumber + 1, DevName, DevIP,), end='')
                DevResp = DataGETReq('http://%s/RequestData' % (DevIP,), timeout=self.TimeoutDevCheck)

                if DevResp.ok:
                    print('Response Success.')
                    passCount += 1
                else:
                    print('Response Failed / No Content.')
                    errCount += 1

            except ConnectionError:
                print('Response Failed.')
                errCount += 1
                pass

        print('Device Checking Finished... (Success: %s, Failed: %s)' % (passCount, errCount))

        if passCount and errCount:
            print("There's are some devices that didn't passed from the connection test. Are you sure you want to continue?")
            print("NOTE |> They are still included from querying over but will be ignored or passed if they are still not responding from REQUESTs.")
            userAcc = input(str("Input [Y/N] |> "))
            return True if userAcc in ('Y', 'y') else False

        elif not passCount and errCount:
            print("All devices were not able to pass from the connection test. Please check their corresponding IP Addresses!")
            Terminate()

    # ! Step 2 | Connect To Them Individual and Check For Datas
    def getNewData(self, **IndivDevice):
        for DevName, DevIP in IndivDevice.items():
            try:
                print('Current Device Query | %s — %s'% (DevName, DevIP,))
                DevResp = DataGETReq('http://%s/RequestData' % (DevIP,), timeout=self.TimeoutDevCheck)

                if DevResp.ok:
                    print('Response Success | %s — %s\n'% (DevName, DevIP,))
                    self.processURL(DevName, DevIP, DevResp.content)

            except ConnectionError:
                print('Response Failed | %s — %s, Skipped...'% (DevName, DevIP,))
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
        Therefore,
        {'cr_assigned': '', 'temp_optpt': '', 'humid_optpt': '', 'authentication': {'recent_detection' : '', 'state' : ''}, 'door_lock': ''}
    """
    def processURL(self, DevTarget_Name, DevTarget_IP, urlStr):
        print("%s | %s | Processing Context from URL Response." % (DevTarget_Name, DevTarget_IP,))
        convIoTData = json.loads(urlStr.decode('utf-8').replace("'", "\""))
        return self.interpretData(DevTarget_Name, DevTarget_IP, **convIoTData)

    # ! Interpret Data from the URL by reading them as a dictionary.
    def interpretData(self, DevInterpret_Name, DevInterpret_IP, **URLSterlData):
        print('%s | %s | Interpreting Context.' % (DevInterpret_Name, DevInterpret_IP))
        return print(URLSterlData)

    # ! We take action and do something about the data. It can be, Data Change, State Change, Logging such as [Sensor Data, UUID Data, and Status for Entries and Etc.],
    def takeAction(self, ActionType=None):
        pass


if __name__ == '__main__':
    CommandLine('CLS', shell=True)
    print('Smart Classroom IoT Data Receiver')
    print("Created by Ronald Langaoan, Janrey Tuazon Licas, Janos Angelo Garcia Jantoc and Johnell Casey Murillo Panotes, and Joshua Santos\n")
    delay(1.3)

    # * We initialize this class with parameters. You can provide your own container by declaring at this scope.
    # ! Means you can change NodeDevCandidate Declaration Here.
    # * This is a reason why it was declared in the first place. Not directly.
    SessionInstance = SC_IoTDriver(**NodeDevCandidates)

    if SessionInstance.checkNodeConn(**NodeDevCandidates): # Test All Connections To The IoT Devices.
        try:
            while 1:
                SessionInstance.getNewData(**NodeDevCandidates)
                print('Device Query | Done. Waiting for 2 Minutes Before Re-Querying...\n')
                delay(2 * 60) # ! 2 Minutes
        except:
            pass
    else:
         Terminate()
    # ! At this point, we keep looping from the device for 5 minutes. That triggers IF and only all scanning to the database were done.
