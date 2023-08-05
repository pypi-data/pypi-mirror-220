import json

from prettytable import PrettyTable

from e2e_cli.core.alias_service import get_user_cred
from e2e_cli.core.constants import ALIAS
from e2e_cli.core.helper_service import Checks
from e2e_cli.core.py_manager import PyVersionManager
from e2e_cli.core.request_service import Request, Methods
from e2e_cli.dbaas.dbaas_actions import helpers
from e2e_cli.dbaas.dbaas_actions.constants import (ADD_PARAMETER_URL,
                                                   ADD_VPC_URL,
                                                   DISABLE_BACKUP_URL,
                                                   ENABLE_BACKUP_URL,
                                                   REMOVE_PARAMETER_URL,
                                                   REMOVE_VPC_URL,
                                                   RESET_PASSWORD_URL,
                                                   RESTART_DB_URL,
                                                   START_DB_URL, STOP_DB_URL,
                                                   TAKE_SNAPSHOT_URL)


class DBaasAction:
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        if (get_user_cred(kwargs[ALIAS])):
            self.api_key = get_user_cred(kwargs[ALIAS])[1]
            self.auth_token = get_user_cred(kwargs[ALIAS])[0]
            self.possible = True
        else:
            self.possible = False

    def caller(self, method):
        function_set = {"take_snapshot": self.take_snapshot,
                        "reset_password": self.reset_password,
                        "stop_db": self.stop_db,
                        "start_db": self.start_db,
                        "restart_db": self.restart_db,
                        "add_parameter_group": self.add_parameter_group,
                        "remove_parameter_group": self.remove_parameter_group,
                        "add_vpc": self.add_vpc,
                        "remove_vpc": self.remove_vpc,
                        "enable_backup": self.enable_backup,
                        "disable_backup": self.disable_backup
                        }
        return function_set.get(method)

    def take_snapshot(self):
        auth_token = self.auth_token
        helpers.db_common_helper(self.kwargs["inputs"])
        dbaas_id = self.kwargs["inputs"]["dbaas_id"]
        request_payload = json.dumps({
            "name": "sanap3"
        })
        url = TAKE_SNAPSHOT_URL.format(dbaas_id=dbaas_id, api_key=self.api_key)
        request_method = Methods.POST
        status = Request(url, auth_token, request_payload, request_method).make_api_call()

        Checks.status_result(status)
        Checks.show_json(status)

    def reset_password(self):
        auth_token = self.auth_token
        helpers.db_common_helper(self.kwargs["inputs"])
        dbaas_id = self.kwargs["inputs"]["dbaas_id"]
        request_payload = json.dumps({
            "password": self.kwargs["inputs"]["new_password"],
            "username": self.kwargs["inputs"]["username"]
        })
        url = RESET_PASSWORD_URL.format(
            dbaas_id=dbaas_id, api_key=self.api_key)
        request_method = Methods.POST
        status = Request(url, auth_token, request_payload, request_method).make_api_call()

        Checks.status_result(status)
        Checks.show_json(status)

    def stop_db(self):
        auth_token = self.auth_token
        helpers.db_common_helper(self.kwargs["inputs"])
        dbaas_id = self.kwargs["inputs"]["dbaas_id"]
        request_payload = {}
        url = STOP_DB_URL.format(dbaas_id=dbaas_id, api_key=self.api_key)
        request_method = Methods.POST
        status = Request(url, auth_token, request_payload, request_method).make_api_call()

        Checks.status_result(status)
        Checks.show_json(status)

    def start_db(self):
        auth_token = self.auth_token
        helpers.db_common_helper(self.kwargs["inputs"])
        dbaas_id = self.kwargs["inputs"]["dbaas_id"]
        request_payload = {}
        url = START_DB_URL.format(dbaas_id=dbaas_id, api_key=self.api_key)
        request_method = Methods.POST
        status = Request(url, auth_token, request_payload, request_method).make_api_call()

        Checks.status_result(status)
        Checks.show_json(status)

    def restart_db(self):
        auth_token = self.auth_token
        helpers.db_common_helper(self.kwargs["inputs"])
        dbaas_id = self.kwargs["inputs"]["dbaas_id"]
        request_payload = {}
        url = RESTART_DB_URL.format(dbaas_id=dbaas_id, api_key=self.api_key)
        request_method = Methods.POST
        status = Request(url, auth_token, request_payload, request_method).make_api_call()

        Checks.status_result(status)
        Checks.show_json(status)

    def add_parameter_group(self):
        auth_token = self.auth_token
        helpers.db_add_rempove_paramter(self.kwargs["inputs"])
        dbaas_id = self.kwargs["inputs"]["dbaas_id"]
        parameter_group_id = self.kwargs["inputs"]["parameter_group_id"]
        request_payload = {}
        url = ADD_PARAMETER_URL.format(
            dbaas_id=dbaas_id, parameter_group_id=parameter_group_id, api_key=self.api_key)
        request_method = Methods.POST
        status = Request(url, auth_token, request_payload, request_method).make_api_call()

        Checks.status_result(status)
        Checks.show_json(status)

    def remove_parameter_group(self):
        auth_token = self.auth_token
        helpers.db_add_rempove_paramter(self.kwargs["inputs"])
        dbaas_id = self.kwargs["inputs"]["dbaas_id"]
        parameter_group_id = self.kwargs["inputs"]["parameter_group_id"]
        request_payload = {}
        url = REMOVE_PARAMETER_URL.format(
            dbaas_id=dbaas_id, parameter_group_id=parameter_group_id, api_key=self.api_key)
        request_method = Methods.POST
        status = Request(url, auth_token, request_payload, request_method).make_api_call()

        Checks.status_result(status)
        Checks.show_json(status)

    def add_vpc(self):
        auth_token = self.auth_token
        helpers.db_add_rempove_vpc(self.kwargs["inputs"])
        dbaas_id = self.kwargs["inputs"]["dbaas_id"]
        request_payload = json.dumps({
            "action": "attach",
            "network_id": self.kwargs["inputs"]["network_id"]
        })
        url = ADD_VPC_URL.format(dbaas_id=dbaas_id, api_key=self.api_key)
        request_method = Methods.POST
        status = Request(url, auth_token, request_payload, request_method).make_api_call()

        Checks.status_result(status)
        Checks.show_json(status)

    def remove_vpc(self):
        auth_token = self.auth_token
        helpers.db_add_rempove_vpc(self.kwargs["inputs"])
        dbaas_id = self.kwargs["inputs"]["dbaas_id"]
        request_payload = json.dumps({
            "action": "detach",
            "network_id": self.kwargs["inputs"]["network_id"]
        })
        url = REMOVE_VPC_URL.format(dbaas_id=dbaas_id, api_key=self.api_key)
        request_method = Methods.POST
        status = Request(url, auth_token, request_payload, request_method).make_api_call()

        Checks.status_result(status)
        Checks.show_json(status)

    def enable_backup(self):
        auth_token = self.auth_token
        helpers.db_enable_backup(self.kwargs["inputs"])
        dbaas_id = self.kwargs["inputs"]["dbaas_id"]
        request_payload = json.dumps({
            "access_key": self.kwargs["inputs"]["access_key"],
            "bucket_location": self.kwargs["inputs"]["bucket_location"],
            "secret_key": self.kwargs["inputs"]["secret_key"]
        })
        url = ENABLE_BACKUP_URL.format(dbaas_id=dbaas_id, api_key=self.api_key)
        request_method = Methods.POST
        status = Request(url, auth_token, request_payload, request_method).make_api_call()

        Checks.status_result(status)
        Checks.show_json(status)

    def disable_backup(self):
        auth_token = self.auth_token
        helpers.db_common_helper(self.kwargs["inputs"])
        dbaas_id = self.kwargs["inputs"]["dbaas_id"]
        request_payload = {}
        url = DISABLE_BACKUP_URL.format(
            dbaas_id=dbaas_id, api_key=self.api_key)
        request_method = Methods.POST
        status = Request(url, auth_token, request_payload, request_method).make_api_call()

        Checks.status_result(status)
        Checks.show_json(status)
