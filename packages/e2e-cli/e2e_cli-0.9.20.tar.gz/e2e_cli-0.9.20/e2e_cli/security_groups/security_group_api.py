import json

from prettytable import PrettyTable

from e2e_cli.core.alias_service import get_user_cred
from e2e_cli.core.constants import ALIAS
from e2e_cli.core.py_manager import PyVersionManager
from e2e_cli.core.request_service import Methods, Request


class SecurityGroup:
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        if (get_user_cred(kwargs[ALIAS])):
            self.api_key = get_user_cred(kwargs[ALIAS])[1]
            self.auth_token = get_user_cred(kwargs[ALIAS])[0]
            self.possible = True
        else:
            self.possible = False

    def caller(self, method):
        function_set = {"list": self.list_security_groups,
                        }
        return function_set.get(method)

    def list_security_groups(self):
        request_payload = ""
        api_key = self.api_key
        auth_token = self.auth_token
        url = "api/v1/security_group/?apikey="+api_key
        request_method = Methods.GET
        status = Request(url, auth_token, request_payload, request_method).make_api_call()
        data = status['data']
        if (data):
            x = PrettyTable()
            x.field_names = ["security_group_id", "Name", "description"]
            x.add_row([data[0]['id'], data[0]['name'], data[0]['description']])
        print(x)
