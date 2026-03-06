"""
Modelo de dados para a entidade Gestor.

Gestor é um subtipo de Usuario. Pode gerenciar N Bairros (1:N).
Acessa o PageGestor para validar descartes e gerar relatórios.

Tabela correspondente: gestor
PK/FK: id_usuario → usuario.id_usuario
UNIQUE: matricula
"""

from dataclasses import dataclass


@dataclass
class Gestor:
    """
    Representa um gestor público cadastrado no sistema.

    Attributes:
        id_usuario (int): PK e FK para usuario.id_usuario.
        matricula (int): número de matrícula funcional. UNIQUE no banco.
        departamento (str): nome do departamento/secretaria responsável.
    """

    id_usuario: int
    matricula: int
    departamento: str
