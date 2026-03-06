"""
Modelo de dados para a entidade Morador.

Morador é um subtipo de Usuario na especialização total e disjunta.
Compartilha id_usuario como PK e FK para a tabela usuario.

Tabela correspondente: morador
PK/FK: id_usuario → usuario.id_usuario
UNIQUE: cpf
CHECK: pontuacao_acumulada >= 0

Relacionamentos:
    - Pertence a um Bairro (id_bairro → bairro.id_bairro)
    - Realiza N RegistrosDeDescarte (composição)
    - Registra N Denuncias (composição)
    - Participa de N Eventos via MoradorEvento (N:N)
    - Desbloqueia N Conquistas via MoradorConquista (N:N)
"""

from dataclasses import dataclass, field


@dataclass
class Morador:
    """
    Representa um morador (cidadão) cadastrado no sistema.

    Para criar um Morador completo, é necessário primeiro inserir
    o Usuario pai e obter o id_usuario gerado pelo banco.

    Attributes:
        id_usuario (int): PK e FK para usuario.id_usuario.
            Deve ser obtido após INSERT em usuario.
        cpf (str): CPF no formato '000.000.000-00' ou '00000000000'.
            Validado por ValidacaoService.validar_cpf() antes do INSERT.
            UNIQUE no banco.
        pontuacao_acumulada (int): total de pontos acumulados por descartes.
            Atualizado por GamificacaoService.creditar_pontos().
            CHECK >= 0 no banco.
        endereco_residencial (str): endereço textual de moradia.
        id_bairro (int): FK para bairro.id_bairro.
            Determina o ranking ao qual o morador pertence.
    """

    id_usuario: int
    cpf: str
    pontuacao_acumulada: int = 0
    endereco_residencial: str = ""
    id_bairro: int = None
