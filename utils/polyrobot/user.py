from datetime import date, datetime
from typing import List
from urllib.parse import urlencode

from http3.exceptions import HttpError

from utils.polyrobot import api_service as APIService
from utils.polyrobot.academic_performance import AcademicPerformance
from utils.polyrobot.base import Deserializable
from utils.polyrobot.payments import Payments
from utils.polyrobot.preference import Preference
from utils.polyrobot.profile import Profile
from utils.polyrobot.schedule import ScheduledLesson


class User(Deserializable):
    id: int
    full_name: str
    username: str
    preferences: List[Preference]
    is_admin: bool

    PREFERENCES = "preferences"

    def __init__(self, id: int, full_name: str, is_admin: bool, username: str = None,
                 preferences: List[Preference] = None, **kwargs):
        self.id = id
        self.full_name = full_name
        self.is_admin = is_admin
        self.preferences = preferences
        self.username = username
        super().__init__(**kwargs)

    @classmethod
    def deserialize(cls, data: dict):
        data[cls.PREFERENCES] = [Preference.deserialize(preference) for preference in data[cls.PREFERENCES]]
        return super().deserialize(data)

    @classmethod
    async def get(cls, id: int):
        data = await APIService.get(f"/telegram/{id}/")
        return cls.deserialize(data)

    @classmethod
    async def get_or_create(cls, id: int, full_name: str, username: str):
        try:
            data = await APIService.get(f"/telegram/{id}/")
        except HttpError as error:
            data = await APIService.post("/telegram/", json={"id": id, "full_name": full_name, "username": username})
        return cls.deserialize(data)

    @classmethod
    async def admins(cls):
        return [cls.deserialize(data) for data in await APIService.get(f"/telegram/admin/")]

    # API to get data direct from MosPolytech
    async def schedule(self) -> dict:
        return await APIService.get(f"/telegram/{self.id}/schedule/")

    async def session_schedule(self) -> dict:
        return await APIService.get(f"/telegram/{self.id}/session-schedule/")

    async def profile(self) -> Profile:
        data = await APIService.get(f"/telegram/{self.id}/profile/")
        return Profile.deserialize(data["user"])

    async def payments(self):
        return Payments.deserialize((await APIService.get(f"/telegram/{self.id}/payments/"))["contracts"])

    async def academic_performance(self, semester_number: int = None):
        if semester_number:
            data = await APIService.get(f"/telegram/{self.id}/academic-performance?semester_number={semester_number}")
        else:
            data = await APIService.get(f"/telegram/{self.id}/academic-performance/")
        return [AcademicPerformance.deserialize(academic_performance) for academic_performance in
                data["academicPerformance"]]

    # API to get data from PolyRobot
    async def scheduled_lesson(
            self, datetime_obj: date = None, datetime_from: datetime = None, datetime_to: datetime = None
    ) -> List[ScheduledLesson]:
        query_params = {}
        if datetime_obj:
            query_params["date"] = datetime_obj.strftime('%Y-%m-%d')
        elif datetime_from or datetime_to:
            if datetime_from:
                query_params["date_from"] = datetime_from.strftime('%Y-%m-%d')
            if datetime_to:
                query_params["date_to"] = datetime_to.strftime('%Y-%m-%d')

        url = f"/telegram/{self.id}/scheduled-lesson?" + urlencode(query_params)
        return [ScheduledLesson.deserialize(scheduled_lesson) for scheduled_lesson in await APIService.get(url)]

    async def export_schedule(self):
        return await APIService.get(f"/telegram/{self.id}/scheduled-lesson/export")
