from app.repositories.registro_repository import RegistroDescarteRepository
from app.repositories.cooperativa_repository import CooperativaRepository
from app.repositories.bairro_repository import BairroRepository


class RelatorioService:
    def __init__(self):
        self._registro_repo = RegistroDescarteRepository()
        self._cooperativa_repo = CooperativaRepository()
        self._bairro_repo = BairroRepository()

    def total_por_tipo(self) -> list[dict]:
        """Q6 — total de kg por tipo de resíduo."""
        return self._registro_repo.total_por_tipo()

    def total_por_bairro(self) -> list[dict]:
        return self._registro_repo.total_por_bairro()

    def ranking_cooperativas(self) -> list[dict]:
        """Q8 — ranking de cooperativas por validações."""
        return self._cooperativa_repo.ranking_validacoes()
