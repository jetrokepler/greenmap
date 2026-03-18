from app.repositories.base_repository import BaseRepository
from app.models.cooperativa import Cooperativa

class CooperativaRepository(BaseRepository):
    def find_all(self) -> list[Cooperativa]:
        rows = self._fetch("SELECT * FROM cooperativa ORDER BY nome")
        return [Cooperativa(**r) for r in rows]

    def find_by_id(self, id_cooperativa: int) -> Cooperativa | None:
        rows = self._fetch("SELECT * FROM cooperativa WHERE id_cooperativa = %s", (id_cooperativa,))
        return Cooperativa(**rows[0]) if rows else None

    def ranking_validacoes(self) -> list[dict]:
        return self._fetch(
            """SELECT c.nome,
                      COUNT(rd.id_registro) AS total_validacoes,
                      COALESCE(SUM(rd.peso_estimado), 0) AS total_kg
               FROM cooperativa c
               LEFT JOIN registro_descarte rd
                      ON rd.id_cooperativa = c.id_cooperativa
                     AND rd.status_validacao = 'aprovado'
               GROUP BY c.id_cooperativa, c.nome
               ORDER BY total_validacoes DESC"""
        )
