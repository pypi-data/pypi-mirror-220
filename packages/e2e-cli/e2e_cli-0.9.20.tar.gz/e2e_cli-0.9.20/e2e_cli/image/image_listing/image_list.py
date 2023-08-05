from prettytable import PrettyTable
import json

from e2e_cli.core.py_manager import PyVersionManager
from e2e_cli.core.request_service import Request, Methods
from e2e_cli.core.alias_service import get_user_cred
from e2e_cli.core.helper_service import Checks
from e2e_cli.core.constants import ALIAS 


class ImageListing:
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        if (get_user_cred(kwargs[ALIAS])):
            self.api_key = get_user_cred(kwargs[ALIAS])[1]
            self.auth_token = get_user_cred(kwargs[ALIAS])[0]
            self.possible = True
        else:
            self.possible = False

    def image_type(self):
        request_payload = {}
        api_key = self.api_key
        auth_token = self.auth_token
        url = "api/v1/images/?apikey="+api_key+"&image_type=private"
        request_method = Methods.GET
        status = Request(url, auth_token, request_payload, request_method).make_api_call()

        print(status)

        query = {}

        cpu = input("number of CPU ")
        ram = input("capacity of RAM in GB ")
        series = input("input the Series ")
        OS = input("input the OS ")
        Version = input("input the OS Version ")
