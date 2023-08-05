import json

from prettytable import PrettyTable

from e2e_cli.core.alias_service import get_user_cred
from e2e_cli.core.constants import (CLI_E2E, CLI_PYTHON, CONFIRMATION_MSG,
                                    SUCCESSFULLY_DELETED_MSG, ALIAS, NODE, YES)
from e2e_cli.core.helper_service import Checks
from e2e_cli.core.py_manager import PyVersionManager
from e2e_cli.core.request_service import Methods, Request
from e2e_cli.node.node_crud.constants import CREATE_LIST_URL, DELETE_GET_URL
from e2e_cli.node.node_crud.helpers import (node_create_helper,
                                            node_delete_helper,
                                            node_get_helper)


class NodeCrud:
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        if (get_user_cred(kwargs[ALIAS])):
            self.api_key = get_user_cred(kwargs[ALIAS])[1]
            self.auth_token = get_user_cred(kwargs[ALIAS])[0]
            self.possible = True
        else:
            self.possible = False

    def caller(self, method):
        function_set = {"create": self.create_node,
                        "delete": self.delete_node,
                        "get": self.get_node_by_id,
                        "list": self.list_node
                        }
        return function_set.get(method)

    def create_node(self):
        print("Creating")
        request_payload = node_create_helper(self.kwargs)
        auth_token = self.auth_token
        url = CREATE_LIST_URL.format(api_key=self.api_key)
        request_method = Methods.POST
        user_agent = CLI_PYTHON if ('auto' in self.kwargs["inputs"]) else CLI_E2E

        status = Request(url, auth_token, json.dumps(
            request_payload), request_method, user_agent).make_api_call()

        # if Checks.status_result(status,request_method):
        #     try :
        #         x = PrettyTable()
        #         x.field_names = ["ID", "Name", "Created at", "disk", "Status", "Plan"]
        #         x.add_row([status['data']['id'], status['data']['name'],
        #               status['data']['created_at'], status['data']['disk'], status['data']['status'], status['data']['plan']])
        #         print(x)
        #     except Exception as e:
        #             print("Errors : ", e)
        Checks.status_result(status)
        Checks.show_json(status)

    def delete_node(self):
        request_payload = {}
        auth_token = self.auth_token
        node_delete_helper(self.kwargs["inputs"])
        node_id = self.kwargs["inputs"]["node_id"]
        url = DELETE_GET_URL.format(node_id=node_id, api_key=self.api_key)
        request_method = Methods.DELETE

        confirmation = input(CONFIRMATION_MSG)
        if (confirmation.lower() == YES):
            status = Request(url, auth_token, request_payload, request_method).make_api_call()
            if Checks.status_result(status, request_method):
                print(SUCCESSFULLY_DELETED_MSG.format(service=NODE))
        Checks.show_json(status)

    def get_node_by_id(self):
        request_payload = {}
        auth_token = self.auth_token
        node_get_helper(self.kwargs["inputs"])
        node_id = self.kwargs["inputs"]["node_id"]
        url = DELETE_GET_URL.format(node_id=node_id, api_key=self.api_key)
        request_method = Methods.GET
        status = Request(url, auth_token, request_payload, request_method).make_api_call()

        # if Checks.status_result(status, request_method):
        #     try:
        #         x = PrettyTable()
        #         x.field_names = ["VM id", "Name", "Created at", "disk", "Plan", "Public IP", "Status"]
        #         x.add_row([ status['data']['vm_id'], status['data']['name'], status['data']['created_at'], status['data']['disk'],  status['data']['plan'], status['data']['public_ip_address'], status['data']['status'] ])
        #         print(x)
        #     except Exception as e:
        #                 print("Errors : ", e)
        Checks.status_result(status)
        Checks.show_json(status)

    def list_node(self, parameter=0):
        request_payload = {}
        auth_token = self.auth_token
        url = CREATE_LIST_URL.format(api_key=self.api_key)
        request_method = Methods.GET
        status = Request(url, auth_token, request_payload,
                         request_method).make_api_call()

        if parameter == 0:
            # if Checks.status_result(status, request_method):
            #     list=status['data']
            #     try:
            #         i = 1
            #         x = PrettyTable()
            #         x.field_names = ["index", "ID", "Name", "Plan", "Status"]
            #         for element in list:
            #             x.add_row([i, element['id'], element['name'],
            #                       element['plan'],  element['status']])
            #             i = i+1
            #         print(x)
            #     except Exception as e:
            #             print("Errors : ", e)
            Checks.status_result(status)
            Checks.show_json(status)

        elif parameter == 1:
            return status['data']

    def update_node(self):
        auth_token = self.auth_token
        print("update call")
