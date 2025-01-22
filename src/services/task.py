from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class TaskDTO:
    task_id: int
    name: str


@dataclass
class ComplaintDTO:
    complaint_id: int
    task_id: int
    description: str


class TaskService(ABC):
    @abstractmethod
    async def create_complaint_by_task(self, task_id: int, description: str):
        raise NotImplementedError

    @abstractmethod
    async def get_tasks(self) -> list[TaskDTO]:
        raise NotImplementedError


class TestTaskService(TaskService):
    def __init__(self):
        self.tasks = [
            TaskDTO(task_id=1, name="Введение в LangChain"),
            TaskDTO(task_id=2, name="Продвинутая архитектура RAG"),
            TaskDTO(task_id=3, name="Интерфейс на Chainlit"),
        ]
        self.complaints = []

    async def create_complaint_by_task(self, task_id: int, description: str):
        complaint = ComplaintDTO(
            complaint_id=len(self.complaints) + 1,
            task_id=task_id,
            description=description
        )
        self.complaints.append(complaint)

    async def get_tasks(self) -> list[TaskDTO]:
        return self.tasks
