from datetime import datetime
from io import BytesIO

from utils.polyrobot import api_service as APIService
from utils.polyrobot.base import Deserializable


class File(Deserializable):
    id: str
    created_at: datetime
    data: str

    CREATED_AT = "created_at"

    def __init__(self, id: str, created_at: datetime, data: str):
        self.id = id
        self.created_at = created_at
        self.data = data

    @classmethod
    def deserialize(cls, data: dict):
        data[cls.CREATED_AT] = datetime.fromisoformat(data[cls.CREATED_AT])
        return super().deserialize(data)

    @classmethod
    async def upload(cls, *files: tuple):
        file_objs = []

        for file in files:
            data = await APIService.post("/file/", files={"data": file})
            file_objs.append(cls.deserialize(data))

        return file_objs
