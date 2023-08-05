import subprocess

from e2e_cli.bucket_store.bucket_actions.bucket_actions import BucketActions
from e2e_cli.bucket_store.bucket_crud.bucket_storage import BucketCrud
from e2e_cli.core import show_messages, constants
from e2e_cli.core.py_manager import PyVersionManager


class BucketRouting:
    def __init__(self, arguments):
        self.arguments = arguments

    def route(self, parsing_errors):
        if (self.arguments.args.bucket_commands is None) and (self.arguments.args.action is None):
            show_messages.show_parsing_error(parsing_errors)
            subprocess.call([constants.E2E_CLI,  constants.BUCKET, constants._HELP])

        elif (self.arguments.args.bucket_commands is not None) and (self.arguments.args.action is not None):
            print("Only one action at a time !!")

        elif (self.arguments.args.bucket_commands is not None):
            bucket_operations = BucketCrud(
                alias=self.arguments.args.alias, inputs=self.arguments.inputs)
            if bucket_operations.possible:
                operation = bucket_operations.caller(
                    self.arguments.args.bucket_commands)
                if operation:
                    operation()

        elif (self.arguments.args.action is not None):
            bucket_operations = BucketActions(
                alias=self.arguments.args.alias, inputs=self.arguments.inputs)
            if bucket_operations.possible:
                operation = bucket_operations.caller(
                    self.arguments.args.action)
                if operation:
                    operation()

                else:
                    print("command not found")
                    show_messages.show_parsing_error(parsing_errors)

        else:
            print("command not found")
            show_messages.show_parsing_error(parsing_errors)
