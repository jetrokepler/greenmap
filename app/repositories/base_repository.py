"""
Classe base abstrata para todos os repositórios.

Todos os repositórios herdam desta classe e ganham acesso aos três
métodos protegidos abaixo, que cobrem todos os cenários de SQL do projeto:

    _fetch          → SELECT   (retorna list[dict])
    _run            → INSERT / UPDATE / DELETE sem retorno
    _run_returning  → INSERT com RETURNING (retorna o dict da linha inserida)

Nenhuma subclasse deve importar DatabaseConnection diretamente —
o acesso ao banco passa sempre por esses três métodos.

Padrão: Repository Pattern
Princípio SOLID aplicado: nenhum SQL aparece fora da camada repository.
"""

from abc import ABC
from app.db.connection import DatabaseConnection


class BaseRepository(ABC):
    """
    Classe base abstrata para repositórios de acesso a dados.

    Injeta a DatabaseConnection singleton no atributo _db e expõe
    três métodos protegidos para as subclasses executarem SQL sem
    repetir código de conexão, commit ou rollback.

    Não deve ser instanciada diretamente — apenas herdada.

    Attributes:
        _db (DatabaseConnection): instância singleton da conexão com o banco.
                                  Obtida uma vez no __init__ e reutilizada.
    """

    def __init__(self):
        """
        Obtém a instância singleton da conexão com o banco.

        Todas as subclasses devem chamar super().__init__() no próprio
        __init__, ou simplesmente não declarar __init__ (Python herda
        automaticamente).

        Exemplo em subclasse:
            class BairroRepository(BaseRepository):
                pass  # __init__ herdado automaticamente
        """
        self._db = DatabaseConnection.get_instance()

    # ------------------------------------------------------------------
    # SELECT
    # ------------------------------------------------------------------

    def _fetch(self, sql: str, params: tuple = ()) -> list[dict]:
        """
        Executa uma query SELECT e retorna os resultados como lista de dicts.

        Delega para DatabaseConnection.execute(), que usa psycopg com
        row_factory=dict_row — cada linha vira um dicionário {coluna: valor}.

        Args:
            sql    (str):   query SELECT com placeholders %s.
                            Nunca concatene valores diretamente na string
                            (vulnerabilidade de SQL injection).
            params (tuple): valores que substituem os %s, na mesma ordem.
                            Default: tupla vazia (query sem parâmetros).

        Returns:
            list[dict]: uma lista com um dicionário por linha retornada.
                        Lista vazia [] se nenhuma linha for encontrada.

        Exemplos de uso em subclasse:

            # sem parâmetros
            def find_all(self) -> list[Bairro]:
                rows = self._fetch("SELECT * FROM bairro ORDER BY nome")
                return [Bairro(**r) for r in rows]

            # com um parâmetro
            def find_by_id(self, id_bairro: int) -> Bairro | None:
                rows = self._fetch(
                    "SELECT * FROM bairro WHERE id_bairro = %s",
                    (id_bairro,)          # ← vírgula obrigatória na tupla de 1 elemento
                )
                return Bairro(**rows[0]) if rows else None

            # com múltiplos parâmetros
            def find_by_bairro_tipo(self, id_bairro: int, id_tipo: int) -> list[dict]:
                return self._fetch(
                    \"\"\"
                    SELECT p.*
                    FROM ponto_de_coleta p
                    JOIN ponto_de_coleta_tipo_de_residuo pt ON pt.id_ponto = p.id_ponto
                    WHERE p.id_bairro = %s AND pt.id_tipo = %s AND p.status = 'ativo'
                    \"\"\",
                    (id_bairro, id_tipo)
                )
        """
        return self._db.execute(sql, params)

    # ------------------------------------------------------------------
    # INSERT / UPDATE / DELETE (sem retorno)
    # ------------------------------------------------------------------

    def _run(self, sql: str, params: tuple = ()) -> None:
        """
        Executa um comando DML (INSERT, UPDATE ou DELETE) com commit automático.

        Delega para DatabaseConnection.execute_dml(), que faz commit em caso
        de sucesso e rollback automático em caso de erro — nenhuma alteração
        parcial fica salva no banco.

        Args:
            sql    (str):   comando DML com placeholders %s.
            params (tuple): valores que substituem os %s.

        Returns:
            None

        Raises:
            psycopg.Error: propagado de DatabaseConnection se houver
                           violação de constraint (UNIQUE, FK, CHECK, NOT NULL)
                           ou qualquer outro erro de SQL.
                           A subclasse pode capturar para dar mensagem melhor,
                           ou deixar propagar até a camada de UI.

        Exemplos de uso em subclasse:

            # UPDATE
            def update_status(self, id_ponto: int, status: str) -> None:
                self._run(
                    "UPDATE ponto_de_coleta SET status = %s WHERE id_ponto = %s",
                    (status, id_ponto)
                )

            # UPDATE acumulativo
            def update_pontuacao(self, id_usuario: int, pts: int) -> None:
                self._run(
                    "UPDATE morador "
                    "SET pontuacao_acumulada = pontuacao_acumulada + %s "
                    "WHERE id_usuario = %s",
                    (pts, id_usuario)
                )

            # INSERT simples (quando não precisa do id gerado)
            def inscrever(self, id_usuario: int, id_evento: int) -> None:
                self._run(
                    "INSERT INTO morador_evento (id_usuario, id_evento) "
                    "VALUES (%s, %s)",
                    (id_usuario, id_evento)
                )
        """
        self._db.execute_dml(sql, params)

    # ------------------------------------------------------------------
    # INSERT com RETURNING (captura o id gerado pelo banco)
    # ------------------------------------------------------------------

    def _run_returning(self, sql: str, params: tuple = ()) -> dict | None:
        """
        Executa um INSERT com cláusula RETURNING e retorna a linha inserida.

        Delega para DatabaseConnection.execute_returning(), que faz commit
        em sucesso e rollback em erro — igual ao _run, mas devolve dados.

        Necessário quando o banco gera o valor da PK (SERIAL / BIGSERIAL)
        e a aplicação precisa desse valor imediatamente após o INSERT —
        por exemplo, para inserir em morador/gestor logo após inserir em usuario.

        Args:
            sql    (str):   INSERT com cláusula RETURNING ao final.
                            ex: "INSERT INTO usuario (...) VALUES (%s) RETURNING id_usuario"
            params (tuple): valores que substituem os %s.

        Returns:
            dict | None: dicionário com as colunas listadas no RETURNING,
                         ou None se o INSERT não retornou nenhuma linha
                         (situação inesperada — normalmente não ocorre).

        Raises:
            psycopg.Error: propagado de DatabaseConnection se houver
                           violação de constraint ou erro de SQL.

        Exemplo de uso em subclasse:

            def save(self, usuario: Usuario) -> int:
                \"\"\"Insere um novo usuário e retorna o id gerado pelo banco.\"\"\"
                row = self._run_returning(
                    \"\"\"
                    INSERT INTO usuario (nome, email, senha)
                    VALUES (%s, %s, %s)
                    RETURNING id_usuario
                    \"\"\",
                    (usuario.nome, usuario.email, usuario.senha)
                )
                return row["id_usuario"]   # int gerado pelo SERIAL do banco

        Por que não usar _run aqui?
            _run não retorna nada. Se usássemos _run para este INSERT,
            perderíamos o id_usuario gerado — e não conseguiríamos
            fazer o INSERT subsequente em morador ou gestor,
            que precisam desse id como FK.
        """
        return self._db.execute_returning(sql, params)