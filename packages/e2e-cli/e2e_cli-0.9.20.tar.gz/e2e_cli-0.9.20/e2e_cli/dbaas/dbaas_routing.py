import subprocess

from e2e_cli.core.py_manager import PyVersionManager
from e2e_cli.core import show_messages, constants
from e2e_cli.dbaas.dbaas_crud.dbaas import DBaaSCrud
from e2e_cli.dbaas.dbaas_crud.dbaas_cli import DbaaSCrud
from e2e_cli.dbaas.dbaas_actions.dbaas_action import DBaasAction


class DBaaSRouting:
    def __init__(self, arguments):
        self.arguments = arguments

    def route(self, parsing_errors):
        if (self.arguments.args.dbaas_commands is None) and (self.arguments.args.action is None):
            show_messages.show_parsing_error(parsing_errors)
            subprocess.call([constants.E2E_CLI,  constants.DBAAS, constants._HELP])

        elif (self.arguments.args.dbaas_commands is not None) and (self.arguments.args.action is not None):
            print("Only one action at a time !!")

        elif (self.arguments.args.dbaas_commands is not None):

            if ("auto" not in self.arguments.inputs):
                Dbaas_operations = DbaaSCrud(
                    alias=self.arguments.args.alias, inputs=self.arguments.inputs)
                if Dbaas_operations.possible:
                    operation = Dbaas_operations.caller(
                        self.arguments.args.dbaas_commands)
                    if operation:
                        operation()

            else:
                dbaas_class_object = DBaaSCrud(
                    alias=self.arguments.args.alias, inputs=self.arguments.inputs)
                if self.arguments.args.dbaas_commands == 'create':
                    dbaas_class_object.create_dbaas()

                elif self.arguments.args.dbaas_commands == 'list' or self.arguments.args.dbaas_commands == 'ls':
                    dbaas_class_object.list_dbaas()

                elif self.arguments.args.dbaas_commands == 'delete':
                    dbaas_class_object.delete_dbaas_by_name()

        elif (self.arguments.args.action is not None):
            DBaas_operations = DBaasAction(
                alias=self.arguments.args.alias, inputs=self.arguments.inputs)
            if DBaas_operations.possible:
                operation = DBaas_operations.caller(
                    self.arguments.args.action)
                if operation:
                    operation()

                else:
                    print("command not found")
                    show_messages.show_parsing_error(parsing_errors)

        else:
            print("command not found")
            show_messages.show_parsing_error(parsing_errors)
