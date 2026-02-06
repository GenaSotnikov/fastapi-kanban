from abc import ABC, abstractmethod
from typing import Any


class DatabaseSession(ABC):
    @abstractmethod
    def select[T](self, model: type[T], params: dict[str, Any]) -> list[T] | None:
        ...
    @abstractmethod
    def insert[T](self, model: type[T], data: T) -> T | None:
        ...
    
    @abstractmethod
    def execute_raw(self, sql_query: str, params: dict[str, Any] | None = None) -> Any:
        ...
