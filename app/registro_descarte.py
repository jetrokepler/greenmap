"""
Modelo de dados para RegistroDescarte.

Entidade central do sistema — representa uma entrega de resíduo
feita por um Morador em um PontoDeColeta.

Após criado com status 'pendente', é validado por uma Cooperativa,
que atualiza status_validacao e data_validacao.
Quando aprovado, GamificacaoService credita pontos ao Morador.

Tabela correspondente: registro_descarte
PK: id_registro (SERIAL)
FK: id_usuario_morador → morador.id_usuario (composição — CASCADE DELETE)
FK: id_ponto → ponto_de_coleta.id_ponto (composição — CASCADE DELETE)
FK: id_tipo → tipo_de_residuo.id_tipo
FK: id_cooperativa → cooperativa.id_cooperativa (pode ser NULL antes da validação)
CHECK: peso_estimado > 0
CHECK: status_validacao IN ('pendente', 'aprovado', 'rejeitado')
"""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class RegistroDescarte:
    """
    Representa um registro de descarte de resíduo.

    Attributes:
        id_usuario_morador (int): FK para morador.id_usuario.
            Morador que realizou o descarte.
        id_ponto (int): FK para ponto_de_coleta.id_ponto.
            Ponto onde o descarte ocorreu.
        id_tipo (int): FK para tipo_de_residuo.id_tipo.
            Determina os pontos via pontos_por_kg.
        peso_estimado (float): peso em kg informado pelo morador.
            CHECK > 0. Validado por ValidacaoService.validar_peso().
        foto_evidencia (bytes | None): foto obrigatória para aprovação.
        status_validacao (str): 'pendente' ao criar; 'aprovado' ou 'rejeitado'
            pela cooperativa. CHECK no banco.
        pontos_concedidos (int): calculado por GamificacaoService.calcular_pontos()
            após aprovação. 0 enquanto pendente.
        id_cooperativa (int | None): FK para cooperativa.id_cooperativa.
            NULL até ser atribuído para validação.
        data (datetime): data/hora do registro. DEFAULT NOW() no banco.
        data_validacao (datetime | None): preenchida quando aprovado/rejeitado.
        id_registro (int): PK gerada pelo banco. -1 antes do INSERT.
    """

    id_usuario_morador: int
    id_ponto: int
    id_tipo: int
    peso_estimado: float
    foto_evidencia: bytes = None
    status_validacao: str = "pendente"
    pontos_concedidos: int = 0
    id_cooperativa: int = None
    data: datetime = None
    data_validacao: datetime = None
    id_registro: int = field(default=-1)
