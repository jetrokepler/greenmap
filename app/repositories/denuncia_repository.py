from app.repositories.base_repository import BaseRepository
from app.models.denuncia import Denuncia

class DenunciaRepository(BaseRepository):
    def save(self, denuncia: Denuncia) -> None:
        self._run(
            """INSERT INTO denuncia (descricao, foto, latitude, longitude, status, id_usuario_autor)
               VALUES (%s, %s, %s, %s, %s, %s)""",
            (denuncia.descricao, denuncia.foto, denuncia.latitude,
             denuncia.longitude, denuncia.status, denuncia.id_usuario_autor)
        )

    def find_by_autor(self, id_usuario: int) -> list[dict]:
        return self._fetch(
            "SELECT * FROM denuncia WHERE id_usuario_autor = %s ORDER BY data DESC",
            (id_usuario,)
        )

    def find_by_bairro_status(self, id_bairro: int, status: str) -> list[dict]:
        """Q4 — múltiplos parâmetros."""
        return self._fetch(
            """SELECT d.*, u.nome AS nome_autor
               FROM denuncia d
               JOIN usuario u ON u.id_usuario = d.id_usuario_autor
               JOIN morador m ON m.id_usuario = d.id_usuario_autor
               WHERE m.id_bairro = %s AND d.status = %s
               ORDER BY d.data DESC""",
            (id_bairro, status)
        )

    def find_pendentes(self) -> list[dict]:
        return self._fetch(
            """SELECT d.*, u.nome AS nome_autor
               FROM denuncia d
               JOIN usuario u ON u.id_usuario = d.id_usuario_autor
               WHERE d.status = 'pendente'
               ORDER BY d.data ASC"""
        )

    def find_all_with_autor(self) -> list[dict]:
        return self._fetch(
            """SELECT d.*, u.nome AS nome_autor
               FROM denuncia d
               JOIN usuario u ON u.id_usuario = d.id_usuario_autor
               ORDER BY d.data DESC"""
        )

    def update_status(self, id_denuncia: int, status: str) -> None:
        self._run(
            "UPDATE denuncia SET status = %s WHERE id_denuncia = %s",
            (status, id_denuncia)
        )
