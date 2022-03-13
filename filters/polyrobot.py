from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import Message
from http3.exceptions import HttpError

from utils.polyrobot.user import User


class IsAuthenticated(BoundFilter):
    key = 'is_authenticated'

    def __init__(self, is_authenticated):
        self.is_authenticated = is_authenticated

    async def check(self, message: Message):
        try:
            user = User(message.from_user.id, message.from_user.full_name, message.from_user.username)
            await user.profile()
        except HttpError:
            return False
        else:
            return True
