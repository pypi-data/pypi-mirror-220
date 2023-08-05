from prettytable import PrettyTable
import json

from e2e_cli.core.py_manager import PyVersionManager
from e2e_cli.core.request_service import Request, Methods
from e2e_cli.core.alias_service import get_user_cred
from e2e_cli.core.helper_service import Checks
from e2e_cli.core.constants import ALIAS


class VolumesActions:
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        if (get_user_cred(kwargs[ALIAS])):
            self.api_key = get_user_cred(kwargs[ALIAS])[1]
            self.auth_token = get_user_cred(kwargs[ALIAS])[0]
            self.possible = True
        else:
            self.possible = False

    def attach_volume(self):
        request_payload = json.dumps({
            "vm_id": input("enter vm id of node you want to attach volume ")
        })
        blockstorage_id = input(
            "input blockstorage_id of the volumes you want to attach : ")
        api_key = self.api_key
        auth_token = self.auth_token
        url = "api/v1/block_storage/"+blockstorage_id + \
            "/vm/attach/?apikey="+api_key+"&location=Delhi"
        request_method = Methods.POST
        status = Request(url, auth_token, request_payload, request_method).make_api_call().text

        Checks.show_json(status)

    def detach_volume(self):
        request_payload = json.dumps({
            "vm_id": input("enter vm id of node you want to attach volume ")
        })
        blockstorage_id = input(
            "input blockstorage_id of the volumes you want to detach : ")
        api_key = self.api_key
        auth_token = self.auth_token
        url = "api/v1/block_storage/"+blockstorage_id + \
            "/vm/detach/?apikey="+api_key+"&location=Delhi"
        request_method = Methods.POST
        status = Request(url, auth_token, request_payload, request_method).make_api_call().text

        Checks.show_json(status)
