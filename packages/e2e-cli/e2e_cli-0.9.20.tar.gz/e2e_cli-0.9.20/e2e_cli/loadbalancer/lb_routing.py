import subprocess

from e2e_cli.core.py_manager import PyVersionManager
from e2e_cli.core import show_messages, constants
from e2e_cli.loadbalancer.lb import LBClass


class LBRouting:
    def __init__(self, arguments):
        self.arguments = arguments

    def route(self, parsing_errors):
        if self.arguments.args.lb_commands is None:
            show_messages.show_parsing_error(parsing_errors)
            subprocess.call([constants.E2E_CLI,  constants.LB, constants._HELP])

        elif (self.arguments.args.lb_commands is not None):
            lb_class_object = LBClass(
                alias=self.arguments.args.alias, inputs=self.arguments.inputs)
            operation = lb_class_object.caller(
                self.arguments.args.lb_commands)
            if operation:
                try:
                    operation()
                except KeyboardInterrupt:
                    print(" ")
