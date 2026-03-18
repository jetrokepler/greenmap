from app.repositories.base_repository import BaseRepository
from app.models.bairro import Bairro

class BairroRepository(BaseRepository):
    def find_all(self) -> list[Bairro]:
        rows = self._fetch("SELECT * FROM bairro ORDER BY nome")
        return [Bairro(**r) for r in rows]

    def find_by_id(self, id_bairro: int) -> Bairro | None:
        rows = self._fetch("SELECT * FROM bairro WHERE id_bairro = %s", (id_bairro,))
        return Bairro(**rows[0]) if rows else None

    def save(self, bairro: Bairro) -> int:
        row = self._run_returning(
            """INSERT INTO bairro (nome, zona, populacao_estimada, id_usuario_gestor)
               VALUES (%s, %s, %s, %s) RETURNING id_bairro""",
            (bairro.nome, bairro.zona, bairro.populacao_estimada, bairro.id_usuario_gestor)
        )
        return row["id_bairro"] if row else -1
