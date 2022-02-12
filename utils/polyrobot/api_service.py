import ssl
from typing import Union

import certifi
from aiohttp import ClientSession
from aiohttp.http_exceptions import HttpProcessingError

from data.config import POLYROBOT_TOKEN, POLYROBOT_ENDPOINT


async def request(method: str, path: str, json: dict = None) -> Union[dict, list]:
    http_error_msg = ""

    ssl_context = ssl.create_default_context(cafile=certifi.where())
    async with ClientSession() as session:
        async with session.request(method=method, url=POLYROBOT_ENDPOINT + "/api" + path,
                                   headers={"Authorization": f"Token {POLYROBOT_TOKEN}",
                                            "Content-Type": "application/json"},
                                   json=json,
                                   ssl=ssl_context) as response:

            if 400 <= response.status < 500:
                http_error_msg = f"Client Error: {response.reason}"
            elif 500 <= response.status < 600:
                http_error_msg = f"Server Error: {response.reason}"

            if http_error_msg:
                raise HttpProcessingError(code=response.status, message=http_error_msg)

            data = await response.json()
            return data


async def get(path: str) -> Union[dict, list]:
    return await request(method="GET", path=path)


async def post(path: str, json: dict = None) -> Union[dict, list]:
    return await request(method="POST", path=path, json=json)


async def put(path: str, json: dict = None) -> Union[dict, list]:
    return await request(method="PUT", path=path, json=json)


async def patch(path: str, json: dict = None) -> Union[dict, list]:
    return await request(method="PATCH", path=path, json=json)


async def delete(path: str) -> Union[dict, list]:
    return await request(method="DELETE", path=path)
