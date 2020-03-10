"""
    ! Smart Classroom IoT Script Instantiator | SC_ScriptInst.py
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

import os
import time
from subprocess import PIPE, Popen, run
from sys import platform as ReturnedOSName

SERVER_IP = '0.0.0.0'
SERVER_PORT = 8000

try:
    os.system('CLS')
    os.system('title Smart Classroom IoT Script Instantiator')

    print("Smart Classroom IoT Script Instantiator | SC_ScriptInst.py")
    print('02/29/2020 | By Janrey "CodexLink" Licas | http://github.com/CodexLink\n')
    print('In Collaboration with')
    print('    - Ronald Langaoan Jr. |> Hardware Designer and Manager')
    print('    - Janos Angelo Jantoc |> Hardware Designer and Assistant Programmer')
    print('    - Joshua Santos |> Hardware Manager and Builder')
    print('    - Johnell Casey Murillo Panotes |> Hardware Assistant\n')

    if ReturnedOSName == "win32":
        print("OS Name | Detected Windows...\n")
        os.chdir('SmartClassroom/')
        print("Process | Instantiating Smart Classroom DJango Deployment Server...")
        Popen("start python manage.py runserver %s:%s" % (SERVER_IP, SERVER_PORT), stdin=PIPE, stdout=PIPE, shell=True)
        print("Process | Instantiated!\n")

        print("Process | Instantiating Smart Classroom Data Stream Handler in DJango via RunScript... ")
        Popen("start python manage.py runscript SC_DSH", stdin=PIPE, stdout=PIPE, shell=True)
        print("Process | Instantiated!\n")

        print("Press CTRL+C or CTRL+BREAK to kill all handler instance and this threader.\n")
        while True:
            pass

    elif ReturnedOSName == "linux":
        print("OS Name | Detected Linux..\n.")
        print("Platform Instance for Linux Will Be Added Soon!")
        exit(1)

    else:
        print("Platform Undetermined!")
        exit(-1)

except KeyboardInterrupt:
    if ReturnedOSName == "win32":
        run("""TASKKILL /F /FI "WINDOWTITLE eq SmartClassroom Data Stream Handler" /T""", shell=False)
        run("""TASKKILL /F /FI "WINDOWTITLE eq SmartClassroom Django Server Handler" /T""", shell=False)
        print("\nAll Threads Closed. Thank you!\n")

    else:
        print("Platform Undetermined!")
        exit(-1)
