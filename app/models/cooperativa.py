from dataclasses import dataclass, field

@dataclass
class Cooperativa:
    nome: str
    cnpj: str
    area_atuacao: str = ""
    id_cooperativa: int = field(default=-1)
