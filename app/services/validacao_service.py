import re
from app.repositories.usuario_repository import UsuarioRepository
from app.repositories.evento_repository import EventoRepository


class ValidacaoService:
    def __init__(self):
        self._usuario_repo = UsuarioRepository()
        self._evento_repo = EventoRepository()

    def validar_cpf(self, cpf: str) -> bool:
        cpf = re.sub(r'\D', '', cpf)
        if len(cpf) != 11 or cpf == cpf[0] * 11:
            return False
        soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
        d1 = 0 if (soma * 10 % 11) >= 10 else (soma * 10 % 11)
        if d1 != int(cpf[9]):
            return False
        soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
        d2 = 0 if (soma * 10 % 11) >= 10 else (soma * 10 % 11)
        return d2 == int(cpf[10])

    def validar_cnpj(self, cnpj: str) -> bool:
        cnpj = re.sub(r'\D', '', cnpj)
        if len(cnpj) != 14 or cnpj == cnpj[0] * 14:
            return False
        pesos1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        pesos2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        soma = sum(int(cnpj[i]) * pesos1[i] for i in range(12))
        d1 = 0 if soma % 11 < 2 else 11 - soma % 11
        if d1 != int(cnpj[12]):
            return False
        soma = sum(int(cnpj[i]) * pesos2[i] for i in range(13))
        d2 = 0 if soma % 11 < 2 else 11 - soma % 11
        return d2 == int(cnpj[13])

    def verificar_vagas(self, id_evento: int) -> bool:
        evento = self._evento_repo.find_by_id(id_evento)
        if not evento:
            return False
        inscritos = self._evento_repo.count_inscritos(id_evento)
        return evento["vagas"] > inscritos

    def is_email_livre(self, email: str) -> bool:
        return not self._usuario_repo.exists_email(email)

    def validar_peso(self, peso: float) -> bool:
        return isinstance(peso, (int, float)) and peso > 0
