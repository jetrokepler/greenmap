"""
Modelo de dados para a entidade Bairro.

Bairro é a entidade geográfica central do sistema.
É usado como pivot para rankings, relatórios e filtragem de pontos.

Tabela correspondente: bairro
PK: id_bairro (SERIAL)
FK: id_usuario_gestor → gestor.id_usuario (pode ser NULL — bairro sem gestor)

Relacionamentos (agregação — partes existem independentemente):
    - Possui N Moradores (bairro.id_bairro → morador.id_bairro)
    - Contém N PontosDeColeta (bairro.id_bairro → ponto_de_coleta.id_bairro)
    - Sedia N Eventos (bairro.id_bairro → evento.id_bairro)
    - É gerenciado por 0 ou 1 Gestor
"""

from dataclasses import dataclass, field


@dataclass
class Bairro:
    """
    Representa um bairro da cidade no sistema.

    Attributes:
        nome (str): nome do bairro (ex: "Centro", "Pirajá").
        zona (str): zona geográfica (ex: "Norte", "Sul", "Leste").
        populacao_estimada (int): estimativa de habitantes. Usado em relatórios.
        id_usuario_gestor (int | None): FK para gestor.id_usuario.
            NULL se o bairro ainda não tiver gestor.
        id_bairro (int): PK gerada pelo banco. -1 antes do INSERT.
    """

    nome: str
    zona: str
    populacao_estimada: int
    id_usuario_gestor: int = None
    id_bairro: int = field(default=-1)
