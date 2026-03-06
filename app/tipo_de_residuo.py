"""
Modelo de dados para TipoDeResiduo.

Tabela de referência que define categorias de resíduo e
quantos pontos cada kg daquele tipo vale no sistema de gamificação.

Tabela correspondente: tipo_de_residuo
PK: id_tipo (SERIAL)
UNIQUE: nome_categoria
CHECK: pontos_por_kg > 0
"""

from dataclasses import dataclass, field


@dataclass
class TipoDeResiduo:
    """
    Representa uma categoria de resíduo aceita pelo sistema.

    Exemplos de categorias: 'Reciclável', 'Eletrônico', 'Orgânico', 'Perigoso'.

    Attributes:
        nome_categoria (str): nome da categoria. UNIQUE no banco.
        descricao (str): descrição detalhada do que pode ser descartado.
        pontos_por_kg (int): pontos concedidos por kg entregue deste tipo.
            Usado por GamificacaoService.calcular_pontos().
            CHECK > 0 no banco.
        id_tipo (int): PK gerada pelo banco. -1 antes do INSERT.
    """

    nome_categoria: str
    descricao: str
    pontos_por_kg: int
    id_tipo: int = field(default=-1)
