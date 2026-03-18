from dataclasses import dataclass
from datetime import datetime

@dataclass
class MoradorConquista:
    id_usuario: int
    id_conquista: int
    data_conquista: datetime = None