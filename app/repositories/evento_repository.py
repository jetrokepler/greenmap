from app.repositories.base_repository import BaseRepository
from app.models.evento import Evento

class EventoRepository(BaseRepository):
    def find_all(self) -> list[dict]:
        return self._fetch(
            """SELECT e.*, b.nome AS nome_bairro
               FROM evento e
               JOIN bairro b ON b.id_bairro = e.id_bairro
               ORDER BY e.data ASC"""
        )

    def find_by_id(self, id_evento: int) -> dict | None:
        rows = self._fetch(
            """SELECT e.*, b.nome AS nome_bairro
               FROM evento e
               JOIN bairro b ON b.id_bairro = e.id_bairro
               WHERE e.id_evento = %s""",
            (id_evento,)
        )
        return rows[0] if rows else None

    def find_com_vagas(self) -> list[dict]:
        """Q5 — eventos com vagas disponíveis."""
        return self._fetch(
            """SELECT e.*, b.nome AS nome_bairro,
                      e.vagas - COALESCE(COUNT(me.id_usuario), 0) AS vagas_restantes
               FROM evento e
               JOIN bairro b ON b.id_bairro = e.id_bairro
               LEFT JOIN morador_evento me ON me.id_evento = e.id_evento
               GROUP BY e.id_evento, b.nome
               HAVING e.vagas > COUNT(me.id_usuario)
               ORDER BY e.data ASC"""
        )

    def count_inscritos(self, id_evento: int) -> int:
        rows = self._fetch(
            "SELECT COUNT(*) AS total FROM morador_evento WHERE id_evento = %s",
            (id_evento,)
        )
        return rows[0]["total"] if rows else 0

    def inscrever(self, id_usuario: int, id_evento: int) -> None:
        self._run(
            "INSERT INTO morador_evento (id_usuario, id_evento) VALUES (%s, %s)",
            (id_usuario, id_evento)
        )

    def is_inscrito(self, id_usuario: int, id_evento: int) -> bool:
        rows = self._fetch(
            "SELECT 1 FROM morador_evento WHERE id_usuario = %s AND id_evento = %s",
            (id_usuario, id_evento)
        )
        return len(rows) > 0

    def find_by_morador(self, id_usuario: int) -> list[dict]:
        return self._fetch(
            """SELECT e.titulo, e.data, e.descricao, me.presenca_confirmada, b.nome AS nome_bairro
               FROM morador_evento me
               JOIN evento e ON e.id_evento = me.id_evento
               JOIN bairro b ON b.id_bairro = e.id_bairro
               WHERE me.id_usuario = %s
               ORDER BY e.data ASC""",
            (id_usuario,)
        )

    def save(self, evento: Evento) -> None:
        self._run(
            """INSERT INTO evento (titulo, data, descricao, vagas, id_bairro)
               VALUES (%s, %s, %s, %s, %s)""",
            (evento.titulo, evento.data, evento.descricao, evento.vagas, evento.id_bairro)
        )
