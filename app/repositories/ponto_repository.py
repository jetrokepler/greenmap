from app.repositories.base_repository import BaseRepository
from app.models.ponto_de_coleta import PontoDeColeta

class PontoDeColetaRepository(BaseRepository):
    def find_all(self) -> list[dict]:
        return self._fetch(
            """SELECT pc.*, b.nome AS nome_bairro
               FROM ponto_de_coleta pc
               JOIN bairro b ON b.id_bairro = pc.id_bairro
               ORDER BY pc.nome_local"""
        )

    def find_ativos(self) -> list[dict]:
        return self._fetch(
            """SELECT pc.*, b.nome AS nome_bairro
               FROM ponto_de_coleta pc
               JOIN bairro b ON b.id_bairro = pc.id_bairro
               WHERE pc.status = 'ativo'
               ORDER BY pc.nome_local"""
        )

    def find_by_tipo(self, id_tipo: int) -> list[dict]:
        return self._fetch(
            """SELECT pc.id_ponto, pc.nome_local, pc.latitude, pc.longitude,
                      pc.status, pc.endereco, pc.id_bairro, b.nome AS nome_bairro
               FROM ponto_de_coleta pc
               JOIN ponto_de_coleta_tipo_de_residuo pt ON pt.id_ponto = pc.id_ponto
               JOIN bairro b ON b.id_bairro = pc.id_bairro
               WHERE pt.id_tipo = %s AND pc.status = 'ativo'""",
            (id_tipo,)
        )

    def find_by_bairro_tipo(self, id_bairro: int, id_tipo: int) -> list[dict]:
        """Q2 — múltiplos parâmetros obrigatória TP2."""
        return self._fetch(
            """SELECT pc.id_ponto, pc.nome_local, pc.latitude, pc.longitude,
                      pc.status, pc.endereco
               FROM ponto_de_coleta pc
               JOIN ponto_de_coleta_tipo_de_residuo pt ON pt.id_ponto = pc.id_ponto
               WHERE pc.id_bairro = %s AND pt.id_tipo = %s AND pc.status = 'ativo'""",
            (id_bairro, id_tipo)
        )

    def find_by_id(self, id_ponto: int) -> dict | None:
        rows = self._fetch(
            "SELECT * FROM ponto_de_coleta WHERE id_ponto = %s", (id_ponto,)
        )
        return rows[0] if rows else None

    def get_tipos(self, id_ponto: int) -> list[dict]:
        return self._fetch(
            """SELECT tr.id_tipo, tr.nome_categoria
               FROM ponto_de_coleta_tipo_de_residuo pt
               JOIN tipo_de_residuo tr ON tr.id_tipo = pt.id_tipo
               WHERE pt.id_ponto = %s""",
            (id_ponto,)
        )

    def save(self, ponto: PontoDeColeta) -> int:
        row = self._run_returning(
            """INSERT INTO ponto_de_coleta (nome_local, latitude, longitude, status, endereco, id_bairro)
               VALUES (%s, %s, %s, %s, %s, %s) RETURNING id_ponto""",
            (ponto.nome_local, ponto.latitude, ponto.longitude, ponto.status, ponto.endereco, ponto.id_bairro)
        )
        return row["id_ponto"] if row else -1

    def add_tipo(self, id_ponto: int, id_tipo: int) -> None:
        self._run(
            "INSERT INTO ponto_de_coleta_tipo_de_residuo (id_ponto, id_tipo) VALUES (%s, %s) ON CONFLICT DO NOTHING",
            (id_ponto, id_tipo)
        )

    def update_status(self, id_ponto: int, status: str) -> None:
        self._run(
            "UPDATE ponto_de_coleta SET status = %s WHERE id_ponto = %s",
            (status, id_ponto)
        )
