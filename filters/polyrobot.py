from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import Message
from aiohttp.http_exceptions import HttpProcessingError

from utils.polyrobot.user import User


class IsAuthenticated(BoundFilter):
    key = 'is_authenticated'

    def __init__(self, is_authenticated):
        self.is_authenticated = is_authenticated

    async def check(self, message: Message):
        try:
            user = await User.get(message.from_user.id)
            await user.information()
        except HttpProcessingError:
            return False
        else:
            return True
