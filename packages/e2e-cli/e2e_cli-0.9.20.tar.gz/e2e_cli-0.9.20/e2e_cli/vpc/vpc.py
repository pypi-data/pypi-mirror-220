import json

from prettytable import PrettyTable

from e2e_cli.core.alias_service import get_user_cred
from e2e_cli.core.constants import SUCCESSFULLY_DELETED_MSG, ALIAS, VPC
from e2e_cli.core.helper_service import Checks
from e2e_cli.core.py_manager import PyVersionManager
from e2e_cli.core.request_service import Methods, Request
from e2e_cli.vpc import helpers
from e2e_cli.vpc.constants import CREATE_VPC_URL, DELETE_VPC_URL, LIST_VPC_URL


class VpcCrud:
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        if (get_user_cred(kwargs[ALIAS])):
            self.api_key = get_user_cred(kwargs[ALIAS])[1]
            self.auth_token = get_user_cred(kwargs[ALIAS])[0]
            self.possible = True
        else:
            self.possible = False

    def caller(self, method):
        function_set = {"create": self.create_vpc,
                        "delete": self.delete_vpc,
                        "list": self.list_vpc,
                        }
        return function_set.get(method)

    def create_vpc(self):
        print("Creating")
        auth_token = self.auth_token
        helpers.create_vpc_helper(self.kwargs["inputs"])
        request_payload = json.dumps({
            "network_size": 512,
            "vpc_name": self.kwargs["inputs"]["vpc_name"]
        })
        url = CREATE_VPC_URL.format(api_key=self.api_key)
        request_method = Methods.POST
        status = Request(url, auth_token, request_payload, request_method).make_api_call()

        Checks.show_json(status)
        # if Checks.status_result(status, request_method):
        #     try:
        #         x = PrettyTable()
        #         x.field_names = ["ID", "Name"]
        #         x.add_row([status['data']['vpc_id'], status['data']['name'] ])
        #         print(x)
        #     except Exception as e:
        #               print("Errors : ", e)

    def delete_vpc(self):
        auth_token = self.auth_token
        request_payload = {}
        helpers.delete_vpc_helper(self.kwargs["inputs"])
        network_id = self.kwargs["inputs"]["network_id"]
        url = DELETE_VPC_URL.format(
            network_id=network_id, api_key=self.api_key)
        request_method = Methods.DELETE
        status = Request(url, auth_token, request_payload, request_method).make_api_call()

        if Checks.status_result(status, request_method):
            print(SUCCESSFULLY_DELETED_MSG.format(service=VPC))

        Checks.show_json(status)

    def list_vpc(self):
        request_payload = {}
        auth_token = self.auth_token
        url = LIST_VPC_URL.format(api_key=self.api_key)
        request_method = Methods.GET
        status = Request(url, auth_token, request_payload, request_method).make_api_call()

        Checks.show_json(status)
        # if Checks.status_result(status, request_method):
        #         print("Your vpcs : ")
        #         try:
        #             list=status['data']
        #             i=1
        #             x = PrettyTable()
        #             x.field_names = ["index", "network_id", "Name", "network_mask", "gateway_ip", "pool_size"]
        #             for element in list:
        #                 x.add_row([i, element['network_id'], element['name'], element['network_mask'], element["gateway_ip"], element["pool_size"]])
        #                 i = i+1
        #             print(x)
        #         except Exception as e:
        #               print("Errors : ", e)
