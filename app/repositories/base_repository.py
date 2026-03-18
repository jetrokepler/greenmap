from abc import ABC
from app.db.connection import DatabaseConnection

class BaseRepository(ABC):
    def __init__(self):
        self._db = DatabaseConnection.get_instance()

    def _fetch(self, sql: str, params: tuple = ()) -> list[dict]:
        return self._db.execute(sql, params)

    def _run(self, sql: str, params: tuple = ()) -> None:
        self._db.execute_dml(sql, params)

    def _run_returning(self, sql: str, params: tuple = ()) -> dict | None:
        return self._db.execute_returning(sql, params)
