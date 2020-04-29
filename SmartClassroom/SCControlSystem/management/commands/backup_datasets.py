"""
    create_definitive_groups.py
    A command script to be used to automate groups which can be easily be referenced later.
    Created on 01/28/2020
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission


class Command(BaseCommand):
    help = 'Automates back up process by taking all data from the current state of the database.'

    def add_arguments(self, parser):
        parser.add_argument(
            '-a',
            '--action',
            type=str,
            help='[start, rebuild] Repopulate Group'
            's Model Content by Deleting Everything or Adds All Content and Assign Permissions To Group.'
        )

    def handle(self, *args, **options):
        usage_param = options['action']

        if usage_param == "start":
            pass

        elif usage_param == "rebuild":
            object_process_count = 1

            self.stdout.write(
                self.style.NOTICE(
                    'Start | Initiating Rebuild of Groups Model with Permissions...'
                ))
            try:
                self.stdout.write(
                    self.style.NOTICE(
                        'Step 1 | Delete Groups Object by All().Delete()'))
                Group.objects.all().delete()
                self.stdout.write(self.style.NOTICE('Step 1 | Success...'))

                self.stdout.write(
                    self.style.NOTICE(
                        'Step 2 | Repopulate Group Object with Selected Permissions'
                    ))

                for RolesDefined in RoleDeclaredTypes:
                    self.stdout.write(
                        self.style.NOTICE(
                            'Step 2.%s | Repopulate -> %s' %
                            (object_process_count, RolesDefined)))
                    permissionPermission.objects.get()
                    Group.objects.create(name=RolesDefined, permissions)
                    #Group.object
                    object_process_count += 1

                self.stdout.write(self.style.NOTICE('Step 2 | Success...'))

            except (ProgrammingError) as ErrMsg:
                self.stderr.write(
                    self.style.ERROR(
                        'Error | Unable to proceed further. Technical Information | %s'
                        % ErrMsg))
                pass
            pass
        else:
            self.stderr.write(
                self.style.ERROR(
                    'Start | Create Definitive Group Script has received invalid argument: %s'
                    % usage_param['action']))
