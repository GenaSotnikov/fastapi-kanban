from fastapi.logger import logger
import logging
from typing import Any
from typing import Annotated, Generator
from fastapi.params import Depends
from sqlmodel import Session, create_engine, select
from sqlalchemy import text
from sqlalchemy.exc import OperationalError, SQLAlchemyError

from application.repositories.db_session import DatabaseSession
from config import get_env

logger.setLevel(logging.ERROR)
logger.addHandler(logging.StreamHandler())

database_url = get_env("DB_URL")

if database_url is None:
    raise ValueError("DB_URL environment variable is not set")

engine = create_engine(database_url)

def get_session() -> Generator[Session]:
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]

class DatabaseConnection(DatabaseSession):

    def __init__(self, session: SessionDep):
        self.session = session

    def select[T](self, model: type[T], params: dict[str, Any]) -> T | None:
        try:
            statement = select(model)
            for key, value in params.items():
                column = getattr(model, key)
                statement = statement.where(column == value)

            result = self.session.exec(statement).first()
            return result
        except AttributeError as e:
            raise BaseException(f'type {model.__name__} has no attribute {str(e)}')
    
    def execute_raw(self, sql_query: str, params: dict[str, Any] | None = None):
        statement = text(sql_query)
        result = self.session.execute(statement, params or {})
        self.session.commit()
        return result
    
    def insert[T](self, model: type[T], data: T) -> T | None:
        self.session.add(data)
        self.session.commit()
        self.session.refresh(data)
        return data

    def health_check(self):
        """
        Checks if the database connection is active and operational.
        """
        try:
            # Perform a simple, lightweight query
            # A common method is to select the number 1
            res = self.session.exec(select(1))
            return True
        except OperationalError as e:
            # Catches specific database operational errors (e.g., connection issues)
            logger.error(f"Database health check failed due to an error: {e}")
            return False
        except SQLAlchemyError as e:
            # Catches other potential SQLAlchemy errors
            logger.error(f"Database health check failed due to an error: {e}")
            return False
        except Exception as e:
            # Catches any other unexpected exceptions
            logger.error(f"An unexpected error occurred during the health check: {e}")
            return False
