from dataclasses import dataclass

@dataclass
class Morador:
    id_usuario: int
    cpf: str
    pontuacao_acumulada: int = 0
    endereco_residencial: str = ""
    id_bairro: int = None