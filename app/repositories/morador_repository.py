from app.repositories.base_repository import BaseRepository
from app.models.morador import Morador

class MoradorRepository(BaseRepository):
    def find_by_id(self, id_usuario: int) -> Morador | None:
        rows = self._fetch("SELECT * FROM morador WHERE id_usuario = %s", (id_usuario,))
        return Morador(**rows[0]) if rows else None

    def find_by_bairro(self, id_bairro: int) -> list[Morador]:
        rows = self._fetch(
            "SELECT * FROM morador WHERE id_bairro = %s ORDER BY pontuacao_acumulada DESC",
            (id_bairro,)
        )
        return [Morador(**r) for r in rows]

    def find_all(self) -> list[Morador]:
        rows = self._fetch("SELECT * FROM morador")
        return [Morador(**r) for r in rows]

    def save(self, morador: Morador) -> None:
        self._run(
            """INSERT INTO morador (id_usuario, cpf, pontuacao_acumulada, endereco_residencial, id_bairro)
               VALUES (%s, %s, %s, %s, %s)""",
            (morador.id_usuario, morador.cpf, morador.pontuacao_acumulada,
             morador.endereco_residencial, morador.id_bairro)
        )

    def update_pontuacao(self, id_usuario: int, pts: int) -> None:
        self._run(
            "UPDATE morador SET pontuacao_acumulada = pontuacao_acumulada + %s WHERE id_usuario = %s",
            (pts, id_usuario)
        )

    def update_bairro(self, id_usuario: int, id_bairro: int) -> None:
        self._run(
            "UPDATE morador SET id_bairro = %s WHERE id_usuario = %s",
            (id_bairro, id_usuario)
        )

    def get_ranking(self, id_bairro: int) -> list[dict]:
        return self._fetch(
            """SELECT u.nome, m.pontuacao_acumulada, m.id_usuario
               FROM morador m
               JOIN usuario u ON u.id_usuario = m.id_usuario
               WHERE m.id_bairro = %s
               ORDER BY m.pontuacao_acumulada DESC""",
            (id_bairro,)
        )

    def get_ranking_periodo(self, id_bairro: int, data_ini: str, data_fim: str) -> list[dict]:
        return self._fetch(
            """SELECT u.nome,
                      COALESCE(SUM(rd.pontos_concedidos), 0) AS pontos_periodo,
                      m.id_usuario
               FROM morador m
               JOIN usuario u ON u.id_usuario = m.id_usuario
               LEFT JOIN registro_descarte rd
                      ON rd.id_usuario_morador = m.id_usuario
                     AND rd.data BETWEEN %s AND %s
                     AND rd.status_validacao = 'aprovado'
               WHERE m.id_bairro = %s
               GROUP BY m.id_usuario, u.nome
               ORDER BY pontos_periodo DESC""",
            (data_ini, data_fim, id_bairro)
        )
