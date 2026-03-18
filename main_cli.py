"""
main_cli.py — Interface CLI do GreenMap ♻️

Para rodar:
    python main_cli.py
"""
import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

from app.db.connection import DatabaseConnection


def banner():
    print("\n" + "="*50)
    print("       ♻️  GreenMap — Sistema de Reciclagem  ♻️")
    print("="*50)


def menu_principal():
    banner()
    print("\n[1] Login como Morador")
    print("[2] Login como Gestor")
    print("[0] Sair")
    return input("\nEscolha: ").strip()


def login(tipo_esperado: str):
    from app.repositories.usuario_repository import UsuarioRepository
    from app.repositories.morador_repository import MoradorRepository
    from app.repositories.gestor_repository import GestorRepository

    email = input("E-mail: ").strip()
    senha = input("Senha: ").strip()
    usuario_repo = UsuarioRepository()
    usuario = usuario_repo.find_by_email(email)
    if not usuario or usuario.senha != senha:
        print("❌ Credenciais inválidas.")
        return None, None

    if tipo_esperado == "morador":
        sub = MoradorRepository().find_by_id(usuario.id_usuario)
    else:
        sub = GestorRepository().find_by_id(usuario.id_usuario)

    if not sub:
        print(f"❌ Usuário não é um {tipo_esperado}.")
        return None, None

    print(f"✅ Bem-vindo(a), {usuario.nome}!")
    return usuario, sub


# ─── MENUS MORADOR ───────────────────────────────────────────

def menu_morador(usuario, morador):
    while True:
        print(f"\n─── Menu Morador: {usuario.nome} ({morador.pontuacao_acumulada} pts) ───")
        print("[1] Ver Mapa de Ecopontos")
        print("[2] Registrar Descarte")
        print("[3] Ver Ranking do Bairro")
        print("[4] Eventos disponíveis")
        print("[5] Minhas Conquistas")
        print("[6] Reportar Denúncia")
        print("[0] Sair")
        op = input("Escolha: ").strip()
        if op == "1":
            menu_mapa()
        elif op == "2":
            menu_descarte(usuario, morador)
            # Atualiza pontuação
            from app.repositories.morador_repository import MoradorRepository
            morador = MoradorRepository().find_by_id(usuario.id_usuario) or morador
        elif op == "3":
            menu_ranking(morador)
        elif op == "4":
            menu_eventos(usuario)
        elif op == "5":
            menu_conquistas(usuario)
        elif op == "6":
            menu_denuncias(usuario)
        elif op == "0":
            break
        else:
            print("Opção inválida.")


def menu_mapa():
    from app.repositories.ponto_repository import PontoDeColetaRepository
    from app.repositories.bairro_repository import BairroRepository
    from app.repositories.tipo_residuo_repository import TipoResiduoRepository

    print("\n─── Ecopontos ───")
    print("[1] Listar todos os ecopontos ativos")
    print("[2] Filtrar por bairro e tipo de resíduo  (Q2 — múltiplos parâmetros)")
    op = input("Escolha: ").strip()

    ponto_repo = PontoDeColetaRepository()
    if op == "1":
        pontos = ponto_repo.find_ativos()
        for p in pontos:
            print(f"  📍 {p['nome_local']} | {p.get('nome_bairro','')} | {p['status']}")
    elif op == "2":
        bairros = BairroRepository().find_all()
        for b in bairros:
            print(f"  [{b.id_bairro}] {b.nome}")
        id_b = int(input("ID do bairro: ").strip())
        tipos = TipoResiduoRepository().find_all()
        for t in tipos:
            print(f"  [{t.id_tipo}] {t.nome_categoria}")
        id_t = int(input("ID do tipo de resíduo: ").strip())
        pontos = ponto_repo.find_by_bairro_tipo(id_b, id_t)
        if pontos:
            for p in pontos:
                print(f"  📍 {p['nome_local']} | {p['endereco']}")
        else:
            print("  Nenhum ecoponto encontrado.")


def menu_descarte(usuario, morador):
    from app.repositories.ponto_repository import PontoDeColetaRepository
    from app.repositories.tipo_residuo_repository import TipoResiduoRepository
    from app.repositories.registro_repository import RegistroDescarteRepository
    from app.models.registro_descarte import RegistroDescarte
    from app.services.validacao_service import ValidacaoService
    from app.services.gamificacao_service import GamificacaoService

    print("\n─── Registrar Descarte ───")
    pontos = PontoDeColetaRepository().find_ativos()
    for p in pontos:
        print(f"  [{p['id_ponto']}] {p['nome_local']}")
    id_ponto = int(input("ID do ecoponto: ").strip())

    tipos = TipoResiduoRepository().find_all()
    for t in tipos:
        print(f"  [{t.id_tipo}] {t.nome_categoria} ({t.pontos_por_kg} pts/kg)")
    id_tipo = int(input("ID do tipo de resíduo: ").strip())

    peso = float(input("Peso estimado (kg): ").strip())
    if not ValidacaoService().validar_peso(peso):
        print("❌ Peso inválido.")
        return

    pts_previstos = GamificacaoService().calcular_pontos(peso, id_tipo)
    print(f"  🏆 Pontos previstos: {pts_previstos}")

    registro = RegistroDescarte(
        id_usuario_morador=usuario.id_usuario,
        id_ponto=id_ponto,
        id_tipo=id_tipo,
        peso_estimado=peso
    )
    RegistroDescarteRepository().save(registro)
    print("✅ Descarte registrado! Aguardando validação.")


