#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from sys import platform as ReturnedOSName

## REQUIRED WHEN RUNNING ON LOCAL REPOSITORY OR CODE COVERAGE IS ENABLED.
# ! The value of `reqCovPercentage` must be inlined with the value of `fail_under` inside .coveragerc.
reqCovPercentage = 85

def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SmartClassroom.settings")

    if ReturnedOSName == "win32":
        os.system("title Smart Classroom Django Server Handler")
        os.system("CLS")
    elif ReturnedOSName == "linux":
        pass
    else:
        exit(-1)

    print("Smart Classroom Django Server Handler | < Django Project Caller >")
    print('02/29/2020 | By Janrey "CodexLink" Licas | http://github.com/CodexLink\n')
    print("In Collaboration with")
    print("    - Ronald Langaoan Jr. |> Hardware Designer and Manager")
    print("    - Janos Angelo Jantoc |> Hardware Designer and Assistant Programmer")
    print("    - Joshua Santos |> Hardware Manager and Builder")
    print("    - Johnell Casey Murillo Panotes |> Hardware Assistant\n")

    if sys.argv[1] == "test":
        print("\n - Coverage Report Activated!")
        from coverage import Coverage
        print("| - Coverage > Importing...")
        baseCov = Coverage()
        print("| - Coverage > Initializing...")
        baseCov.erase()
        print("| - Coverage > Erasing Recent Reports...")
        baseCov.start()
        print("| - Coverage > Code Coverage Start!")

    try:
        from django.core.management import execute_from_command_line

    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

    if sys.argv[1] == "test":
        baseCov.stop()
        baseCov.save()
        baseCovReport = baseCov.report()
        print("\n | - Coverage > Report Saved.")
        baseCov.html_report()
        if baseCovReport < reqCovPercentage:
            print("\n | - Coverage > Code Coverage Completed But Fails To Meet Required Passing Rate of {0}%...".format(reqCovPercentage))
        else:
            print("\n | - Coverage > Code Coverage Completed and Passed Above Required Passing Rate of {0}%!".format(reqCovPercentage))

        print("\n | - Coverage > Done~!")
        sys.exit(0)

if __name__ == "__main__":
    main()
