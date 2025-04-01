from abc import ABC, abstractmethod


class ServiceError(BaseException, ABC):
    @abstractmethod
    def message(self) -> str:
        raise NotImplementedError


class StudentAlreadyExistsError(ServiceError):
    def __init__(self, telegram_user: int | str) -> None:
        self.telegram_user = telegram_user

    @property
    def message(self) -> str:
        return f"Пользователь с id={self.telegram_user} уже существует"


class StudentNotFoundError(ServiceError):
    def __init__(self, telegram_user: int | str) -> None:
        self.telegram_user = telegram_user

    @property
    def message(self) -> str:
        return f"Пользователь с id={self.telegram_user} не существует"
