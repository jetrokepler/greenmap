from dataclasses import dataclass, field

@dataclass
class PontoDeColeta:
    nome_local: str
    latitude: float
    longitude: float
    status: str
    id_bairro: int
    endereco: str = ""
    id_ponto: int = field(default=-1)
