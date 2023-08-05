from e2e_cli.core.constants import ALIAS
from e2e_cli.core.helper_service import ApiFilter, Checks
from e2e_cli.node.node_crud.node_listing_service import Nodelisting


def node_create_helper(arguments):
    required = {"name": str, "region": str, "plan": str,
                "image": str, "security_group_id": int}
    optional = {"ssh_keys": str,
                "start_scripts": str,
                "backups": bool,
                "enable_bitninja": bool,
                "disable_password": bool,
                "is_saved_image": bool,
                "saved_image_template_id": int,
                "is_ipv6_availed": bool,
                "vpc_id": int,
                "default_public_ip": bool,
                "ngc_container_id": int,
                "reserve_ip": "",
                "reserve_ip_pool": "", }
    return __creation_payload(arguments)


def __creation_payload(arguments):
    payload = {}
    if ('auto' in arguments["inputs"]):
        node_specifications = Nodelisting(
            arguments[ALIAS]).node_listing()
        payload["image"] = node_specifications['image']
        payload["plan"] = node_specifications['plan']
        if (node_specifications['location'] == 'Delhi'):
            payload["region"] = 'ncr'
        else:
            payload["region"] = 'mumbai'
    else:
        payload["image"] = Checks.take_input(arguments["inputs"], "image")
        payload["plan"] = Checks.take_input(arguments["inputs"], "plan")
        payload["region"] = Checks.take_input(arguments["inputs"], "region")

    payload["security_group_id"] = Checks.take_input(
        arguments["inputs"], "security_group_id")
    payload["name"] = Checks.take_input(arguments["inputs"], "name")
    payload["ssh_keys"] = []
    if ("ssh_keys" in arguments["inputs"]):
        payload["ssh_keys"].append(arguments["inputs"]["ssh_keys"])
    payload["start_scripts"] = []
    return payload


def node_delete_helper(inputs):
    required = {"node_id": int, }
    optional = {}
    ApiFilter(inputs, required, optional)


def node_get_helper(inputs):
    required = {"node_id": int, }
    optional = {}
    ApiFilter(inputs, required, optional)


class __Check:
    """Note format for input checks has been defined in this way, so that data type and format both can be handeled by inputs_and_required_check and inputs_and_optional_check
    All checks/validation functions must follow this format/syntax as shown for bucket_name_validity"""