def menu_ranking(morador):
    from app.repositories.bairro_repository import BairroRepository
    from app.services.gamificacao_service import GamificacaoService

    print("\n─── Ranking ───")
    print("[1] Ranking do meu bairro")
    print("[2] Ranking por bairro e período  (Q1b — múltiplos parâmetros)")
    op = input("Escolha: ").strip()

    gamif = GamificacaoService()
    if op == "1":
        if not morador.id_bairro:
            print("Você não está associado a nenhum bairro.")
            return
        ranking = gamif.get_ranking(morador.id_bairro)
        for i, r in enumerate(ranking, 1):
            print(f"  {i}. {r['nome']} — {r['pontuacao_acumulada']} pts")
    elif op == "2":
        bairros = BairroRepository().find_all()
        for b in bairros:
            print(f"  [{b.id_bairro}] {b.nome}")
        id_b = int(input("ID do bairro: ").strip())
        data_ini = input("Data inicial (YYYY-MM-DD): ").strip()
        data_fim = input("Data final (YYYY-MM-DD): ").strip()
        ranking = gamif.get_ranking_periodo(id_b, data_ini, data_fim)
        for i, r in enumerate(ranking, 1):
            print(f"  {i}. {r['nome']} — {r['pontos_periodo']} pts no período")


def menu_eventos(usuario):
    from app.repositories.evento_repository import EventoRepository
    from app.services.validacao_service import ValidacaoService

    print("\n─── Eventos ───")
    print("[1] Ver eventos com vagas  (Q5)")
    print("[2] Meus eventos")
    op = input("Escolha: ").strip()

    evento_repo = EventoRepository()
    if op == "1":
        eventos = evento_repo.find_com_vagas()
        if not eventos:
            print("  Nenhum evento com vagas.")
            return
        for ev in eventos:
            data_str = ev["data"].strftime("%d/%m/%Y") if hasattr(ev["data"],"strftime") else ev["data"]
            print(f"  [{ev['id_evento']}] {ev['titulo']} | {ev['nome_bairro']} | {data_str} | {ev['vagas_restantes']} vaga(s)")
        id_ev = input("ID do evento para inscrever-se (Enter para pular): ").strip()
        if id_ev:
            id_ev = int(id_ev)
            if not ValidacaoService().verificar_vagas(id_ev):
                print("❌ Evento lotado!")
            elif evento_repo.is_inscrito(usuario.id_usuario, id_ev):
                print("Você já está inscrito.")
            else:
                evento_repo.inscrever(usuario.id_usuario, id_ev)
                print("✅ Inscrição realizada!")
    elif op == "2":
        meus = evento_repo.find_by_morador(usuario.id_usuario)
        for ev in meus:
            data_str = ev["data"].strftime("%d/%m/%Y") if hasattr(ev["data"],"strftime") else ev["data"]
            pres = "✅" if ev["presenca_confirmada"] else "⏳"
            print(f"  {pres} {ev['titulo']} | {data_str}")


def menu_conquistas(usuario):
    from app.repositories.conquista_repository import ConquistaRepository

    print("\n─── Conquistas ───")
    conquista_repo = ConquistaRepository()
    todas = conquista_repo.find_all()
    minhas_ids = {c["id_conquista"] for c in conquista_repo.find_by_morador(usuario.id_usuario)}
    for c in todas:
        status = "🏅" if c.id_conquista in minhas_ids else "🔒"
        print(f"  {status} {c.nome_badge} — {c.criterio}")


def menu_denuncias(usuario):
    from app.repositories.denuncia_repository import DenunciaRepository
    from app.models.denuncia import Denuncia

    print("\n─── Denúncias ───")
    descricao = input("Descreva o problema: ").strip()
    if not descricao:
        print("Descrição obrigatória.")
        return
    denuncia = Denuncia(descricao=descricao, id_usuario_autor=usuario.id_usuario)
    DenunciaRepository().save(denuncia)
    print("✅ Denúncia enviada!")


# ─── MENUS GESTOR ────────────────────────────────────────────

def menu_gestor(usuario, gestor):
    while True:
        print(f"\n─── Menu Gestor: {usuario.nome} | {gestor.departamento} ───")
        print("[1] Validar descartes pendentes")
        print("[2] Relatórios ambientais")
        print("[3] Gerenciar ecopontos")
        print("[4] Gerenciar denúncias  (Q4 — múltiplos parâmetros)")
        print("[0] Sair")
        op = input("Escolha: ").strip()
        if op == "1":
            menu_validacoes()
        elif op == "2":
            menu_relatorios()
        elif op == "3":
            menu_ecopontos()
        elif op == "4":
            menu_denuncias_mgmt()
        elif op == "0":
            break
        else:
            print("Opção inválida.")


