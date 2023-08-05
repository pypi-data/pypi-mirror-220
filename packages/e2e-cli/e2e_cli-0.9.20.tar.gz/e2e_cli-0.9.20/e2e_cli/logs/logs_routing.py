import subprocess

from e2e_cli.core.py_manager import PyVersionManager
from e2e_cli.core import show_messages, constants
from e2e_cli.logs import logs_service


class LogRouting:
    def __init__(self, arguments):
        self.arguments = arguments

    def route(self, parsing_errors):
        if (self.arguments.args.log_commands is None):
            show_messages.show_parsing_error(parsing_errors)
            subprocess.call([constants.E2E_CLI, constants.LOGS, constants._HELP])

        elif (self.arguments.args.log_commands is not None):
            logs_operations = logs_service.caller(
                self.arguments.args.log_commands)
            if logs_operations:
                logs_operations()

        else:
            print("command not found")
            show_messages.show_parsing_error(parsing_errors)
