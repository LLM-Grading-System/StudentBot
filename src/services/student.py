import datetime
from abc import ABC, abstractmethod
from dataclasses import dataclass
from src.services.exceptions import StudentAlreadyExistsError, StudentNotFoundError


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
