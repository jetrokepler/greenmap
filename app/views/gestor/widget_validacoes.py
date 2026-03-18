import streamlit as st
from app.repositories.registro_repository import RegistroDescarteRepository
from app.repositories.cooperativa_repository import CooperativaRepository
from app.services.gamificacao_service import GamificacaoService


def render_validacoes():
    st.subheader("✅ Validar Descartes")

    reg_repo = RegistroDescarteRepository()
    coop_repo = CooperativaRepository()
    gamif_svc = GamificacaoService()

    pendentes = reg_repo.find_pendentes()
    cooperativas = coop_repo.find_all()

    if not cooperativas:
        st.warning("Nenhuma cooperativa cadastrada.")
        return

    coop_opts = {c.nome: c.id_cooperativa for c in cooperativas}
    coop_sel = st.selectbox("Cooperativa validadora", list(coop_opts.keys()), key="val_coop")
    id_cooperativa = coop_opts[coop_sel]

    if not pendentes:
        st.success("🎉 Nenhum descarte pendente de validação!")
        return

    st.info(f"**{len(pendentes)}** descarte(s) aguardando validação.")

    for reg in pendentes:
        msg_key = f"msg_apr_{reg['id_registro']}"
        if msg_key in st.session_state:
            st.success(f"✅ Aprovado! {st.session_state.pop(msg_key)} pontos creditados.")
        with st.expander(
            f"📦 #{reg['id_registro']} — {reg['nome']} | {reg['nome_categoria']} | {reg['peso_estimado']} kg"
        ):
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                st.write(f"**Morador:** {reg['nome']}")
                st.write(f"**Tipo:** {reg['nome_categoria']}")
                st.write(f"**Peso:** {reg['peso_estimado']} kg")
                st.write(f"**Local:** {reg['nome_local']}")
                data_str = reg['data'].strftime('%d/%m/%Y %H:%M') if hasattr(reg['data'],'strftime') else str(reg['data'])
                st.write(f"**Data:** {data_str}")
            with col2:
                if st.button("✅ Aprovar", key=f"apr_{reg['id_registro']}", type="primary"):
                    try:
                        from app.db.connection import DatabaseConnection
                        db = DatabaseConnection.get_instance()
                        rows = db.execute(
                            "SELECT id_usuario_morador, id_tipo, peso_estimado FROM registro_descarte WHERE id_registro = %s",
                            (reg["id_registro"],)
                        )
                        if rows:
                            r = rows[0]
                            pts = gamif_svc.creditar_pontos(
                                r["id_usuario_morador"], reg["id_registro"],
                                r["id_tipo"], float(r["peso_estimado"])
                            )
                            reg_repo.update_validacao(reg["id_registro"], "aprovado", id_cooperativa)
                            st.session_state[f"msg_apr_{reg['id_registro']}"] = pts
                        st.rerun()
                    except Exception as e:
                        st.error(f"Erro: {e}")
            with col3:
                if st.button("❌ Rejeitar", key=f"rej_{reg['id_registro']}"):
                    try:
                        reg_repo.update_validacao(reg["id_registro"], "rejeitado", id_cooperativa)
                        st.warning("Registro rejeitado.")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Erro: {e}")
