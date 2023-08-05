import json
import os
import platform

from e2e_cli.core.py_manager import PyVersionManager
from e2e_cli.core.constants import RESERVES, VALID_ALIAS, INVALID_ALIAS, DEFAULT

__NIX_SYSTEM = ["Linux", "Darwin"]
__WINDOWS = "Windows"
__E2E_FOLDER = ".E2E_CLI"
__E2E_LOGS = "cli_logs.log"
__E2E_CONFIG = "config.json"


def system_file():
    home_directory = os.path.expanduser("~")
    if platform.system() == __WINDOWS:
        return __WINDOWS, f"{home_directory}\{__E2E_FOLDER}", f"{home_directory}\{__E2E_FOLDER}\{__E2E_CONFIG}", f"{home_directory}\{__E2E_FOLDER}\{__E2E_LOGS}"
    elif platform.system() in __NIX_SYSTEM:
        return platform.system(), f"{home_directory}/{__E2E_FOLDER}", f"{home_directory}/{__E2E_FOLDER}/{__E2E_CONFIG}", f"{home_directory}/{__E2E_FOLDER}/{__E2E_LOGS}"


class AliasServices:
    def __init__(self, alias):
        self.alias = alias

    def get_api_credentials(self):
        system_type, folder, config_file, log_file = system_file()
        file_reference = open(config_file, "r")
        config_file_object = json.loads(file_reference.read())
        if self.alias in config_file_object:
            if (self.alias == DEFAULT):
                default_alias = config_file_object[DEFAULT]['api_key']
                return {"api_credentials": config_file_object[default_alias],
                        "message": VALID_ALIAS}
            else:
                return {"api_credentials": config_file_object[self.alias],
                        "message": VALID_ALIAS}
        else:
            return {"message": INVALID_ALIAS}


def get_user_cred(name, type=0):
    # type=0 default case, get credential api key, token
    # type=1 fetch all alias/token list
    # type=2 checking existance of alias on system

    system_type, folder, config_file, log_file = system_file()
    f = open(config_file)
    data = json.load(f)
    f.close()

    # viewing alias
    if (name == "all" and type == 1):
        try:
            print("default --> ", data[DEFAULT]['api_key'])
        except:
            print("default --> ", "Not set")
        return data.keys()

    # getting/checking alias
    if (name in data):
        if (name == DEFAULT):
            return get_user_cred(data[DEFAULT]['api_key'])
        else:
            return [data[name]['api_auth_token'], data[name]['api_key']]
    # checking existance of alias on system
    elif type == 2:
        return None
    else:
        print(INVALID_ALIAS)
        return None
