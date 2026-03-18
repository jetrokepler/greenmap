from app.repositories.base_repository import BaseRepository
from app.models.conquista import Conquista

class ConquistaRepository(BaseRepository):
    def find_all(self) -> list[Conquista]:
        rows = self._fetch("SELECT * FROM conquista ORDER BY id_conquista")
        return [Conquista(**r) for r in rows]

    def find_by_id(self, id_conquista: int) -> Conquista | None:
        rows = self._fetch("SELECT * FROM conquista WHERE id_conquista = %s", (id_conquista,))
        return Conquista(**rows[0]) if rows else None

    def find_by_morador(self, id_usuario: int) -> list[dict]:
        return self._fetch(
            """SELECT c.id_conquista, c.nome_badge, c.criterio, c.icone_url,
                      mc.data_conquista
               FROM morador_conquista mc
               JOIN conquista c ON c.id_conquista = mc.id_conquista
               WHERE mc.id_usuario = %s
               ORDER BY mc.data_conquista DESC""",
            (id_usuario,)
        )

    def count_by_morador(self, id_usuario: int) -> int:
        rows = self._fetch(
            "SELECT COUNT(*) AS total FROM morador_conquista WHERE id_usuario = %s",
            (id_usuario,)
        )
        return rows[0]["total"] if rows else 0

    def has_conquista(self, id_usuario: int, id_conquista: int) -> bool:
        rows = self._fetch(
            "SELECT 1 FROM morador_conquista WHERE id_usuario = %s AND id_conquista = %s",
            (id_usuario, id_conquista)
        )
        return len(rows) > 0

    def unlock(self, id_usuario: int, id_conquista: int) -> None:
        self._run(
            "INSERT INTO morador_conquista (id_usuario, id_conquista) VALUES (%s, %s) ON CONFLICT DO NOTHING",
            (id_usuario, id_conquista)
        )
