from dataclasses import dataclass, field

@dataclass
class TipoDeResiduo:
    nome_categoria: str
    descricao: str
    pontos_por_kg: int
    id_tipo: int = field(default=-1)
