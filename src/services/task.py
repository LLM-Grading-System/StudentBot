import json
from abc import ABC, abstractmethod
from dataclasses import dataclass

import aiohttp

from src.settings import app_settings


@dataclass
class TaskDTO:
    task_id: str
    name: str


@dataclass
class ComplaintDTO:
    complaint_id: str
    task_id: str
    description: str


class TaskService(ABC):
    @abstractmethod
    async def create_complaint_by_task(self, user_id: int, task_id: str, description: str):
        raise NotImplementedError

    @abstractmethod
    async def get_tasks(self) -> list[TaskDTO]:
        raise NotImplementedError


class TestTaskService(TaskService):
    def __init__(self):
        self.tasks = [
            TaskDTO(task_id="1", name="Введение в LangChain"),
            TaskDTO(task_id="2", name="Продвинутая архитектура RAG"),
            TaskDTO(task_id="3", name="Интерфейс на Chainlit"),
        ]
        self.complaints = []

    async def create_complaint_by_task(self, user_id: int, task_id: str, description: str):
        complaint = ComplaintDTO(
            complaint_id=str(len(self.complaints) + 1),
            task_id=task_id,
            description=description
        )
        self.complaints.append(complaint)

    async def get_tasks(self) -> list[TaskDTO]:
        return self.tasks


class APITaskService(TaskService):
    def __init__(self):
        self._endpoint = app_settings.core_api_endpoint
        self._tasks: list[TaskDTO] = []

    async def create_complaint_by_task(self, user_id: int, task_id: str, description: str) -> str:
        create_complaint_endpoint = f"{self._endpoint}/api/complaints"
        async with aiohttp.ClientSession() as session:
            data = {
              "taskId": task_id,
              "studentTelegramUserId": user_id,
              "studentRequest": description
            }
            async with session.post(create_complaint_endpoint, json=data) as res:
                content = await res.text(encoding="utf-8")
                data = json.loads(content)
        return data["message"]


    async def get_tasks(self) -> list[TaskDTO]:
        get_tasks_endpoint = f"{self._endpoint}/api/tasks/public"
        async with aiohttp.ClientSession() as session:
            async with session.get(get_tasks_endpoint) as res:
                content = await res.text(encoding="utf-8")
                data = json.loads(content)
                tasks = [TaskDTO(task_id=item["taskId"], name=item["name"]) for item in data]
        self._tasks = tasks
        return tasks
