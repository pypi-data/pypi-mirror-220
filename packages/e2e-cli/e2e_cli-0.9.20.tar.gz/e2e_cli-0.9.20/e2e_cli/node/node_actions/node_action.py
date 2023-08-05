import json

from prettytable import PrettyTable

from e2e_cli.core.alias_service import get_user_cred
from e2e_cli.core.constants import ALIAS
from e2e_cli.core.helper_service import Checks
from e2e_cli.core.py_manager import PyVersionManager
from e2e_cli.core.request_service import Request, Methods
from e2e_cli.node.node_actions.constants import (NODE_ACTION_URL,
                                                 NODE_MONITORING_URL, ENABLE_RECOVERY_MODE, DISABLE_RECOVERY_MODE, REBOOT, REINSTALL, RENAME, LOCK_VM, UNLOCK_VM, POWER_OFF, POWER_ON)
from e2e_cli.node.node_actions.helpers import (node_action_helper,
                                               node_rename_helper)


class NodeActions:
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        if (get_user_cred(kwargs[ALIAS])):
            self.api_key = get_user_cred(kwargs[ALIAS])[1]
            self.auth_token = get_user_cred(kwargs[ALIAS])[0]
            self.possible = True
        else:
            self.possible = False

    def caller(self, method):
        function_set = {"enable_recovery": self.enable_recovery,
                        "disable_recovery": self.disable_recovery,
                        "reinstall": self.reinstall,
                        "reboot": self.reboot,
                        "power_on": self.power_on,
                        "power_off": self.power_off,
                        "rename_node": self.rename_node,
                        "lock_vm": self.lock_vm,
                        "unlock_vm": self.unlock_vm,
                        "monitor": self.node_monitoring
                        }
        return function_set.get(method)

    def action_table(self, status, request_method):
        Checks.status_result(status)
        Checks.show_json(status)
        # if Checks.status_result(status, request_method):
        #         try:
        #             x = PrettyTable()
        #             x.field_names = ["Action_type", "Status", "Action ID"]
        #             x.add_row([status['data']['action_type'],
        #                     status['data']['status'], status['data']['id']])
        #             print(x)
        #         except Exception as e:
        #                 print("Errors while reading json ", str(e))
        # if('json' in self.kwargs["inputs"]):
        #     Checks.show_json(status)

    def node_monitoring(self):
        auth_token = self.auth_token
        node_action_helper(self.kwargs["inputs"])
        node_id = self.kwargs["inputs"]["node_id"]
        request_payload = {}
        url = NODE_MONITORING_URL.format(node_id=node_id, api_key=self.api_key)
        request_method = Methods.GET
        status = Request(url, auth_token, request_payload, request_method).make_api_call()

        self.action_table(status, request_method)

    def enable_recovery(self):
        auth_token = self.auth_token
        node_action_helper(self.kwargs["inputs"])
        node_id = self.kwargs["inputs"]["node_id"]
        request_payload = json.dumps({
            "type": ENABLE_RECOVERY_MODE
        })
        url = NODE_ACTION_URL.format(node_id=node_id, api_key=self.api_key)
        request_method = Methods.POST
        status = Request(url, auth_token, request_payload, request_method).make_api_call()

        self.action_table(status, request_method)

    def disable_recovery(self):
        auth_token = self.auth_token
        node_action_helper(self.kwargs["inputs"])
        node_id = self.kwargs["inputs"]["node_id"]
        request_payload = json.dumps({
            "type": DISABLE_RECOVERY_MODE
        })
        auth_token = self.auth_token
        url = NODE_ACTION_URL.format(node_id=node_id, api_key=self.api_key)
        request_method = Methods.POST
        status = Request(url, auth_token, request_payload, request_method).make_api_call()

        self.action_table(status, request_method)

    def reinstall(self):
        auth_token = self.auth_token
        node_action_helper(self.kwargs["inputs"])
        node_id = self.kwargs["inputs"]["node_id"]
        request_payload = json.dumps({
            "type": REINSTALL
        })
        url = NODE_ACTION_URL.format(node_id=node_id, api_key=self.api_key)
        request_method = Methods.POST
        status = Request(url, auth_token, request_payload, request_method).make_api_call()

        self.action_table(status, request_method)

    def reboot(self):
        auth_token = self.auth_token
        node_action_helper(self.kwargs["inputs"])
        node_id = self.kwargs["inputs"]["node_id"]
        request_payload = json.dumps({
            "type": REBOOT
        })
        url = NODE_ACTION_URL.format(node_id=node_id, api_key=self.api_key)
        request_method = Methods.POST
        status = Request(url, auth_token, request_payload, request_method).make_api_call()

        self.action_table(status, request_method)

    def power_on(self):
        auth_token = self.auth_token
        node_action_helper(self.kwargs["inputs"])
        node_id = self.kwargs["inputs"]["node_id"]
        request_payload = json.dumps({
            "type": POWER_ON
        })
        url = NODE_ACTION_URL.format(node_id=node_id, api_key=self.api_key)
        request_method = Methods.POST
        status = Request(url, auth_token, request_payload, request_method).make_api_call()

        self.action_table(status, request_method)

    def power_off(self):
        auth_token = self.auth_token
        node_action_helper(self.kwargs["inputs"])
        node_id = self.kwargs["inputs"]["node_id"]
        request_payload = json.dumps({
            "type": POWER_OFF
        })
        url = NODE_ACTION_URL.format(node_id=node_id, api_key=self.api_key)
        request_method = Methods.POST
        status = Request(url, auth_token, request_payload, request_method).make_api_call()

        self.action_table(status, request_method)

    def rename_node(self):
        auth_token = self.auth_token
        node_rename_helper(self.kwargs["inputs"])
        node_id = self.kwargs["inputs"]["node_id"]
        new_name = self.kwargs["inputs"]["new_name"]
        request_payload = json.dumps({
            "name": new_name,
            "type": RENAME
        })
        url = NODE_ACTION_URL.format(node_id=node_id, api_key=self.api_key)
        request_method = Methods.POST
        status = Request(url, auth_token, request_payload, request_method).make_api_call()

        self.action_table(status, request_method)

    def unlock_vm(self):
        auth_token = self.auth_token
        node_action_helper(self.kwargs["inputs"])
        node_id = self.kwargs["inputs"]["node_id"]
        request_payload = json.dumps({
            "type": UNLOCK_VM
        })
        url = NODE_ACTION_URL.format(node_id=node_id, api_key=self.api_key)
        request_method = Methods.POST
        status = Request(url, auth_token, request_payload, request_method).make_api_call()

        self.action_table(status, request_method)

    def lock_vm(self):
        auth_token = self.auth_token
        node_action_helper(self.kwargs["inputs"])
        node_id = self.kwargs["inputs"]["node_id"]
        request_payload = json.dumps({
            "type": LOCK_VM
        })
        url = NODE_ACTION_URL.format(node_id=node_id, api_key=self.api_key)
        request_method = Methods.POST
        status = Request(url, auth_token, request_payload, request_method).make_api_call()

        self.action_table(status, request_method)
