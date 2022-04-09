from utils.polyrobot import api_service as APIService
from utils.polyrobot.base import Deserializable
from utils.polyrobot.constants import NOTIFICATION_SLUG_TO_BUTTON_TEXT, NOTIFICATION_SLUG_TO_UPDATE_MESSAGE_TEXT, \
    NOTIFICATION_SLUG_TO_UPDATE_BUTTON_VALUES, NOTIFICATION_SLUG_TO_SWITCHABLE


class Preference(Deserializable):
    id: str
    slug: str
    enabled: bool
    value: int
    max_value: int

    def __init__(self, id: str, slug: str, enabled: bool, value: int, max_value: int):
        self.id = id
        self.slug = slug
        self.enabled = enabled
        self.value = value
        self.max_value = max_value

    @classmethod
    async def get(cls, id: str):
        data = await APIService.get(f"/user-preference/{id}/")
        return cls.deserialize(data)

    @classmethod
    async def update(cls, id: str, **kwargs):
        return cls.deserialize(await APIService.patch(f"/user-preference/{id}/", json=kwargs))

    def button_text(self):
        return NOTIFICATION_SLUG_TO_BUTTON_TEXT[self.slug]

    def update_value_message_text(self):
        return NOTIFICATION_SLUG_TO_UPDATE_MESSAGE_TEXT[self.slug]

    def update_values(self):
        return NOTIFICATION_SLUG_TO_UPDATE_BUTTON_VALUES[self.slug]

    def is_switchable(self):
        return NOTIFICATION_SLUG_TO_SWITCHABLE[self.slug]
