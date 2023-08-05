import json

from prettytable import PrettyTable

from e2e_cli.core.alias_service import get_user_cred
from e2e_cli.core.constants import SUCCESSFULLY_DELETED_MSG, ALIAS, VOLUME
from e2e_cli.core.helper_service import Checks
from e2e_cli.core.py_manager import PyVersionManager
from e2e_cli.core.request_service import Methods, Request
from e2e_cli.volumes.volumes_crud import helpers
from e2e_cli.volumes.volumes_crud.constants import (CREATE_LIST_VOLUMES_URL,
                                                    DELETE_VOLUMES_URL,
                                                    VOLUME_IOPS_URL)


class VolumesCrud:
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        if (get_user_cred(kwargs[ALIAS])):
            self.api_key = get_user_cred(kwargs[ALIAS])[1]
            self.auth_token = get_user_cred(kwargs[ALIAS])[0]
            self.possible = True
        else:
            self.possible = False

    def caller(self, method):
        function_set = {"create": self.create_volumes,
                        "delete": self.delete_volumes,
                        "list": self.list_volumes,
                        "get_plans": self.get_plans
                        }
        return function_set.get(method)

    def create_volumes(self):
        print("Creating")
        auth_token = self.auth_token
        helpers.create_volumes_helper(self.kwargs["inputs"])
        request_payload = json.dumps({
            "name": self.kwargs["inputs"]["name"],
            "size": self.kwargs["inputs"]["size"],
            "iops": self.kwargs["inputs"]["iops"]
        })
        url = CREATE_LIST_VOLUMES_URL.format(api_key=self.api_key)
        request_method = Methods.POST
        status = Request(url, auth_token, request_payload, request_method).make_api_call()

        Checks.status_result(status)
        Checks.show_json(status)
        # if Checks.status_result(status, request_method):
        #     try:
        #         x = PrettyTable()
        #         x.field_names = ["block_storage_id", "name"]
        #         x.add_row([status['data']['block_storage_id'], status['data']['image_name']])
        #         print(x)
        #     except Exception as e:
        #               Checks.show_json(status, e)
        #               return

    def delete_volumes(self):
        auth_token = self.auth_token
        helpers.delete_volumes_helper(self.kwargs["inputs"])
        request_payload = {}
        blockstorage_id = self.kwargs["inputs"]["blockstorage_id"]
        url = DELETE_VOLUMES_URL.format(
            blockstorage_id=blockstorage_id, api_key=self.api_key)
        request_method = Methods.DELETE
        status = Request(url, auth_token, request_payload, request_method).make_api_call()

        if Checks.status_result(status, request_method):
            print(SUCCESSFULLY_DELETED_MSG.format(service=VOLUME))
        Checks.show_json(status)

    def list_volumes(self):
        auth_token = self.auth_token
        request_payload = {}
        url = CREATE_LIST_VOLUMES_URL.format(api_key=self.api_key)
        request_method = Methods.GET
        status = Request(url, auth_token, request_payload, request_method).make_api_call()

        Checks.status_result(status)
        Checks.show_json(status)
        # if Checks.status_result(status, request_method):
        #         print("Your volumess : ")
        #         try:
        #             list=status['data']
        #             i=1
        #             x = PrettyTable()
        #             x.field_names = ["index", "name", "block_id", "status"]
        #             for element in list:
        #                 x.add_row([i, element['name'], element['block_id'], element["status"]])
        #                 i = i+1
        #             print(x)
        #         except Exception as e:
        #             print("Errors : ", e)

    def get_plans(self):
        auth_token = self.auth_token
        request_payload = {}
        url = VOLUME_IOPS_URL.format(api_key=self.api_key)
        request_method = Methods.GET
        status = Request(url, auth_token, request_payload, request_method).make_api_call()
        data = status['data']
        if data:
            x = PrettyTable()
            x.field_names = ["size(GB)", "iops"]
            for element in data:
                x.add_row([float(element['bs_size'])*1000, element['iops']])
            print(x)
