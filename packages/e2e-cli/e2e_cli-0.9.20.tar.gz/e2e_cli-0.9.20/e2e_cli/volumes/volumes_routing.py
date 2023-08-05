import subprocess

from e2e_cli.core.py_manager import PyVersionManager
from e2e_cli.core import show_messages, constants
from e2e_cli.volumes.volumes_crud.volumes import VolumesCrud
from e2e_cli.volumes.volumes_actions.volumes_action import VolumesActions


class VolumesRouting:
    def __init__(self, arguments):
        self.arguments = arguments

    def route(self,  parsing_errors):
        if (self.arguments.args.action is None) and (self.arguments.args.volumes_commands is None):
            show_messages.show_parsing_error(parsing_errors)
            subprocess.call([constants.E2E_CLI, constants.VOLUME, constants._HELP])

        elif (self.arguments.args.volumes_commands is not None) and (self.arguments.args.action is not None):
            print("Only one action at a time !!")

        elif (self.arguments.args.volumes_commands is not None):
            volumes_operations = VolumesCrud(
                alias=self.arguments.args.alias, inputs=self.arguments.inputs)
            if volumes_operations.possible:
                operation = volumes_operations.caller(
                    self.arguments.args.volumes_commands)
                if operation:
                    operation()

                else:
                    print("command not found")
                    show_messages.show_parsing_error(parsing_errors)
        # elif self.arguments.args.action == "attach_volume":
        #     volumes_operations = volumesActions(alias=self.arguments.args.alias, inputs=self.arguments.inputs)
        #     if(volumes_operations.possible):
        #                 try:
        #                     volumes_operations.attach_volume()
        #                 except KeyboardInterrupt:
        #                     print(" ")

        # elif self.arguments.args.action == "desable_volumes":
        #     volumes_operations = volumesActions(alias=self.arguments.args.alias, inputs=self.arguments.inputs)
        #     if(volumes_operations.possible):
        #                 try:
        #                     volumes_operations.disable_volumes()
        #                 except KeyboardInterrupt:
        #                     print(" ")

        else:
            print("command not found")
            show_messages.show_parsing_error(parsing_errors)
