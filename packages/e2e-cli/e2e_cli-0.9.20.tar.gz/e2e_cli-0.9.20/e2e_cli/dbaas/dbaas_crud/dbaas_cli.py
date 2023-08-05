import json

from prettytable import PrettyTable

from e2e_cli.core.alias_service import get_user_cred
from e2e_cli.core.constants import (CLI_E2E, CONFIRMATION_MSG,
                                    SUCCESSFULLY_DELETED_MSG, ALIAS, DBAAS, YES)
from e2e_cli.core.helper_service import Checks
from e2e_cli.core.py_manager import PyVersionManager
from e2e_cli.core.request_service import Methods, Request
from e2e_cli.dbaas.dbaas_crud.constants import (CREATE_LIST_DBAAS_URL,
                                                DELETE_DBAAS_URL)
from e2e_cli.dbaas.dbaas_crud.helpers import (dbaas_create_helper,
                                              dbaas_delete_helper)


class DbaaSCrud:
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        if (get_user_cred(kwargs[ALIAS])):
            self.api_key = get_user_cred(kwargs[ALIAS])[1]
            self.auth_token = get_user_cred(kwargs[ALIAS])[0]
            self.possible = True
        else:
            self.possible = False

    def caller(self, method):
        function_set = {"create": self.create_dbaas,
                        "delete": self.delete_dbaas,
                        "list": self.list_dbaas
                        }
        return function_set.get(method)

    def create_dbaas(self):
        print("Creating")
        auth_token = self.auth_token
        dbaas_create_helper(self.kwargs["inputs"])
        request_payload = {
            "name": self.kwargs["inputs"]["name"],
            # ex- DBS.8GB, DBS.16GB
            "plan_name": self.kwargs["inputs"]["plan_name"],
            # ex- mysql, postgresql, mariadb
            "db":  self.kwargs["inputs"]["db"],
            # ex- 8, 11, 5.6
            "db_version": self.kwargs["inputs"]["db_version"],
            "group": "Default",
            "database": {
                "name": self.kwargs["inputs"]["name"],
                "user": self.kwargs["inputs"]["user"],
                "password": self.kwargs["inputs"]["password"]
            }
        }
        url = CREATE_LIST_DBAAS_URL.format(api_key=self.api_key)
        request_method = Methods.POST
        user_agent = CLI_E2E

        status = Request(url, auth_token, json.dumps(request_payload),
                         request_method, user_agent).make_api_call()

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

    def delete_dbaas(self):
        request_payload = {}
        auth_token = self.auth_token
        dbaas_delete_helper(self.kwargs["inputs"])
        dbaas_id = self.kwargs["inputs"]["dbaas_id"]
        url = DELETE_DBAAS_URL.format(dbaas_id=dbaas_id, api_key=self.api_key)
        request_method = Methods.DELETE

        confirmation = input(CONFIRMATION_MSG)
        if (confirmation.lower() == YES):
            status = Request(url, auth_token, request_payload, request_method).make_api_call()
            if Checks.status_result(status, request_method):
                print(SUCCESSFULLY_DELETED_MSG.format(service=DBAAS))

        Checks.show_json(status)

    def list_dbaas(self, parameter=0):
        request_payload = {}
        auth_token = self.auth_token
        url = CREATE_LIST_DBAAS_URL.format(api_key=self.api_key)
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
            # Checks.status_result(status)
            Checks.show_json(status)

        elif parameter == 1:
            return status['data']
