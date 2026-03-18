"""
app/db/connection.py — Conexão com o banco de dados

O QUE ESTE ARQUIVO FAZ:
    Cria e mantém UMA ÚNICA conexão com o PostgreSQL
    que é compartilhada por toda a aplicação.

POR QUE UMA SÓ CONEXÃO?
    Abrir e fechar conexões com banco é lento e pesado.
    O padrão "Singleton" garante que a conexão seja
    criada uma vez e reutilizada sempre.

COMO OS OUTROS ARQUIVOS USAM ISSO:
    from app.db.connection import DatabaseConnection

    db = DatabaseConnection.get_instance()
    linhas = db.execute("SELECT * FROM bairro")
"""

import os
import threading
import psycopg
import psycopg.rows
from dotenv import load_dotenv


class DatabaseConnection:
    _local = threading.local()

    def __init__(self):
        load_dotenv()
        self._conn = psycopg.connect(
            host=os.getenv("DB_HOST", "localhost"),
            port=os.getenv("DB_PORT", "5432"),
            dbname=os.getenv("DB_NAME", "collector"),
            user=os.getenv("DB_USER", "collector_user"),
            password=os.getenv("DB_PASSWORD", "collector_pass"),
        )
        self._conn.autocommit = False

    @classmethod
    def get_instance(cls) -> "DatabaseConnection":
        instance = getattr(cls._local, "instance", None)
        if instance is not None:
            try:
                with instance._conn.cursor() as cur:
                    cur.execute("SELECT 1")
            except Exception:
                instance = None
        if instance is None:
            cls._local.instance = cls()
        return cls._local.instance

    def execute(self, sql: str, params: tuple = ()) -> list[dict]:
        with self._conn.cursor(row_factory=psycopg.rows.dict_row) as cur:
            cur.execute(sql, params)
            return cur.fetchall()

    def execute_dml(self, sql: str, params: tuple = ()) -> None:
        try:
            with self._conn.cursor() as cur:
                cur.execute(sql, params)
            self._conn.commit()
        except psycopg.Error:
            self._conn.rollback()
            raise

    def execute_returning(self, sql: str, params: tuple = ()) -> dict | None:
        try:
            with self._conn.cursor(row_factory=psycopg.rows.dict_row) as cur:
                cur.execute(sql, params)
                result = cur.fetchone()
            self._conn.commit()
            return result
        except psycopg.Error:
            self._conn.rollback()
            raise