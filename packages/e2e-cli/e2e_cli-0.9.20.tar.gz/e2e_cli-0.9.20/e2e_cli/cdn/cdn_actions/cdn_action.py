import json

from prettytable import PrettyTable

from e2e_cli.cdn.cdn_actions import helpers
from e2e_cli.cdn.cdn_actions.constants import (CDN_BANDWIDTH_USAGE_URL,
                                               CDN_MONITORING_URL,
                                               ENABLE_DISABLE_CDN_URL)
from e2e_cli.core.alias_service import get_user_cred
from e2e_cli.core.constants import ALIAS
from e2e_cli.core.helper_service import Checks
from e2e_cli.core.py_manager import PyVersionManager
from e2e_cli.core.request_service import Request, Methods


class CdnActions:
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        if (get_user_cred(kwargs[ALIAS])):
            self.api_key = get_user_cred(kwargs[ALIAS])[1]
            self.auth_token = get_user_cred(kwargs[ALIAS])[0]
            self.possible = True
        else:
            self.possible = False

    def caller(self, method):
        function_set = {"enable_cdn": self.enable_cdn,
                        "disable_cdn": self.disable_cdn,
                        "list": self.cdn_monitoring,
                        "cdn_bandwidth_usage": self.cdn_bandwidth_usage
                        }
        return function_set.get(method)

    def cdn_monitoring(self):
        auth_token = self.auth_token
        helpers.cdn_monitoring_helper()
        request_payload = {}
        query = {}
        query['start_date'] = self.kwargs["inputs"]["start_date"]
        query['end_date'] = self.kwargs["inputs"]["end_date"]
        query['distribution_id'] = self.kwargs["inputs"]["distribution_id"]
        query['granularity'] = self.kwargs["inputs"]["granularity"]
        url = CDN_MONITORING_URL.format(api_key=self.api_key)
        request_method = Methods.GET
        status = Request(url, auth_token, request_payload,
                         request_method, query=query).make_api_call()

        Checks.status_result(status)
        Checks.show_json(status)

    def enable_cdn(self):
        auth_token = self.auth_token
        helpers.enable_disable_cdn_helper(self.kwargs["inputs"])
        request_payload = json.dumps({
            "domain_id": self.kwargs["inputs"]["domain_id"],
            "is_enabled": True
        })
        url = ENABLE_DISABLE_CDN_URL.format(api_key=self.api_key)
        request_method = Methods.PUT
        status = Request(url, auth_token, request_payload, request_method).make_api_call()

        Checks.status_result(status)
        Checks.show_json(status)

    def disable_cdn(self):
        auth_token = self.auth_token
        helpers.enable_disable_cdn_helper(self.kwargs["inputs"])
        request_payload = json.dumps({
            "domain_id": self.kwargs["inputs"]["domain_id"],
            "is_enabled": False
        })
        url = ENABLE_DISABLE_CDN_URL.format(api_key=self.api_key)
        request_method = Methods.PUT
        status = Request(url, auth_token, request_payload, request_method).make_api_call()

        Checks.status_result(status)
        Checks.show_json(status)

    def cdn_bandwidth_usage(self):
        auth_token = self.auth_token
        helpers.cdn_bandwidth_usage_helper(self.kwargs["inputs"])
        request_payload = json.dumps({
            'domain': "all",
            'start_date': self.kwargs["inputs"]["start_date"],
            'end_date': self.kwargs["inputs"]["end_date"],
            'granularity': self.kwargs["inputs"]["granularity"]
        })
        url = CDN_BANDWIDTH_USAGE_URL.format(api_key=self.api_key)
        request_method = Methods.POST
        status = Request(url, auth_token, request_payload, request_method).make_api_call()

        Checks.status_result(status)
        Checks.show_json(status)
