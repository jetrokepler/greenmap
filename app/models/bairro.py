from dataclasses import dataclass, field

@dataclass
class Bairro:
    nome: str
    zona: str
    populacao_estimada: int
    id_usuario_gestor: int = None
    id_bairro: int = field(default=-1)
