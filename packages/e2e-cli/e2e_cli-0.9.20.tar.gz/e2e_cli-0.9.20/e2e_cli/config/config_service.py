from e2e_cli.core.request_service import Request, Methods


def is_valid(api_key, auth_token):
    url = "api/v1/customer/details/?apikey=" + api_key+"&contact_person_id=null"
    response = Request(url, auth_token, {}, Methods.GET).make_api_call()
    if ('code' in response):
        return True
    else:
        return False
