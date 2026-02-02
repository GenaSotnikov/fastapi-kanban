from abc import ABC, abstractmethod


class DatabaseSession(ABC):
    @abstractmethod
    async def select[T](self, model: type[T], params: dict) -> T | None:
        ...
    @abstractmethod
    async def insert[T](self, model: type[T], data: T) -> T | None:
        ...