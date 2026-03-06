"""
Modelo de dados para a entidade Evento.

Eventos são mutirões de limpeza ou ações comunitárias organizadas
por um Gestor e vinculadas a um Bairro. Moradores podem se inscrever
via tabela N:N morador_evento (gerenciada por MoradorEvento).

Tabela correspondente: evento
PK: id_evento (SERIAL)
FK: id_bairro → bairro.id_bairro (CASCADE DELETE)
CHECK: vagas > 0

Relacionamentos:
    - Pertence a um Bairro (id_bairro → bairro.id_bairro)
    - Tem N Moradores inscritos via MoradorEvento (N:N)
"""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Evento:
    """
    Representa um evento comunitário vinculado a um bairro.

    Attributes:
        titulo (str): título do evento (ex: "Mutirão de Limpeza – Pirajá").
        data (datetime): data e hora do evento.
        vagas (int): número máximo de inscrições permitidas.
            CHECK > 0 no banco. Verificado por ValidacaoService.verificar_vagas()
            antes de cada inscrição.
        id_bairro (int): FK para bairro.id_bairro.
            Determina em qual bairro o evento ocorre.
        descricao (str | None): descrição detalhada do evento. Pode ser None.
        id_evento (int): PK gerada pelo banco. -1 antes do INSERT.
    """

    titulo: str
    data: datetime
    vagas: int
    id_bairro: int
    descricao: str = None
    id_evento: int = field(default=-1)
