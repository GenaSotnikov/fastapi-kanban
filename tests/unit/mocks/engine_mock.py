from src.application.repositories.db_session import DatabaseSession


class DatabaseConnectionMock(DatabaseSession):
    def __init__(self):
        self.data = {
            'User': [],
            'UserCredentials': []
        }
    
    def select(self, model: type, filters: dict) -> list | None:
        records = self.data.get(model.__name__, [])
        for key, value in filters.items():
            records = [record for record in records if getattr(record, key) == value]
        return records if records else None
    
    def insert(self, record):
        model_name = record.__class__.__name__
        if model_name not in self.data:
            self.data[model_name] = []
        self.data[model_name].append(record)
        return record
    
    def execute_raw(self, sql_query: str, params: dict | None = None):
        # This mock does not support raw SQL execution, but we can simulate some basic queries if needed
        raise NotImplementedError("Raw SQL execution is not implemented in the mock database connection")
    
    def clear(self):
        for key in self.data:
            self.data[key].clear()

db_mock = DatabaseConnectionMock()
