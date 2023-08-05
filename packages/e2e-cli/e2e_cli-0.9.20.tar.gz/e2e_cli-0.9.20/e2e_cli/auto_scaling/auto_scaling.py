from prettytable import PrettyTable

from e2e_cli.auto_scaling.constants import (DELETE_AUTOSCALING_URL,
                                            LIST_AUTOSCALING_URL)
from e2e_cli.auto_scaling.helpers import autoscaling_crud_helper
from e2e_cli.core.alias_service import get_user_cred
from e2e_cli.core.constants import SUCCESSFULLY_DELETED_MSG, ALIAS, AUTOSCALING
from e2e_cli.core.helper_service import Checks
from e2e_cli.core.py_manager import PyVersionManager
from e2e_cli.core.request_service import Methods, Request


class AutoscalingCrud:
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        if (get_user_cred(kwargs[ALIAS])):
            self.api_key = get_user_cred(kwargs[ALIAS])[1]
            self.auth_token = get_user_cred(kwargs[ALIAS])[0]
            self.possible = True
        else:
            self.possible = False

    def caller(self, method):
        function_set = {"create": self.create_autoscaling,
                        "delete": self.delete_autoscaling,
                        "list": self.list_autoscaling
                        }
        return function_set.get(method)

    def create_autoscaling(self):
        print("Currently not integrated")
        # request_payload= {}
        # autoscaling_name=input("input name of your new autoscaling : ")
        # while(Checks.autoscaling_name_validity(autoscaling_name)):
        #         autoscaling_name=input("Only following chars are supported: lowercase letters (a-z) or numbers(0-9)  Re-enter : ")

        # api_key=self.api_key
        # auth_token=self.auth_token
        # url =  "api/v1/storage/autoscalings/"+ autoscaling_name +"/?apikey="+api_key+"&location=Delhi"
        # request_method=Methods.POST
        # status=Request(url, auth_token, request_payload, request_method).make_api_call()

        # if Checks.status_result(status, request_method):
        #     try:
        #         x = PrettyTable()
        #         x.field_names = ["ID", "Name", "Created at"]
        #         x.add_row([status['data']['id'], status['data']['name'], status['data']['created_at']])
        #         print(x)
        #     except Exception as e:
        #               Checks.show_json(status, e)
        #               return

        # Checks.show_json(status)

    def delete_autoscaling(self):
        auth_token = self.auth_token
        autoscaling_crud_helper(self.kwargs["inputs"])
        request_payload = {}
        autoscaling_id = self.kwargs["inputs"]["autoscaling_id"]
        url = DELETE_AUTOSCALING_URL.format(
            autoscaling_id=autoscaling_id, api_key=self.api_key)
        request_method = Methods.DELETE
        status = Request(url, auth_token, request_payload, request_method).make_api_call()

        Checks.show_json(status)
        print(SUCCESSFULLY_DELETED_MSG.format(service=AUTOSCALING))
        # if Checks.status_result(status,request_method):
        #                 print(SUCCESSFULLY_DELETED_MSG.format(service=constants.AUTOSCALING))

    def list_autoscaling(self):
        auth_token = self.auth_token
        request_payload = {}
        url = LIST_AUTOSCALING_URL.format(api_key=self.api_key)
        request_method = Methods.GET
        status = Request(url, auth_token, request_payload, request_method).make_api_call()

        Checks.status_result(status)
        Checks.show_json(status)
        # if Checks.status_result(status, request_method):
        #         print("Your autoscalings : ")
        #         try:
        #             list=status['data']
        #             i=1
        #             x = PrettyTable()
        #             x.field_names = ["index", "ID", "Policy", "Name", "Max_nodes", "Min_nodes"]
        #             for element in list:
        #                 x.add_row([i, element['id'], element['policy'], element['name'], element['max_nodes'], element["min_nodes"]])
        #                 i = i+1
        #             print(x)
        #         except Exception as e:
        #               print("Errors : ", e)
