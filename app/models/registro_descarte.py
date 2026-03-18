from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class RegistroDescarte:
    id_usuario_morador: int
    id_ponto: int
    id_tipo: int
    peso_estimado: float
    foto_evidencia: bytes = None
    status_validacao: str = "pendente"
    pontos_concedidos: int = 0
    id_cooperativa: int = None
    data: datetime = None
    data_validacao: datetime = None
    id_registro: int = field(default=-1)
