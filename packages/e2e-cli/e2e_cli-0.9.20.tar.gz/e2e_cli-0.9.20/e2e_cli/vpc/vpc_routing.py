import subprocess

from e2e_cli.core.py_manager import PyVersionManager
from e2e_cli.core import show_messages, constants
from e2e_cli.vpc.vpc import VpcCrud


class VpcRouting:
    def __init__(self, arguments):
        self.arguments = arguments

    def route(self, parsing_errors):
        if (self.arguments.args.vpc_commands is None):
            show_messages.show_parsing_error(parsing_errors)
            subprocess.call([constants.E2E_CLI, constants.VPC, constants._HELP])

        # elif (self.arguments.args.vpc_commands is not None) and (self.arguments.args.action is not None):
        #     print("Only one action at a time !!")

        elif (self.arguments.args.vpc_commands is not None):
            vpc_operations = VpcCrud(
                alias=self.arguments.args.alias, inputs=self.arguments.inputs)
            if vpc_operations.possible:
                operation = vpc_operations.caller(
                    self.arguments.args.vpc_commands)
                if operation:
                    operation()

                else:
                    print("command not found")
                    show_messages.show_parsing_error(parsing_errors)

        else:
            print("command not found")
            show_messages.show_parsing_error(parsing_errors)
