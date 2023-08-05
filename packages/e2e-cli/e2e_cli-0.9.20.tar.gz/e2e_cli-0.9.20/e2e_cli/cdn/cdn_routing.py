import subprocess

from e2e_cli.cdn.cdn_actions.cdn_action import CdnActions
from e2e_cli.cdn.cdn_crud.cdn import CdnCrud
from e2e_cli.core import show_messages, constants
from e2e_cli.core.py_manager import PyVersionManager


class CdnRouting:
    def __init__(self, arguments):
        self.arguments = arguments

    def route(self, parsing_errors):
        if (self.arguments.args.action is None) and (self.arguments.args.cdn_commands is None):
            show_messages.show_parsing_error(parsing_errors)
            subprocess.call([constants.E2E_CLI, constants.CDN, constants._HELP])

        elif (self.arguments.args.cdn_commands is not None) and (self.arguments.args.action is not None):
            print("Only one action at a time !!")

        elif (self.arguments.args.cdn_commands is not None):
            cdn_operations = CdnCrud(
                alias=self.arguments.args.alias, inputs=self.arguments.inputs)
            if cdn_operations.possible:
                operation = cdn_operations.caller(
                    self.arguments.args.cdn_commands)
                if operation:
                    operation()

        elif (self.arguments.args.action is not None):
            cdn_operations = CdnActions(
                alias=self.arguments.args.alias, inputs=self.arguments.inputs)
            if cdn_operations.possible:
                operation = cdn_operations.caller(
                    self.arguments.args.action)
                if operation:
                    operation()

                else:
                    print("command not found")
                    show_messages.show_parsing_error(parsing_errors)

        else:
            print("command not found")
            show_messages.show_parsing_error(parsing_errors)
