from datetime import date, datetime
from typing import List

from aiohttp.http_exceptions import HttpProcessingError

from utils.polyrobot import api_service as APIService
from utils.polyrobot.academic_performance import AcademicPerformance
from utils.polyrobot.profile import Profile
from utils.polyrobot.schedule import ScheduledLesson


class User:
    id: int
    full_name: str
    username: str

    def __init__(self, id: int, full_name: str, username: str = None):
        self.id, self.full_name, self.username = id, full_name, username

    # API to get data direct from MosPolytech
    async def schedule(self) -> dict:
        return await APIService.get(f"/telegram/{self.id}/schedule/")

    async def session_schedule(self) -> dict:
        return await APIService.get(f"/telegram/{self.id}/session-schedule/")

    async def profile(self) -> Profile:
        data = await APIService.get(f"/telegram/{self.id}/profile/")
        return Profile.deserialize(data["user"])

    async def payments(self):
        return await APIService.get(f"/telegram/{self.id}/payments/")

    async def academic_performance(self, semester_number: int = None):
        if semester_number:
            data = await APIService.get(f"/telegram/{self.id}/academic-performance?semester_number={semester_number}")
        else:
            data = await APIService.get(f"/telegram/{self.id}/academic-performance/")
        return [AcademicPerformance.deserialize(academic_performance) for academic_performance in
                data['academicPerformance']]

    # API to get data from PolyRobot
    async def scheduled_lesson(
            self, date_obj: date = None, date_from: datetime = None, date_to: datetime = None
    ) -> List[ScheduledLesson]:
        url = f"/telegram/{self.id}/scheduled-lesson"
        if date_obj:
            url += f"?date={date_obj.strftime('%Y-%m-%d')}"
        elif date_from or date_to:
            if date_from:
                url += f"?date={date_obj.strftime('%Y-%m-%d')}"
            if date_to:
                url += f"?date={date_obj.strftime('%Y-%m-%d')}"

        return [ScheduledLesson.deserialize(scheduled_lesson) for scheduled_lesson in await APIService.get(url)]

    @staticmethod
    async def get(id: int):
        data = await APIService.get(f"/telegram/{id}/")
        return User(**data)

    @staticmethod
    async def get_or_create(id: int, full_name: str, username: str):
        try:
            data = await APIService.get(f"/telegram/{id}/")
        except HttpProcessingError as error:
            if error.code == 404:
                data = await APIService.post("/telegram/",
                                             json={"id": id, "full_name": full_name, "username": username})
            raise error
        return User(**data)
