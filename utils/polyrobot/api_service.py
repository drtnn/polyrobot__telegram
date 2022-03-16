from typing import Union

from http3 import AsyncClient, StatusCode, AsyncResponse
from http3.exceptions import HttpError

from data.config import POLYROBOT_TOKEN, POLYROBOT_ENDPOINT


def raise_for_status(response: AsyncResponse) -> None:
    """
    Raise the `HttpError` if one occurred.
    """
    message = (
        "{0.status_code} {error_type}: {0.reason_phrase} for url: {0.url}\n"
        "Response data: {0.text}\n"
        "For more information check: https://httpstatuses.com/{0.status_code}"
    )

    if StatusCode.is_client_error(response.status_code):
        message = message.format(response, error_type="Client Error")
    elif StatusCode.is_server_error(response.status_code):
        message = message.format(response, error_type="Server Error")
    else:
        message = None

    if message:
        raise HttpError(message)


async def request(
        method: str, path: str, json: dict = None, data: dict = None, files: dict = None
) -> Union[dict, list, bytes, None]:
    client = AsyncClient()
    response = await client.request(method=method, url=POLYROBOT_ENDPOINT + "/api" + path,
                                    headers={"Authorization": f"Token {POLYROBOT_TOKEN}"},
                                    json=json, data=data, files=files, verify=False)
    raise_for_status(response=response)

    if response.headers.get("content-type") == "application/json":
        return response.json()
    else:
        return response.content


async def get(path: str) -> Union[dict, list]:
    return await request(method="GET", path=path)


async def post(path: str, json: dict = None, data: dict = None, files: dict = None) -> Union[dict, list]:
    return await request(method="POST", path=path, json=json, data=data, files=files)


async def put(path: str, json: dict = None, data: dict = None, files: dict = None) -> Union[dict, list]:
    return await request(method="PUT", path=path, json=json, data=data, files=files)


async def patch(path: str, json: dict = None, data: dict = None, files: dict = None) -> Union[dict, list]:
    return await request(method="PATCH", path=path, json=json, data=data, files=files)


async def delete(path: str) -> Union[dict, list]:
    return await request(method="DELETE", path=path)
