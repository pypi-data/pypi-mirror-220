from prettytable import PrettyTable

from e2e_cli.bucket_store.bucket_crud.constants import (
    BUCKET_CREATE_DETETE_URL, BUCKET_LIST_URL)
from e2e_cli.bucket_store.bucket_crud.helpers import bucket_crud_helper
from e2e_cli.core.alias_service import get_user_cred
from e2e_cli.core.constants import SUCCESSFULLY_DELETED_MSG, ALIAS, BUCKET
from e2e_cli.core.helper_service import Checks
from e2e_cli.core.py_manager import PyVersionManager
from e2e_cli.core.request_service import Methods, Request


class BucketCrud:
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        if (get_user_cred(kwargs[ALIAS])):
            self.api_key = get_user_cred(kwargs[ALIAS])[1]
            self.auth_token = get_user_cred(kwargs[ALIAS])[0]
            self.possible = True
        else:
            self.possible = False

    def caller(self, method):
        function_set = {"create": self.create_bucket,
                        "delete": self.delete_bucket,
                        "list": self.list_bucket
                        }
        return function_set.get(method)

    def create_bucket(self):
        print("Creating")
        auth_token = self.auth_token
        bucket_crud_helper(self.kwargs["inputs"])
        request_payload = {}
        bucket_name = self.kwargs["inputs"]["bucket_name"]
        url = BUCKET_CREATE_DETETE_URL.format(
            bucket_name=bucket_name, api_key=self.api_key)
        request_method = Methods.POST
        status = Request(url, auth_token, request_payload, request_method).make_api_call()

        Checks.status_result(status)
        Checks.show_json(status)
        # if Checks.status_result(status, request_method):
        #     try:
        #         x = PrettyTable()
        #         x.field_names = ["ID", "Name", "Created at"]
        #         x.add_row([status['data']['id'], status['data']['name'], status['data']['created_at']])
        #         print(x)
        #     except Exception as e:
        #             print("Errors : ", e)

    def delete_bucket(self):
        auth_token = self.auth_token
        bucket_crud_helper(self.kwargs["inputs"])
        request_payload = {}
        bucket_name = self.kwargs["inputs"]["bucket_name"]
        url = BUCKET_CREATE_DETETE_URL.format(
            bucket_name=bucket_name, api_key=self.api_key)
        request_method = Methods.DELETE
        status = Request(url, auth_token, request_payload, request_method).make_api_call()

        if Checks.status_result(status, request_method):
            print(SUCCESSFULLY_DELETED_MSG.format(service=BUCKET))
        Checks.show_json(status)

    def list_bucket(self):
        auth_token = self.auth_token
        request_payload = {}
        url = BUCKET_LIST_URL.format(api_key=self.api_key)
        request_method = Methods.GET
        status = Request(url, auth_token, request_payload, request_method).make_api_call()

        Checks.status_result(status)
        Checks.show_json(status)
        # if Checks.status_result(status, request_method):
        #         print("Your Buckets : ")
        #         try:
        #             list=status['data']
        #             i=1
        #             x = PrettyTable()
        #             x.field_names = ["index", "ID", "Name", "Created at", "bucket size"]
        #             for element in list:
        #                 x.add_row([i, element['id'], element['name'], element['created_at'], element['bucket_size']])
        #                 i = i+1
        #             print(x)
        #         except Exception as e:
        #             print("Errors : ", e)
