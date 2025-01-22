from abc import ABC, abstractmethod


class ServiceError(BaseException, ABC):
    @abstractmethod
    def message(self) -> str:
        raise NotImplementedError


class StudentAlreadyExistsError(ServiceError):
    def __init__(self, telegram_user_id: int) -> None:
        self.telegram_user_id = telegram_user_id

    @property
    def message(self) -> str:
        return f"Пользователь с id={self.telegram_user_id} уже существует"


class StudentNotFoundError(ServiceError):
    def __init__(self, telegram_user_id: int) -> None:
        self.telegram_user_id = telegram_user_id

    @property
    def message(self) -> str:
        return f"Пользователь с id={self.telegram_user_id} уже существует"
