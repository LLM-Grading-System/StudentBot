import datetime
from abc import ABC, abstractmethod
from dataclasses import dataclass
from src.services.exceptions import StudentAlreadyExistsError, StudentNotFoundError


@dataclass
class TaskStatisticsDTO:
    task_name: str
    task_attempt: int
    task_score: float


@dataclass
class StatisticsDTO:
    telegram_user_id: int
    tasks: list[TaskStatisticsDTO]


class StatisticsService(ABC):
    @abstractmethod
    async def get_statistics_by_telegram_user_id(self, telegram_user_id: int) -> StatisticsDTO:
        raise NotImplementedError


class TestStatisticsService(StatisticsService):
    def __init__(self):
        self.statistics = StatisticsDTO(
            telegram_user_id=1,
            tasks=[
                TaskStatisticsDTO(task_name="Уравнение на LangChain", task_attempt=4, task_score=0.785),
                TaskStatisticsDTO(task_name="Advanced RAG", task_attempt=2, task_score=0.25),
                TaskStatisticsDTO(task_name="CoT SO Practice", task_attempt=0, task_score=0)
            ]
        )

    async def get_statistics_by_telegram_user_id(self, telegram_user_id: int) -> StatisticsDTO:
        return self.statistics
