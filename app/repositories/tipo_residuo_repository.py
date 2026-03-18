from app.repositories.base_repository import BaseRepository
from app.models.tipo_de_residuo import TipoDeResiduo

class TipoResiduoRepository(BaseRepository):
    def find_all(self) -> list[TipoDeResiduo]:
        rows = self._fetch("SELECT * FROM tipo_de_residuo ORDER BY nome_categoria")
        return [TipoDeResiduo(**r) for r in rows]

    def find_by_id(self, id_tipo: int) -> TipoDeResiduo | None:
        rows = self._fetch("SELECT * FROM tipo_de_residuo WHERE id_tipo = %s", (id_tipo,))
        return TipoDeResiduo(**rows[0]) if rows else None
