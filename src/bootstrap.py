from dataclasses import dataclass
from src.services import TaskService, StudentService, TestStudentService, TestTaskService, GitHubService, HTTPGitHubService


@dataclass
class Bootstrap:
    student_service: StudentService
    task_service: TaskService
    github_service: GitHubService


def get_test_bootstrap() -> Bootstrap:
    return Bootstrap(
        student_service=TestStudentService(),
        task_service=TestTaskService(),
        github_service=HTTPGitHubService()
    )
