import subprocess

from e2e_cli.core import show_messages, constants
from e2e_cli.core.py_manager import PyVersionManager
from e2e_cli.node.node_actions.node_action import NodeActions
from e2e_cli.node.node_crud.node import NodeCrud


class NodeRouting:
    def __init__(self, arguments):
        self.arguments = arguments

    def route(self, parsing_errors):
        if (self.arguments.args.node_commands is None) and (self.arguments.args.action is None):
            show_messages.show_parsing_error(parsing_errors)
            subprocess.call([constants.E2E_CLI, constants.NODE, constants._HELP])

        elif (self.arguments.args.node_commands is not None) and (self.arguments.args.action is not None):
            print("Only one action at a time !!")

        elif (self.arguments.args.node_commands is not None):
            node_operations = NodeCrud(
                alias=self.arguments.args.alias, inputs=self.arguments.inputs)
            if node_operations.possible:
                operation = node_operations.caller(
                    self.arguments.args.node_commands)
                if operation:
                    operation()

        elif (self.arguments.args.action is not None):
            node_operations = NodeActions(
                alias=self.arguments.args.alias, inputs=self.arguments.inputs)
            if node_operations.possible:
                operation = node_operations.caller(
                    self.arguments.args.action)
                if operation:
                    operation()

                else:
                    print("command not found")
                    show_messages.show_parsing_error(parsing_errors)

        else:
            print("command not found")
            show_messages.show_parsing_error(parsing_errors)
