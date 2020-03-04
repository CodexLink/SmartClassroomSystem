"""
    ! Smart Classroom IoT Data Stream MySQL Wrapper | SCMySQLDB.py
    02/29/2020 | Janrey "CodexLink" Licas | http://github.com/CodexLink

    ! In Collaboration with
        - Ronald Langaoan Jr. |> Hardware Designer and Manager
        - Janos Angelo Jantoc |> Hardware Designer and Assistant Programmer
        - Joshua Santos |> Hardware Manager and Builder
        - Johnell Casey Murillo Panotes |> Hardware Assistant

    @required_by: Smart Classroom IoT Data Stream Handler | SC_DSH.py
    @descrip: A Wrapper Class that contains all MySQL functions.
            : It was created to isolate the DB Code from Main Driver Code for SC_DSH.py
            : This was also meant to be isolated for easy debugging.

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

from sys import exit as Terminate

import pymysql as MySQLConnector

# ! This Class contains minimal functions that is wrapped. Unlike PyODBC, it contains additional function that can be used for better debugging experience.
class MySQLEssentialHelper(object):

    # * We initialize our MySQL by __init__ without using any OpenCon() or doing it manually.
    def __init__(self, ServerHost=None, UCredential=None, PCredential=None, DB_Target=None):
        try:
            self.MySQLDataWire = MySQLConnector.connect(host=ServerHost, user=UCredential, password=PCredential, db=DB_Target, charset='utf8mb4', cursorclass=MySQLConnector.cursors.DictCursor)

        except MySQLConnector.MySQLError as OpenConErrorMsg:
            print('Connection Error | Cannot Connect to Database. Detailed Info |> %s' % OpenConErrorMsg)
            Terminate()  # ! Terminate the program, when we're unable to connect to the database.

    # ! Execute Statement Given with the IoT Data Attached to it.
    def MySQL_ExecuteState(self, ExecuteStatement, FetchType=None):
        try:
            cursorSet = self.MySQLDataWire.cursor()
            cursorSet.execute(ExecuteStatement)

            if FetchType == "FetchOne":
                return cursorSet.fetchone()
            elif FetchType == "FetchAll":
                return cursorSet.fetchall()
            else:
                return self.MySQLDataWire.commit()

        except MySQLConnector.MySQLError as ExecErrMsg:
            print('Execution State Error | Please check your MySQL statements. | Detailed Info |> %s' % ExecErrMsg)

    # ! Commits Data from IoT Device after all processing them.
    def MSSQL_CommitData(self, SourceFunction=None):
        try:
            return self.MySQLDataWire.commit()

        except MySQLConnector.MySQLError as CommitError:
            print('Commitment Error | [Unexplainable Reason.] | Detailed Info |> %s' % CommitError)
