from dataclasses import dataclass, field

@dataclass
class Conquista:
    nome_badge: str
    criterio: str
    icone_url: str = ""
    id_conquista: int = field(default=-1)
