"""
Modelo de dados para a entidade Cooperativa.

Cooperativas são as organizações responsáveis por validar os
registros de descarte submetidos pelos Moradores.
Quando uma cooperativa aprova um RegistroDescarte, o
GamificacaoService credita os pontos ao Morador.

Tabela correspondente: cooperativa
PK: id_cooperativa (GENERATED ALWAYS AS IDENTITY)
UNIQUE: cnpj

Relacionamentos:
    - Valida N RegistrosDeDescarte (registro_descarte.id_cooperativa)
"""

from dataclasses import dataclass, field


@dataclass
class Cooperativa:
    """
    Representa uma cooperativa de reciclagem cadastrada no sistema.

    Attributes:
        nome (str): razão social da cooperativa.
        cnpj (str): CNPJ no formato '00.000.000/0000-00' ou sem formatação.
            Validado por ValidacaoService.validar_cnpj() antes do INSERT.
            UNIQUE no banco.
        area_atuacao (str | None): descrição da área geográfica ou tipo de
            resíduo com que a cooperativa trabalha. Pode ser None.
        id_cooperativa (int): PK gerada pelo banco (GENERATED ALWAYS AS IDENTITY).
            -1 antes do INSERT.
    """

    nome: str
    cnpj: str
    area_atuacao: str = None
    id_cooperativa: int = field(default=-1)
