from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class Usuario:
    nome: str
    email: str
    senha: str
    id_usuario: int = field(default=-1)
    data_cadastro: datetime = field(default=None)
