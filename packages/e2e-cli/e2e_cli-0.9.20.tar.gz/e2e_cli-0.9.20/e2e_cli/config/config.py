import json
import os

from e2e_cli.config.config_service import is_valid
from e2e_cli.core.alias_service import get_user_cred, system_file
from e2e_cli.core.constants import RESERVES, DEFAULT, ALIAS
from e2e_cli.core.py_manager import PyVersionManager


class AuthConfig:
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.system_type, self.folder, self.file, self.log_file = system_file()

    def windows_hider(self):
        os.system("attrib +h " + self.folder)

    def windows_file_check(self):
        if not os.path.isdir(self.folder):
            return -1
        elif not os.path.isfile(self.file):
            self.windows_hider()
            return 0
        else:
            self.windows_hider()
            return 1

    def linux_mac_file_check(self):
        if not os.path.isdir(self.folder):
            return -1
        elif not os.path.isfile(self.file):
            return 0
        else:
            return 1

    def check_if_file_exist(self):
        if self.system_type == "Windows":
            return self.windows_file_check()
        elif self.system_type == "Linux" or self.system_type == "Darwin":
            return self.linux_mac_file_check()

    def reserve_keyword_check(self):
        if (str(self.kwargs[ALIAS]).lower() in RESERVES):
            print("The used alias name is a reserve keyword for cli tool")
        else:
            self.add_json_to_file()

    def add_json_to_file(self):
        api_access_credentials_object = {"api_key": self.kwargs["api_key"],
                                         "api_auth_token": self.kwargs["api_auth_token"]}
        if (is_valid(api_access_credentials_object["api_key"], api_access_credentials_object["api_auth_token"])):
            with open(self.file, 'r+') as file_reference:
                read_string = file_reference.read()
                if read_string == "":
                    file_reference.write(json.dumps({self.kwargs[ALIAS]:
                                                     api_access_credentials_object}))
                else:
                    api_access_credentials = json.loads(read_string)
                    api_access_credentials.update({self.kwargs[ALIAS]:
                                                   api_access_credentials_object})
                    file_reference.seek(0)
                    file_reference.write(json.dumps(api_access_credentials))

            print("Alias/user_name/Token name successfully added")
        else:

            print(
                "Invalid credentials given please enter correct Api key and Authorisation")
            return

    def add_to_config(self):
        file_exist_check_variable = self.check_if_file_exist()
        if file_exist_check_variable == -1:
            os.mkdir(self.folder)
            with open(self.file, 'w'):
                pass
            self.reserve_keyword_check()
        elif file_exist_check_variable == 0:
            with open(self.file, 'w'):
                pass
            self.reserve_keyword_check()
        elif file_exist_check_variable == 1:
            if (get_user_cred(self.kwargs[ALIAS], 2)):
                print(
                    "The given alias/username already exist!! Please use another name or delete the previous one")
            else:
                self.reserve_keyword_check()

    def delete_from_config(self, x=0):
        file_exist_check_variable = self.check_if_file_exist()
        if file_exist_check_variable == -1 | file_exist_check_variable == 0:
            print(
                "You need to add your api access credentials using the add functionality ")
            print("To know more please write 'e2e_cli alias -h' on your terminal")

        elif file_exist_check_variable == 1:
            with open(self.file, 'r+') as file_reference:
                file_contents_object = json.loads(file_reference.read())
                delete_output = file_contents_object.pop(
                    self.kwargs[ALIAS], 'No key found')

                if delete_output == "No key found" and x != 1:
                    print("No such alias found. Please re-check and enter again")
                else:
                    file_reference.seek(0)
                    file_reference.write(json.dumps(file_contents_object))
                    file_reference.truncate()
                    if (x != 1):
                        print("Alias/Token Successfully deleted")

    def adding_config_file(self, path):
        # for drag and drop
        if (path[0] == "'" and path[-1] == "'"):
            path = path.lstrip(path[0])
            path = path.rstrip(path[-1])

        if ((path.endswith("/config.json") or path == "config.json") and os.path.isfile(path)):

            if (self.check_if_file_exist() == -1):
                os.mkdir(self.folder)

            if self.system_type == "Windows":
                os.system('copy ' + path + ' ' + self.folder)
            elif self.system_type == "Linux" or self.system_type == "Darwin":
                os.system('cp ' + path + ' ' + self.folder)

            print("Token file successfuly added")

    def set_default(self):
        api_access_credentials_object = {"api_key": self.kwargs["api_key"],
                                         "api_auth_token": self.kwargs["api_auth_token"]}
        with open(self.file, 'r+') as file_reference:
            read_string = file_reference.read()
            if read_string == "":
                file_reference.write(json.dumps({DEFAULT:
                                                 api_access_credentials_object}))
            else:
                api_access_credentials = json.loads(read_string)
                api_access_credentials.update({DEFAULT:
                                               api_access_credentials_object})
                file_reference.seek(0)
                file_reference.truncate(0)
                file_reference.write(json.dumps(api_access_credentials))
