"""
Modelo de dados para a entidade Usuario.

Usuario é a superclasse da especialização total e disjunta
do sistema. Todo usuário é ou um Morador ou um Gestor — nunca
os dois ao mesmo tempo (garantido por ValidacaoService.is_disjunto()).

Tabela correspondente: usuario
PK: id_usuario (SERIAL)
UNIQUE: email
"""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Usuario:
    """
    Representa um usuário do sistema #1 Collector.

    Usado como superclasse de Morador e Gestor.
    A PK id_usuario é compartilhada como FK/PK nessas subclasses.

    Attributes:
        id_usuario (int): chave primária, gerada pelo banco (SERIAL).
            Valor -1 indica objeto ainda não persistido.
        nome (str): nome completo do usuário.
        email (str): e-mail único no sistema. Validado antes do INSERT.
        senha (str): hash da senha. NÃO armazenar senha em texto puro.
        data_cadastro (datetime): preenchida automaticamente pelo banco
            (DEFAULT NOW()). Pode ser None antes do INSERT.
    """

    nome: str
    email: str
    senha: str
    id_usuario: int = field(default=-1)
    data_cadastro: datetime = field(default=None)
