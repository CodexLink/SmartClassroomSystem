#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SmartClassroom.settings')

    os.system("title SmartClassroom Django Server Handler")
    os.system("CLS")

    print('SmartClassroom Django Server Handler | < Django Project Caller >')
    print('02/29/2020 | By Janrey "CodexLink" Licas | http://github.com/CodexLink\n')
    print('In Collaboration with')
    print('    - Ronald Langaoan Jr. |> Hardware Designer and Manager')
    print('    - Janos Angelo Jantoc |> Hardware Designer and Assistant Programmer')
    print('    - Joshua Santos |> Hardware Manager and Builder')
    print('    - Johnell Casey Murillo Panotes |> Hardware Assistant\n')

    try:
        from django.core.management import execute_from_command_line

    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
