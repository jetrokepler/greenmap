from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class Denuncia:
    descricao: str
    id_usuario_autor: int
    foto: bytes = None
    latitude: float = None
    longitude: float = None
    status: str = "pendente"
    data: datetime = None
    id_denuncia: int = field(default=-1)
