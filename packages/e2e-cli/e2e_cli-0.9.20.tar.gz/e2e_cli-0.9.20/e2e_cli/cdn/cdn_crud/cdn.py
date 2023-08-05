from prettytable import PrettyTable

from e2e_cli.cdn.cdn_crud import helpers
from e2e_cli.cdn.cdn_crud.constants import CDN_LIST_DELETE_URL
from e2e_cli.core.alias_service import get_user_cred
from e2e_cli.core.constants import SUCCESSFULLY_DELETED_MSG, ALIAS, CDN
from e2e_cli.core.helper_service import Checks
from e2e_cli.core.py_manager import PyVersionManager
from e2e_cli.core.request_service import Methods, Request


class CdnCrud:
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        if (get_user_cred(kwargs[ALIAS])):
            self.api_key = get_user_cred(kwargs[ALIAS])[1]
            self.auth_token = get_user_cred(kwargs[ALIAS])[0]
            self.possible = True
        else:
            self.possible = False

    def caller(self, method):
        function_set = {"create": self.create_cdn,
                        "delete": self.delete_cdn,
                        "list": self.list_cdn
                        }
        return function_set.get(method)

    def create_cdn(self):
        print("Currently not integrated")
        # request_payload= {}
        # cdn_name=input("input name of your new cdn : ")
        # while(Checks.cdn_name_validity(cdn_name)):
        #         cdn_name=input("Only following chars are supported: lowercase letters (a-z) or numbers(0-9)  Re-enter : ")

        # api_key=self.api_key
        # auth_token=self.auth_token
        # url =  "api/v1/storage/cdns/"+ cdn_name +"/?apikey="+api_key+"&location=Delhi"
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

    def delete_cdn(self):
        auth_token = self.auth_token
        helpers.cdn_delete_helper(self.kwargs["inputs"])
        request_payload = {}
        query = {}
        query['domain_id'] = self.kwargs["inputs"]["domain_id"]
        url = CDN_LIST_DELETE_URL.format(api_key=self.api_key)
        request_method = Methods.DELETE
        status = Request(url, auth_token, request_payload,
                         request_method, query=query).make_api_call()

        if Checks.status_result(status, request_method):
            print(SUCCESSFULLY_DELETED_MSG.format(service=CDN))
        Checks.show_json(status)

    def list_cdn(self):
        auth_token = self.auth_token
        request_payload = {}
        url = CDN_LIST_DELETE_URL.format(api_key=self.api_key)
        request_method = Methods.GET
        status = Request(url, auth_token, request_payload, request_method).make_api_call()

        Checks.status_result(status)
        Checks.show_json(status)
        # if Checks.status_result(status, request_method):
        #         print("Your cdns : ")
        #         try:
        #             list=status['data']
        #             i=1
        #             x = PrettyTable()
        #             x.field_names = ["index", "ID", "user_domain_name", "Created at", "domain_id"]
        #             for element in list:
        #                 x.add_row([i, element['id'], element['user_domain_name'], element['created_at'], element['domain_id']])
        #                 i = i+1
        #             print(x)
        #         except Exception as e:
        #             print("Errors : ", e)
