from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class MoradorEvento:
    id_usuario: int
    id_evento: int
    presenca_confirmada: bool = False
    data_inscricao: datetime = None
