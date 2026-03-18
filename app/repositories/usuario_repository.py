from app.repositories.base_repository import BaseRepository
from app.models.usuario import Usuario

class UsuarioRepository(BaseRepository):
    def find_by_id(self, id_usuario: int) -> Usuario | None:
        rows = self._fetch("SELECT * FROM usuario WHERE id_usuario = %s", (id_usuario,))
        return Usuario(**rows[0]) if rows else None

    def find_by_email(self, email: str) -> Usuario | None:
        rows = self._fetch("SELECT * FROM usuario WHERE email = %s", (email,))
        return Usuario(**rows[0]) if rows else None

    def exists_email(self, email: str) -> bool:
        rows = self._fetch("SELECT 1 FROM usuario WHERE email = %s", (email,))
        return len(rows) > 0

    def save(self, usuario: Usuario) -> int:
        row = self._run_returning(
            "INSERT INTO usuario (nome, email, senha) VALUES (%s, %s, %s) RETURNING id_usuario",
            (usuario.nome, usuario.email, usuario.senha)
        )
        return row["id_usuario"] if row else -1

    def find_all(self) -> list[Usuario]:
        rows = self._fetch("SELECT * FROM usuario ORDER BY nome")
        return [Usuario(**r) for r in rows]
