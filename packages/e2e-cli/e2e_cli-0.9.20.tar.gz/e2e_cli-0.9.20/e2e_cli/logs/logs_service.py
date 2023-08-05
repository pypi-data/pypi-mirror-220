from datetime import datetime
import logging

from e2e_cli.core.alias_service import system_file
from e2e_cli.core.py_manager import PyVersionManager

__system_type, __folder, __config_file, __logs_file = system_file()

logging.basicConfig(filename=__logs_file)
logger = logging.getLogger("E2E_CLI LOGGER")


# open to all for logging records
def save_to_logs(arguments, response_traceback):
    logger.error("ERROR IN COMMAND, : {}, {}".format(
        str(datetime.now()), arguments))
    logger.error(response_traceback)


def caller(method):
    function_set = {"view": __view_logs,
                    "clear": __clear_logs,
                    }
    return function_set.get(method)


def __view_logs():
    try:
        with open(__logs_file, 'r+') as file_reference:
            read_string = file_reference.read()
        print(read_string)
    except:
        print("Error : logs not found")


def __clear_logs():
    try:
        with open(__logs_file, 'w') as file_reference:
            file_reference.write("")
    except:
        print("Error : logs not found")
