from dataclasses import dataclass
from src.services import (
    TaskService, StudentService,GitHubService, HTTPGitHubService,
    StatisticsService, TestStatisticsService
)
from src.services.student import APIStudentService
from src.services.task import APITaskService


@dataclass
class Bootstrap:
    student_service: StudentService
    task_service: TaskService
    github_service: GitHubService
    statistics_service: StatisticsService


def get_bootstrap() -> Bootstrap:
    return Bootstrap(
        student_service=APIStudentService(),
        task_service=APITaskService(),
        github_service=HTTPGitHubService(),
        statistics_service=TestStatisticsService()
    )
