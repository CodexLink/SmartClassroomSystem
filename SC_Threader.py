"""
    ! Smart Classroom IoT Data Stream Handler | SC_DSH.py
    02/29/2020 | Janrey "CodexLink" Licas | http://github.com/CodexLink

    ! In Collaboration with
        - Ronald Langaoan Jr. |> Hardware Designer and Manager
        - Janos Angelo Jantoc |> Hardware Designer and Assistant Programmer
        - Joshua Santos |> Hardware Manager and Builder
        - Johnell Casey Murillo Panotes |> Hardware Assitant

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

from subprocess import CREATE_NEW_CONSOLE, Popen, PIPE, STDOUT
import os
import signal

SERVER_IP = '0.0.0.0'
SERVER_PORT = 8000
try:
    print("Launching Smart Classroom Data Receiver / Interfacer... ")

    os.chdir('Externals/DataStream_Handler')
    StreamHandlerInstance = Popen("start python SC_DSH.py", creationflags=CREATE_NEW_CONSOLE, shell=True)

    print("Launching DJango Instance with Arguments... ")

    os.chdir('../../SmartClassroom')
    ServerHandlerInstance = Popen("start python manage.py runserver %s:%s" % (
        SERVER_IP, SERVER_PORT), creationflags=CREATE_NEW_CONSOLE, shell=True)

    print("Press Control+C to kill all instance and this threader.")
    while True:
        pass
except KeyboardInterrupt:
    Popen("TASKKILL /F /PID %s /T" % (StreamHandlerInstance.pid))
    Popen("TASKKILL /F /PID %s /T" % (ServerHandlerInstance.pid))
    print("All Threads Closed. Thank you!")
