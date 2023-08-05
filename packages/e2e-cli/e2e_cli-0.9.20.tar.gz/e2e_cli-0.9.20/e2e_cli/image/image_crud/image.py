import json

from e2e_cli.core.alias_service import get_user_cred
from e2e_cli.core.constants import CONFIRMATION_MSG, ALIAS, YES
from e2e_cli.core.helper_service import Checks
from e2e_cli.core.py_manager import PyVersionManager
from e2e_cli.core.request_service import Methods, Request
from e2e_cli.image.image_crud import helpers


def response_output(status, request_method):
    Checks.status_result(status, request_method)
    Checks.show_json(status)


class ImageCrud:
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        if (get_user_cred(kwargs[ALIAS])):
            self.api_key = get_user_cred(kwargs[ALIAS])[1]
            self.auth_token = get_user_cred(kwargs[ALIAS])[0]
            self.possible = True
        else:
            self.possible = False

    def caller(self, method):
        function_set = {"create": self.create_image,
                        "delete": self.delete_image,
                        "list": self.list_image,
                        "rename": self.rename_image
                        }
        return function_set.get(method)

    def create_image(self):
        api_key = self.api_key
        auth_token = self.auth_token
        helpers.create_image_helper(self.kwargs["inputs"])
        node_id = self.kwargs["inputs"]["node_id"]
        new_image_name = self.kwargs["inputs"]["image_name"]
        request_payload = json.dumps({
            "name": new_image_name,
            "type": "save_images"
        })
        url = f"api/v1/nodes/{node_id}/actions/?apikey={api_key}&location=Delhi"
        request_method = Methods.POST
        status = Request(url, auth_token, request_payload, request_method).make_api_call()

        response_output(status, request_method)

    def delete_image(self):
        api_key = self.api_key
        auth_token = self.auth_token
        helpers.delete_image_helper(self.kwargs["inputs"])
        image_id = self.kwargs["inputs"]["image_id"]
        request_payload = json.dumps({
            "action_type": "delete_image"
        })
        url = f"api/v1/images/{image_id}/?apikey={api_key}&location=Delhi"
        request_method = Methods.POST
        if (input(CONFIRMATION_MSG).lower() == YES):
            status = Request(url, auth_token, request_payload, request_method).make_api_call()

        response_output(status, request_method)

    def rename_image(self):
        api_key = self.api_key
        auth_token = self.auth_token
        helpers.rename_image_helper(self.kwargs["inputs"])
        image_id = self.kwargs["inputs"]["image_id"]
        new_name = self.kwargs["inputs"]["new_name"]
        request_payload = json.dumps({
            "name": new_name,
            "action_type": "rename"
        })
        url = f"api/v1/images/{image_id}/?apikey={api_key}&location=Delhi"
        request_method = Methods.POST
        status = Request(url, auth_token, request_payload, request_method).make_api_call()

        response_output(status, request_method)

    def list_image(self):
        request_payload = {}
        api_key = self.api_key
        auth_token = self.auth_token
        url = "api/v1/images/saved-images/?apikey="+api_key+"&location=Delhi"
        request_method = Methods.GET
        status = Request(url, auth_token, request_payload, request_method).make_api_call()

        response_output(status, request_method)
