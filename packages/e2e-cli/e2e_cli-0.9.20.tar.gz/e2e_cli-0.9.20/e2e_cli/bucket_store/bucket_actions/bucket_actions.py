import json

from prettytable import PrettyTable

from e2e_cli.bucket_store.bucket_actions import helpers
from e2e_cli.bucket_store.bucket_actions.constants import (
    BUCKET_ADD_PERMISSION_URL, BUCKET_KEY_URL, BUCKET_LIST_KEY_URL,
    BUCKET_REMOVE_PERMISSION_URL, BUCKET_VERSIONING_URL)
from e2e_cli.core.alias_service import get_user_cred
from e2e_cli.core.constants import ALIAS
from e2e_cli.core.helper_service import Checks
from e2e_cli.core.py_manager import PyVersionManager
from e2e_cli.core.request_service import Request, Methods


class BucketActions:
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        if (get_user_cred(kwargs[ALIAS])):
            self.api_key = get_user_cred(kwargs[ALIAS])[1]
            self.auth_token = get_user_cred(kwargs[ALIAS])[0]
            self.possible = True
        else:
            self.possible = False

    def caller(self, method):
        function_set = {"enable_versioning": self.enable_versioning,
                        "disable_versioning": self.disable_versioning,
                        "create_key": self.create_key,
                        "delete_key": self.delete_key,
                        "list_key": self.list_key,
                        "lock_key": self.lock_key,
                        "unlock_key": self.unlock_key,
                        "add_permission": self.add_permission
                        }
        return function_set.get(method)

    def enable_versioning(self):
        auth_token = self.auth_token
        helpers.bucket_versioning_helper(self.kwargs["inputs"])
        bucket_name = self.kwargs["inputs"]["bucket_name"]
        request_payload = json.dumps({
            "bucket_name": bucket_name,
            "new_versioning_state": "Enabled"
        })
        url = BUCKET_VERSIONING_URL.format(
            bucket_name=bucket_name, api_key=self.api_key)
        request_method = Methods.POST
        status = Request(url, auth_token, request_payload, request_method).make_api_call()

        Checks.status_result(status)
        Checks.show_json(status)

    def disable_versioning(self):
        auth_token = self.auth_token
        helpers.bucket_versioning_helper(self.kwargs["inputs"])
        bucket_name = self.kwargs["inputs"]["bucket_name"]
        request_payload = json.dumps({
            "bucket_name": bucket_name,
            "new_versioning_state": "Disabled"
        })
        url = BUCKET_VERSIONING_URL.format(
            bucket_name=bucket_name, api_key=self.api_key)
        request_method = Methods.POST
        status = Request(url, auth_token, request_payload, request_method).make_api_call()

        Checks.status_result(status)
        Checks.show_json(status)

    def create_key(self):
        auth_token = self.auth_token
        helpers.bucket_create_key(self.kwargs["inputs"])
        key_name = self.kwargs["inputs"]["key_name"]
        request_payload = json.dumps({
            "tag": key_name
        })
        url = BUCKET_KEY_URL.format(api_key=self.api_key)
        request_method = Methods.POST
        status = Request(url, auth_token, request_payload, request_method).make_api_call()

        if Checks.status_result(status):
            print("Key Created successfully")

        Checks.show_json(status)

    def delete_key(self):
        auth_token = self.auth_token
        helpers.bucket_delete_key(self.kwargs["inputs"])
        access_key = self.kwargs["inputs"]["access_key"]
        request_payload = {}
        query = {}
        query['access_key'] = access_key
        url = BUCKET_KEY_URL.format(api_key=self.api_key)
        request_method = Methods.DELETE
        status = Request(url, auth_token, request_payload,
                         request_method, query=query).make_api_call()

        if Checks.status_result(status):
            print("Key deleted successfully")

        Checks.show_json(status)

    def list_key(self):
        auth_token = self.auth_token
        request_payload = {}
        url = BUCKET_LIST_KEY_URL.format(api_key=self.api_key)
        request_method = Methods.GET
        status = Request(url, auth_token, request_payload, request_method).make_api_call()

        # if Checks.status_result(status, request_method):
        #         print("Your Keys : ")
        #         try:
        #             list=status['data']
        #             i=1
        #             x = PrettyTable()
        #             x.field_names = ["index", "ID", "Name", "access_key" ]
        #             for element in list:
        #                 x.add_row([i, element['id'], element['tag'], element['access_key']])
        #                 i = i+1
        #             print(x)
        #         except Exception as e:
        #               Checks.show_json(status, e)
        #               return
        Checks.status_result(status)
        Checks.show_json(status)

    def lock_key(self):
        auth_token = self.auth_token
        helpers.bucket_lock_unlock_key(self.kwargs["inputs"])
        key_id = self.kwargs["inputs"]["key_id"]
        request_payload = json.dumps({
            "disabled": True,
            "id": key_id
        })
        url = BUCKET_KEY_URL.format(api_key=self.api_key)
        request_method = Methods.PUT
        status = Request(url, auth_token, request_payload, request_method).make_api_call()

        if Checks.status_result(status):
            print("Key locked")
        Checks.show_json(status)

    def unlock_key(self):
        auth_token = self.auth_token
        helpers.bucket_lock_unlock_key(self.kwargs["inputs"])
        key_id = self.kwargs["inputs"]["key_id"]
        request_payload = json.dumps({
            "disabled": False,
            "id": key_id
        })
        url = BUCKET_KEY_URL.format(api_key=self.api_key)
        request_method = Methods.PUT
        status = Request(url, auth_token, request_payload, request_method).make_api_call()

        if Checks.status_result(status):
            print("Key unlocked")
        Checks.show_json(status)

    def add_permission(self):
        auth_token = self.auth_token
        bucket_name = self.kwargs["inputs"]["bucket_name"]
        request_payload = json.dumps({
            "role_name": "Bucket Admin",
            "users": [
                {
                    "access_key": input("input access key (Alphanumeric): "),
                    "disabled": False,
                    "email": "",
                    "id": input("enter bucket id "),
                    "is_default": False,
                    "my_account_id": None,
                    "secret_key": None,
                    "tag": input("name "),
                    "user_name": input("username ")
                }
            ]
        })
        query = {}
        query['bucket_name'] = bucket_name
        url = BUCKET_ADD_PERMISSION_URL.format(api_key=self.api_key)
        request_method = Methods.PUT
        status = Request(url, auth_token, request_payload,
                         request_method, query=query).make_api_call()

        if Checks.status_result(status):
            print("Premission added successfully")
        Checks.show_json(status)

    def remove_permission(self):
        auth_token = self.auth_token
        helpers.bucket_remove_permission(self.kwargs["inputs"])
        bucket_name = self.kwargs["inputs"]["bucket_name"]
        bucket_permission_id = self.kwargs["inputs"]["bucket_permission_id"]
        request_payload = {}
        query = {}
        query['access_key'] = bucket_name
        url = BUCKET_REMOVE_PERMISSION_URL.format(
            bucket_permission_id=bucket_permission_id, api_key=self.api_key)
        request_method = Methods.DELETE
        status = Request(url, auth_token, request_payload,
                         request_method, query=query).make_api_call()

        if Checks.status_result(status):
            print("Premission removed")
        Checks.show_json(status)
