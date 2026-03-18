import streamlit as st
from app.repositories.evento_repository import EventoRepository
from app.services.validacao_service import ValidacaoService


def render_eventos():
    st.subheader("📅 Eventos de Reciclagem")
    usuario = st.session_state.get("usuario")
    if not usuario:
        st.warning("Faça login primeiro.")
        return

    evento_repo = EventoRepository()
    val_svc = ValidacaoService()

    tab1, tab2 = st.tabs(["🗓️ Eventos com vagas", "📋 Meus eventos"])

    with tab1:
        eventos = evento_repo.find_com_vagas()
        if not eventos:
            st.info("Nenhum evento com vagas disponíveis.")
        else:
            for ev in eventos:
                with st.expander(f"📌 {ev['titulo']} — {ev['nome_bairro']}"):
                    st.write(f"**Data:** {ev['data'].strftime('%d/%m/%Y %H:%M') if hasattr(ev['data'], 'strftime') else ev['data']}")
                    st.write(f"**Descrição:** {ev['descricao']}")
                    st.write(f"**Vagas restantes:** {ev['vagas_restantes']}")
                    inscrito = evento_repo.is_inscrito(usuario.id_usuario, ev["id_evento"])
                    if inscrito:
                        st.success("✅ Você já está inscrito.")
                    else:
                        if st.button(f"Inscrever-se", key=f"insc_{ev['id_evento']}"):
                            if not val_svc.verificar_vagas(ev["id_evento"]):
                                st.error("Evento lotado!")
                            else:
                                try:
                                    evento_repo.inscrever(usuario.id_usuario, ev["id_evento"])
                                    st.success("✅ Inscrição realizada!")
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"Erro: {e}")

    with tab2:
        meus = evento_repo.find_by_morador(usuario.id_usuario)
        if not meus:
            st.info("Você não está inscrito em nenhum evento.")
        else:
            import pandas as pd
            df = pd.DataFrame(meus)
            df["data"] = pd.to_datetime(df["data"]).dt.strftime("%d/%m/%Y %H:%M")
            df["presenca_confirmada"] = df["presenca_confirmada"].map({True: "✅ Confirmada", False: "⏳ Pendente"})
            df = df.rename(columns={
                "titulo": "Evento", "data": "Data", "nome_bairro": "Bairro",
                "presenca_confirmada": "Presença"
            })
            st.dataframe(df[["Evento", "Data", "Bairro", "Presença"]], use_container_width=True)
