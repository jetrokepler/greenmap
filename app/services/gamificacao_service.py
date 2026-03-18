from app.repositories.morador_repository import MoradorRepository
from app.repositories.conquista_repository import ConquistaRepository
from app.repositories.tipo_residuo_repository import TipoResiduoRepository
from app.repositories.registro_repository import RegistroDescarteRepository


class GamificacaoService:
    # Regras de conquistas: (id_conquista, tipo_criterio, valor_necessario)
    REGRAS = [
        (1, "descartes", 1),    # Primeiro Passo: 1 descarte
        (2, "pontos", 500),     # Coletor Prata: 500 pontos
        (3, "pontos", 1000),    # Coletor Ouro: 1000 pontos
        (4, "descartes", 10),   # Eco Guerreiro: 10 descartes
    ]

    def __init__(self):
        self._morador_repo = MoradorRepository()
        self._conquista_repo = ConquistaRepository()
        self._tipo_repo = TipoResiduoRepository()
        self._registro_repo = RegistroDescarteRepository()

    def calcular_pontos(self, peso: float, id_tipo: int) -> int:
        tipo = self._tipo_repo.find_by_id(id_tipo)
        if not tipo:
            return 1
        return max(1, round(peso * tipo.pontos_por_kg))

    def creditar_pontos(self, id_usuario: int, id_registro: int, id_tipo: int, peso: float) -> int:
        pontos = self.calcular_pontos(peso, id_tipo)
        self._morador_repo.update_pontuacao(id_usuario, pontos)
        self._registro_repo.update_pontos(id_registro, pontos)
        self.verificar_conquistas(id_usuario)
        return pontos

    def verificar_conquistas(self, id_usuario: int) -> list:
        morador = self._morador_repo.find_by_id(id_usuario)
        if not morador:
            return []
        descartes = len(self._registro_repo.find_by_morador(id_usuario))
        desbloqueadas = []
        for id_conquista, tipo, valor in self.REGRAS:
            if self._conquista_repo.has_conquista(id_usuario, id_conquista):
                continue
            if tipo == "pontos" and morador.pontuacao_acumulada >= valor:
                self._conquista_repo.unlock(id_usuario, id_conquista)
                desbloqueadas.append(id_conquista)
            elif tipo == "descartes" and descartes >= valor:
                self._conquista_repo.unlock(id_usuario, id_conquista)
                desbloqueadas.append(id_conquista)
        return desbloqueadas

    def get_ranking(self, id_bairro: int) -> list[dict]:
        return self._morador_repo.get_ranking(id_bairro)

    def get_ranking_periodo(self, id_bairro: int, data_ini: str, data_fim: str) -> list[dict]:
        return self._morador_repo.get_ranking_periodo(id_bairro, data_ini, data_fim)
