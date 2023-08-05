import subprocess

from e2e_cli.auto_scaling.auto_scaling import AutoscalingCrud
from e2e_cli.core import show_messages, constants
from e2e_cli.core.py_manager import PyVersionManager


class AutoscalingRouting:
    def __init__(self, arguments):
        self.arguments = arguments

    def route(self, parsing_errors):
        if (self.arguments.args.autoscaling_commands is None):
            show_messages.show_parsing_error(parsing_errors)
            subprocess.call([constants.E2E_CLI, constants.AUTOSCALING, constants._HELP])

        # elif (self.arguments.args.autoscaling_commands is not None) and (self.arguments.args.action is not None):
        #       print("Only one action at a time !!")

        elif (self.arguments.args.autoscaling_commands is not None):
            auto_scaling_operations = AutoscalingCrud(
                alias=self.arguments.args.alias, inputs=self.arguments.inputs)
            if auto_scaling_operations.possible:
                operation = auto_scaling_operations.caller(
                    self.arguments.args.autoscaling_commands)
                if operation:
                    operation()

        else:
            print("command not found")
            show_messages.show_parsing_error(parsing_errors)
