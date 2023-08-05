from prettytable import PrettyTable

from e2e_cli.core.alias_service import get_user_cred
from e2e_cli.core.constants import CLI_PYTHON
from e2e_cli.core.py_manager import PyVersionManager
from e2e_cli.core.request_service import Request, Methods
from e2e_cli.node.node_crud.constants import NODE_PLAN_LIST_URL, NODE_TYPE_URL


class Nodelisting:
    def __init__(self, alias):
        if (get_user_cred(alias)):
            self.api_key = get_user_cred(alias)[1]
            self.auth_token = get_user_cred(alias)[0]

    def node_listing(self):
        url = NODE_TYPE_URL.format(api_key=self.api_key)
        request_method = Methods.GET
        request_payload = {}
        response = Request(url, self.auth_token, request_payload,
                           request_method, user_agent=CLI_PYTHON).make_api_call()['data']

        i = 1
        x = PrettyTable()
        x.field_names = ["ID", 'Types of node']
        category = {}
        for key in response['category_list']:
            x.add_row([i, key])
            category[str(i)] = key
            i = i+1
        print(x)
        node_type = input("Select one of above id : ")
        while (not node_type in category):
            node_type = input("Select one of above id : ")
        node_type = category[node_type]

        i = 1
        x = PrettyTable()
        x.field_names = ["ID", 'Types of OS']
        os_type_list = {}
        for key in response['category_list'][node_type]:
            x.add_row([i, key])
            os_type_list[str(i)] = key
            i = i+1
        print(x)
        os_type = input("Select one of above id : ")
        while (not os_type in os_type_list):
            os_type = input("Select one of above id : ")
        os_type = os_type_list[os_type]

        i = 1
        x = PrettyTable()
        x.field_names = ["ID", 'Types of OS']
        os_version_list = {}
        for key in response['category_list'][node_type][os_type]:
            x.add_row([i, key['version']])
            os_version_list[str(i)] = key['version']
            i = i+1
        print(x)
        os_version = input("Select one of above id : ")
        while (not os_version in os_version_list):
            os_version = input("Select one of above id : ")
        os_version = os_version_list[os_version]

        node_type = node_type.split()
        node_type1 = ""
        for ele in node_type:
            node_type1 = node_type1 + ele + "%20"

        url = NODE_PLAN_LIST_URL.format(
            api_key=self.api_key, node_type1=node_type1, os_version=os_version, os_type=os_type)
        request_method = Methods.GET
        request_payload = {}
        response = Request(url, self.auth_token, request_payload,
                           request_method, user_agent=CLI_PYTHON).make_api_call()['data']
        i = 1
        x = PrettyTable()
        x.field_names = ["ID", 'Plan', 'image',
                         'location', 'Price(Monthly)', 'Price(Hourly)']
        plan_list = {}
        for key in response:
            x.add_row([i, key['plan'], key['image'], key['location'],
                      key['specs']['price_per_month'], key['specs']['price_per_hour']])
            plan_list[str(i)] = {"plan": key['plan'],
                                 "image": key['image'],
                                 "location": key['location']}
            i = i+1
        print(x)
        choice = input("Enter your choice : ")
        while (choice not in plan_list):
            choice = input("Select one of above id : ")
        return plan_list[choice]
