"""
Modelo de dados para PontoDeColeta (Ecoponto).

Ponto físico georreferenciado onde moradores entregam resíduos.
Aceita N tipos de resíduo via tabela N:N ponto_de_coleta_tipo_de_residuo.

Tabela correspondente: ponto_de_coleta
PK: id_ponto (SERIAL)
FK: id_bairro → bairro.id_bairro
CHECK: status IN ('ativo', 'manutencao', 'inativo')
"""

from dataclasses import dataclass, field


@dataclass
class PontoDeColeta:
    """
    Representa um ponto de coleta (ecoponto) cadastrado no sistema.

    Attributes:
        nome_local (str): nome de referência (ex: "Ecoponto Pirajá").
        latitude (float): coordenada geográfica. Usado no mapa (US01).
        longitude (float): coordenada geográfica. Usado no mapa (US01).
        status (str): estado do ponto. Valores aceitos: 'ativo', 'manutencao',
            'inativo'. Validado por CHECK no banco.
        id_bairro (int): FK para bairro.id_bairro.
        endereco (str): endereço textual para exibição.
        id_ponto (int): PK gerada pelo banco. -1 antes do INSERT.
    """

    nome_local: str
    latitude: float
    longitude: float
    status: str
    id_bairro: int
    endereco: str = ""
    id_ponto: int = field(default=-1)
