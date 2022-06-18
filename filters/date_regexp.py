import re

from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import Message

DATE_REGEXP_LIST = [
    r"(0?[1-9]|[12][0-9]|3[01])\.(0?[1-9]|[1][0-2])\.(\d*)",
    r"(0?[1-9]|[12][0-9]|3[01])/(0?[1-9]|[1][0-2])/(\d*)",
    r"(\d*)\.(0?[1-9]|[1][0-2])\.(0?[1-9]|[12][0-9]|3[01])",
    r"(\d*)/(0?[1-9]|[1][0-2])/(0?[1-9]|[12][0-9]|3[01])",
]


class IsDate(BoundFilter):
    key = "is_date"

    def __init__(self, is_date):
        self.is_date = is_date

    async def check(self, message: Message):
        if any([re.search(r, message.text) for r in DATE_REGEXP_LIST]):
            return True
        return False
