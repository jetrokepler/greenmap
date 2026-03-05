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
import psycopg
import psycopg.rows
from dotenv import load_dotenv


class DatabaseConnection:
    """
    Conexão Singleton com o PostgreSQL.

    Uso em qualquer repositório:
        db = DatabaseConnection.get_instance()
        rows = db.execute("SELECT * FROM bairro WHERE id_bairro = %s", (1,))
    """

    # _instance guarda a única instância criada
    # começa como None — será preenchida na primeira chamada
    _instance = None

    def __init__(self):
        """
        Abre a conexão com o banco lendo as variáveis de ambiente.

        As variáveis vêm de duas fontes:
          - Rodando com Docker: definidas no docker-compose.yml
          - Rodando sem Docker: lidas do arquivo .env
        """
        # load_dotenv lê o arquivo .env se existir
        # se as variáveis já existirem (Docker), não sobrescreve
        load_dotenv()

        self._conn = psycopg.connect(
            host=os.getenv("DB_HOST", "localhost"),
            port=os.getenv("DB_PORT", "5432"),
            dbname=os.getenv("DB_NAME", "collector"),
            user=os.getenv("DB_USER", "collector_user"),
            password=os.getenv("DB_PASSWORD", "collector_pass"),
        )
        # autocommit=False significa que precisamos chamar commit()
        # manualmente após INSERT/UPDATE/DELETE
        # isso nos dá controle sobre quando salvar no banco
        self._conn.autocommit = False

    @classmethod
    def get_instance(cls) -> "DatabaseConnection":
        """
        Retorna a conexão existente ou cria uma nova se não existir.

        É um "classmethod" — pode ser chamado sem criar um objeto:
            db = DatabaseConnection.get_instance()  ← certo
            db = DatabaseConnection()               ← errado, não use

        Returns:
            DatabaseConnection: a instância única com conexão ativa.
        """
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def execute(self, sql: str, params: tuple = ()) -> list[dict]:
        """
        Roda um SELECT e devolve os resultados como lista de dicionários.

        Por que dicionários?
            Mais fácil de usar: linha["nome"] em vez de linha[0]

        Args:
            sql:    a query SQL, com %s onde vão os parâmetros
                    ex: "SELECT * FROM bairro WHERE zona = %s"
            params: tupla com os valores dos %s
                    ex: ("Norte",)
                    ATENÇÃO: sempre use %s e params — nunca junte
                    strings com f"...{valor}..." (vulnerável a SQL injection)

        Returns:
            lista de dicionários, um por linha retornada.
            Lista vazia se nenhuma linha encontrada.

        Exemplo:
            rows = db.execute(
                "SELECT * FROM morador WHERE id_bairro = %s",
                (2,)
            )
            for r in rows:
                print(r["cpf"], r["pontuacao_acumulada"])
        """
        with self._conn.cursor(row_factory=psycopg.rows.dict_row) as cur:
            cur.execute(sql, params)
            return cur.fetchall()

    def execute_dml(self, sql: str, params: tuple = ()) -> None:
        """
        Roda um INSERT, UPDATE ou DELETE e salva no banco (commit).

        O "try/except" garante que se algo der errado,
        o banco volta ao estado anterior (rollback) —
        nenhuma alteração parcial fica salva.

        Args:
            sql:    comando SQL com %s
            params: valores para os %s

        Raises:
            psycopg.Error: se violar uma constraint (ex: UNIQUE, FK)
                           ou qualquer outro erro de banco.
                           O erro é relançado para o repositório tratar.

        Exemplo:
            db.execute_dml(
                "UPDATE morador SET pontuacao_acumulada = pontuacao_acumulada + %s"
                " WHERE id_usuario = %s",
                (50, 3)
            )
        """
        try:
            with self._conn.cursor() as cur:
                cur.execute(sql, params)
            self._conn.commit()   # salva no banco
        except psycopg.Error:
            self._conn.rollback() # desfaz tudo em caso de erro
            raise                 # repassa o erro para quem chamou

    def execute_returning(self, sql: str, params: tuple = ()) -> dict | None:
        """
        Roda um INSERT com RETURNING e devolve a linha inserida.

        Usado quando precisamos do ID gerado pelo banco após um INSERT.

        Args:
            sql:    INSERT com cláusula RETURNING
                    ex: "INSERT INTO usuario (nome, email, senha)
                         VALUES (%s, %s, %s) RETURNING id_usuario"
            params: valores para os %s

        Returns:
            dicionário com as colunas do RETURNING, ou None se falhou.

        Exemplo:
            row = db.execute_returning(
                "INSERT INTO usuario (nome, email, senha) "
                "VALUES (%s, %s, %s) RETURNING id_usuario",
                ("Jetro", "jetro@email.com", "hash123")
            )
            id_gerado = row["id_usuario"]
        """
        try:
            with self._conn.cursor(row_factory=psycopg.rows.dict_row) as cur:
                cur.execute(sql, params)
                result = cur.fetchone()
            self._conn.commit()
            return result
        except psycopg.Error:
            self._conn.rollback()
            raise
