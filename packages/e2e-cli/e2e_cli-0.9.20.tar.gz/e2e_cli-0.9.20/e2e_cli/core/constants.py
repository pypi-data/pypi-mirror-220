# constant, reserved keywords
RESERVES = ["alias", "all", "config", "node", "bucket", "lb", "dbaas", "create",
            "get", "list", "update", "edit", "delete", "file", "doc", "help", "default"]

# names of apps/common constants
# note these are common keywords used in whole cli code, especially for service/command names or as common key names
DEFAULT = "default"
E2E_CLI = "e2e_cli"
ALIAS = "alias"
CONFIG = "config"
BUCKET = "bucket"
DBAAS = "dbaas"
NODE = "node"
LB = "lb"
IMAGE = "image"
SECURITY_GROUPS = "security_groups"
VOLUME = "volume"
VPC = "vpc"
AUTOSCALING = "autoscaling"
CDN = "cdn"
LOGS = "logs"
_HELP = "-h"
YES = "y"


# version
PACKAGE_VERSION = "e2e-cli/1.0.0 Python Linux/Mac/Windows"

# package_info
PACKAGE_INFO = " A command line tool developed by E2E Networks Ltd. \n Used to access and manage my_account/e2e_cloud services from cmd/shell \n Published 1st April 2023"

# url for api request
BASE_URL = "https://api.e2enetworks.com/myaccount/"
# BASE_URL = "https://api-thor.e2enetworks.net/myaccount/"


# for better error handeling, write --action options and related help strings here for argparser

NODE_ACTIONS = ["enable_recovery", "disable_recovery", "reinstall", "reboot",
                "power_on", "power_off", "rename_node", "lock_vm", "unlock_vm", "monitor"]
NODE_ACTIONS_STR = """
        lock_vm
        unlock_vm
        reinstall
        reboot
        power_on
        power_off
        monitor
        rename_node
        enable_recovery
        disable_recovery
"""

BUCKET_ACTIONS = ["enable_versioning", "disable_versioning", "create_key",
                  "delete_key", "list_key", "lock_key", "unlock_key", "add_permission"]
BUCKET_ACTIONS_STR = """
        enable_versioning
        disable_versioning
        create_key
        delete_key
        list_key
        lock_key
        unlock_key
        add_permission
"""

DBAAS_ACTIONS = ["take_snapshot", "reset_password", "stop_db", "start_db", "restart_db", "enable_backup",
                 "disable_backup", "add_parameter_group", "remove_parameter_group", "add_vpc", "remove_vpc"]
DBAAS_ACTIONS_STR = """
        take_snapshot
        reset_password
        add_vpc
        remove_vpc
        stop_db
        start_db
        restart_db
        enable_backup
        disable_backup
        add_parameter_group
        remove_parameter_group
"""

CDN_ACTIONS = ["enable_cdn", "disable_cdn",
               "cdn_monitoring", "cdn_bandwidth_usage"]
CDN_ACTIONS_STR = """
        enable_cdn
        disable_cdn
        cdn_monitoring
        cdn_bandwidth_usage
"""

VOLUMES_ACTIONS = []


# messages
VALID_ALIAS = "Valid alias"
INVALID_ALIAS = "Warning : The given alias/credential doesn't exist"
CONFIRMATION_MSG = "are you sure you want to proceed, press y for yes, else any other key : "
SUCCESSFULLY_DELETED_MSG = "{service} successfully deleted, \n use following command -> e2e_cli --alias=<value> {service} list to check if {service} has been deleted"

# user-agents
CLI_PYTHON = "cli_python"
CLI_E2E = 'cli-e2e'
