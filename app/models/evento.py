from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class Evento:
    titulo: str
    data: datetime
    vagas: int
    id_bairro: int
    descricao: str = ""
    id_evento: int = field(default=-1)
