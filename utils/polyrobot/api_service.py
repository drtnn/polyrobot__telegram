from typing import Union

from http3 import AsyncClient

from data.config import POLYROBOT_TOKEN, POLYROBOT_ENDPOINT


async def request(
        method: str, path: str, json: dict = None, data: dict = None, files: dict = None
) -> Union[dict, list]:
    client = AsyncClient()
    response = await client.request(method=method, url=POLYROBOT_ENDPOINT + "/api" + path,
                                    headers={"Authorization": f"Token {POLYROBOT_TOKEN}"},
                                    json=json, data=data, files=files, verify=False)
    response.raise_for_status()
    return response.json()


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
