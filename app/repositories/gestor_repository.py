from app.repositories.base_repository import BaseRepository
from app.models.gestor import Gestor

class GestorRepository(BaseRepository):
    def find_by_id(self, id_usuario: int) -> Gestor | None:
        rows = self._fetch("SELECT * FROM gestor WHERE id_usuario = %s", (id_usuario,))
        return Gestor(**rows[0]) if rows else None

    def find_all(self) -> list[Gestor]:
        rows = self._fetch("SELECT * FROM gestor")
        return [Gestor(**r) for r in rows]

    def save(self, gestor: Gestor) -> None:
        self._run(
            "INSERT INTO gestor (id_usuario, matricula, departamento) VALUES (%s, %s, %s)",
            (gestor.id_usuario, gestor.matricula, gestor.departamento)
        )
