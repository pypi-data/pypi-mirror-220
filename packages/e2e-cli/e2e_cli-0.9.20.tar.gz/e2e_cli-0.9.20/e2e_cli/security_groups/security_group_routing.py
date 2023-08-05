import subprocess

from e2e_cli.core.py_manager import PyVersionManager
from e2e_cli.core import show_messages
from e2e_cli.security_groups.security_group_api import SecurityGroup


class SecurityGroupRouting:
    def __init__(self, arguments):
        self.arguments = arguments

    def route(self, parsing_errors):
        # if (self.arguments.args.autoscaling_commands is None):
        #     show_messages.show_parsing_error(parsing_errors)

        if (self.arguments.args.command is not None):
            security_groups = SecurityGroup(
                alias=self.arguments.args.alias, inputs=self.arguments.inputs)
            if security_groups.possible:
                operation = security_groups.caller("list")
                operation()

        else:
            print("command not found")
            show_messages.show_parsing_error(parsing_errors)
