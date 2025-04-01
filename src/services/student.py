import datetime
import json
from abc import ABC, abstractmethod
from dataclasses import dataclass

import aiohttp

from src.services.exceptions import StudentAlreadyExistsError, StudentNotFoundError
from src.settings import app_settings


@dataclass
class StudentDTO:
    telegram_user_id: int
    telegram_username: str
    github_username: str
    joined_at: datetime.date
    has_enabled_notifications: bool


class StudentService(ABC):
    @abstractmethod
    async def create_student(self, telegram_user_id: int, telegram_username: str) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_student_by_telegram_user_id(self, telegram_user_id: int) -> StudentDTO:
        raise NotImplementedError

    @abstractmethod
    async def get_student_by_github_username(self, github_username: str) -> StudentDTO:
        raise NotImplementedError

    @abstractmethod
    async def set_github_username(self, telegram_user_id: int, github_username: str) -> None:
        raise NotImplementedError


class TestStudentService(StudentService):
    def __init__(self):
        self.students: dict[int:StudentDTO] = dict()

    async def create_student(self, telegram_user_id: int, telegram_username: str) -> None:
        if telegram_user_id in self.students:
            raise StudentAlreadyExistsError(telegram_user_id)
        current_date = datetime.date.today()
        student = StudentDTO(telegram_user_id, telegram_username, "", current_date, True)
        self.students[telegram_user_id] = student

    async def get_student_by_telegram_user_id(self, telegram_user_id: int) -> StudentDTO:
        if telegram_user_id not in self.students:
            raise StudentNotFoundError(telegram_user_id)
        return self.students[telegram_user_id]

    async def set_github_username(self, telegram_user_id: int, github_username: str) -> None:
        if telegram_user_id not in self.students:
            raise StudentNotFoundError(telegram_user_id)
        student: StudentDTO = self.students[telegram_user_id]
        student.github_username = github_username


class APIStudentService(StudentService):
    def __init__(self):
        self._endpoint = app_settings.core_api_endpoint

    async def create_student(self, telegram_user_id: int, telegram_username: str) -> None:
        create_student_endpoint = f"{self._endpoint}/api/students"
        async with aiohttp.ClientSession() as session:
            data = {
                "telegramUserId": telegram_user_id,
                "telegramUsername": telegram_username
            }
            async with session.post(create_student_endpoint, json=data) as res:
                if res.status == 409:
                    raise StudentAlreadyExistsError(telegram_user_id)
                content = await res.text(encoding="utf-8")
                print(content)

    async def get_student_by_telegram_user_id(self, telegram_user_id: int) -> StudentDTO:
        get_student_endpoint = f"{self._endpoint}/api/students/telegram/{telegram_user_id}"
        async with aiohttp.ClientSession() as session:
            async with session.get(get_student_endpoint) as res:
                if res.status == 404:
                    raise StudentNotFoundError(telegram_user_id)
                content = await res.text(encoding="utf-8")
                data = json.loads(content)
                return StudentDTO(
                    telegram_user_id=data["telegramUserId"],
                    telegram_username=data["telegramUsername"],
                    github_username=data["githubUsername"],
                    joined_at=data["registeredAt"],
                    has_enabled_notifications=True
                )

    async def get_student_by_github_username(self, github_username: str) -> StudentDTO:
        get_student_endpoint = f"{self._endpoint}/api/students/github/{github_username}"
        async with aiohttp.ClientSession() as session:
            async with session.get(get_student_endpoint) as res:
                if res.status == 404:
                    raise StudentNotFoundError(github_username)
                content = await res.text(encoding="utf-8")
                data = json.loads(content)
                return StudentDTO(
                    telegram_user_id=data["telegramUserId"],
                    telegram_username=data["telegramUsername"],
                    github_username=data["githubUsername"],
                    joined_at=data["registeredAt"],
                    has_enabled_notifications=True
                )

    async def set_github_username(self, telegram_user_id: int, github_username: str) -> None:
        set_student_github_endpoint = f"{self._endpoint}/api/students/telegram/{telegram_user_id}"
        async with aiohttp.ClientSession() as session:
            data = {
                "githubUsername": github_username
            }
            async with session.put(set_student_github_endpoint, json=data) as res:
                if res.status == 404:
                    raise StudentNotFoundError(telegram_user_id)
                content = await res.text(encoding="utf-8")
                print(content)
