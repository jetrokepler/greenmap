from app.repositories.base_repository import BaseRepository
from app.models.registro_descarte import RegistroDescarte

class RegistroDescarteRepository(BaseRepository):
    def save(self, registro: RegistroDescarte) -> int:
        row = self._run_returning(
            """INSERT INTO registro_descarte
               (id_usuario_morador, id_ponto, id_tipo, peso_estimado, foto_evidencia, status_validacao, pontos_concedidos)
               VALUES (%s, %s, %s, %s, %s, 'pendente', 0)
               RETURNING id_registro""",
            (registro.id_usuario_morador, registro.id_ponto, registro.id_tipo,
             registro.peso_estimado, registro.foto_evidencia)
        )
        return row["id_registro"] if row else -1

    def count_aprovados_by_morador(self, id_usuario: int) -> int:
        rows = self._fetch(
            """SELECT COUNT(*) AS total FROM registro_descarte
               WHERE id_usuario_morador = %s AND status_validacao = 'aprovado'""",
            (id_usuario,)
        )
        return rows[0]["total"] if rows else 0

    def find_by_morador(self, id_usuario: int) -> list[dict]:
        """Q3 — histórico parametrizado."""
        return self._fetch(
            """SELECT rd.data, rd.peso_estimado, rd.status_validacao,
                      rd.pontos_concedidos, tr.nome_categoria, pc.nome_local
               FROM registro_descarte rd
               JOIN tipo_de_residuo tr ON tr.id_tipo = rd.id_tipo
               JOIN ponto_de_coleta pc ON pc.id_ponto = rd.id_ponto
               WHERE rd.id_usuario_morador = %s
               ORDER BY rd.data DESC""",
            (id_usuario,)
        )

    def find_pendentes(self) -> list[dict]:
        return self._fetch(
            """SELECT rd.id_registro, u.nome, tr.nome_categoria,
                      rd.peso_estimado, rd.data, rd.foto_evidencia, pc.nome_local
               FROM registro_descarte rd
               JOIN usuario u ON u.id_usuario = rd.id_usuario_morador
               JOIN tipo_de_residuo tr ON tr.id_tipo = rd.id_tipo
               JOIN ponto_de_coleta pc ON pc.id_ponto = rd.id_ponto
               WHERE rd.status_validacao = 'pendente'
               ORDER BY rd.data ASC"""
        )

    def update_validacao(self, id_registro: int, status: str, id_cooperativa: int) -> None:
        self._run(
            """UPDATE registro_descarte
               SET status_validacao = %s, data_validacao = NOW(), id_cooperativa = %s
               WHERE id_registro = %s""",
            (status, id_cooperativa, id_registro)
        )

    def update_pontos(self, id_registro: int, pontos: int) -> None:
        self._run(
            "UPDATE registro_descarte SET pontos_concedidos = %s WHERE id_registro = %s",
            (pontos, id_registro)
        )

    def total_por_tipo(self) -> list[dict]:
        """Q6."""
        return self._fetch(
            """SELECT tr.nome_categoria, SUM(rd.peso_estimado) AS total_kg
               FROM registro_descarte rd
               JOIN tipo_de_residuo tr ON tr.id_tipo = rd.id_tipo
               WHERE rd.status_validacao = 'aprovado'
               GROUP BY tr.nome_categoria
               ORDER BY total_kg DESC"""
        )

    def total_por_bairro(self) -> list[dict]:
        """Q8 complementar."""
        return self._fetch(
            """SELECT b.nome, SUM(rd.peso_estimado) AS total_kg,
                      COUNT(rd.id_registro) AS total_registros
               FROM registro_descarte rd
               JOIN ponto_de_coleta pc ON pc.id_ponto = rd.id_ponto
               JOIN bairro b ON b.id_bairro = pc.id_bairro
               WHERE rd.status_validacao = 'aprovado'
               GROUP BY b.nome
               ORDER BY total_kg DESC"""
        )