def menu_validacoes():
    from app.repositories.registro_repository import RegistroDescarteRepository
    from app.repositories.cooperativa_repository import CooperativaRepository
    from app.services.gamificacao_service import GamificacaoService
    from app.db.connection import DatabaseConnection

    print("\n─── Validar Descartes ───")
    reg_repo = RegistroDescarteRepository()
    pendentes = reg_repo.find_pendentes()
    if not pendentes:
        print("  Nenhum descarte pendente.")
        return

    cooperativas = CooperativaRepository().find_all()
    for c in cooperativas:
        print(f"  [{c.id_cooperativa}] {c.nome}")
    id_coop = int(input("Cooperativa validadora (ID): ").strip())

    for reg in pendentes:
        data_str = reg["data"].strftime("%d/%m/%Y") if hasattr(reg["data"],"strftime") else reg["data"]
        print(f"\n  #{reg['id_registro']} | {reg['nome']} | {reg['nome_categoria']} | {reg['peso_estimado']}kg | {data_str}")
        acao = input("  [a]provar / [r]ejeitar / [p]ular: ").strip().lower()
        if acao == "a":
            db = DatabaseConnection.get_instance()
            rows = db.execute(
                "SELECT id_usuario_morador, id_tipo, peso_estimado FROM registro_descarte WHERE id_registro = %s",
                (reg["id_registro"],)
            )
            if rows:
                r = rows[0]
                reg_repo.update_validacao(reg["id_registro"], "aprovado", id_coop)
                pts = GamificacaoService().creditar_pontos(
                    r["id_usuario_morador"], reg["id_registro"],
                    r["id_tipo"], float(r["peso_estimado"])
                )
                print(f"  ✅ Aprovado! {pts} pontos creditados.")
        elif acao == "r":
            reg_repo.update_validacao(reg["id_registro"], "rejeitado", id_coop)
            print("  ❌ Rejeitado.")


def menu_relatorios():
    from app.services.relatorio_service import RelatorioService

    print("\n─── Relatórios ───")
    print("[1] Total por tipo de resíduo  (Q6)")
    print("[2] Total por bairro")
    print("[3] Ranking de cooperativas  (Q8)")
    op = input("Escolha: ").strip()

    rel = RelatorioService()
    if op == "1":
        for r in rel.total_por_tipo():
            print(f"  {r['nome_categoria']}: {r['total_kg']:.2f} kg")
    elif op == "2":
        for r in rel.total_por_bairro():
            print(f"  {r['nome']}: {r['total_kg']:.2f} kg ({r['total_registros']} registros)")
    elif op == "3":
        for r in rel.ranking_cooperativas():
            print(f"  {r['nome']}: {r['total_validacoes']} validações | {r['total_kg']:.2f} kg")


def menu_ecopontos():
    from app.repositories.ponto_repository import PontoDeColetaRepository

    print("\n─── Ecopontos ───")
    print("[1] Listar todos")
    print("[2] Atualizar status")
    op = input("Escolha: ").strip()

    repo = PontoDeColetaRepository()
    if op == "1":
        for p in repo.find_all():
            print(f"  [{p['id_ponto']}] {p['nome_local']} | {p['status']}")
    elif op == "2":
        for p in repo.find_all():
            print(f"  [{p['id_ponto']}] {p['nome_local']} | {p['status']}")
        id_p = int(input("ID do ponto: ").strip())
        novo = input("Novo status (ativo/manutencao/inativo): ").strip()
        repo.update_status(id_p, novo)
        print("✅ Status atualizado.")


def menu_denuncias_mgmt():
    from app.repositories.denuncia_repository import DenunciaRepository
    from app.repositories.bairro_repository import BairroRepository

    print("\n─── Denúncias por Bairro e Status  (Q4) ───")
    bairros = BairroRepository().find_all()
    for b in bairros:
        print(f"  [{b.id_bairro}] {b.nome}")
    id_b = int(input("ID do bairro: ").strip())
    status = input("Status (pendente/em_analise/resolvida): ").strip()

    repo = DenunciaRepository()
    denuncias = repo.find_by_bairro_status(id_b, status)
    if not denuncias:
        print("  Nenhuma denúncia encontrada.")
        return
    for d in denuncias:
        data_str = d["data"].strftime("%d/%m/%Y") if hasattr(d["data"],"strftime") else d["data"]
        print(f"  #{d['id_denuncia']} | {data_str} | {d['nome_autor']} — {d['descricao'][:60]}")
    id_d = input("\nID para atualizar status (Enter para pular): ").strip()
    if id_d:
        novo = input("Novo status: ").strip()
        repo.update_status(int(id_d), novo)
        print("✅ Status atualizado.")


# ─── MAIN ────────────────────────────────────────────────────

def main():
    while True:
        op = menu_principal()
        if op == "1":
            usuario, morador = login("morador")
            if usuario and morador:
                menu_morador(usuario, morador)
        elif op == "2":
            usuario, gestor = login("gestor")
            if usuario and gestor:
                menu_gestor(usuario, gestor)
        elif op == "0":
            print("\nAté logo! ♻️")
            break
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    main()