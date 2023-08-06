from aiohttp import ContentTypeError, ClientResponse


async def raise_exception_if_not_ok(response: ClientResponse):
    if response.status < 400:
        return
    resp_json = await __get_json_or_raise_for_status(response)

    raise Exception(get_response_error_message(response.status, resp_json))


async def __get_json_or_raise_for_status(response: ClientResponse):
    try:
        return await response.json()
    except ContentTypeError as e:
        # if no json available in response then use raise_for_status() to raise exception
        response.raise_for_status()


def get_response_error_message(status_code, resp_json):
    error_msg = f"received {status_code}"

    err_type = resp_json.get("type", "")
    message = resp_json.get("message", "")
    if err_type:
        error_msg += f" : {err_type}"

    if message:
        error_msg += f" : {message}"

    return error_msg
