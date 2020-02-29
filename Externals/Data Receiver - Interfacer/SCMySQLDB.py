"""
    ! Smart Classroom IoT Data Receiver | MySQL Wrapper | SCMySQLDB
    Created by Janrey "CodexLink" Licas — https://github.com/CodexLink

#  A Wrapper Class that contains all MySQL functions. Created for Easy Debugging.
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