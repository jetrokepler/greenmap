import streamlit as st
from app.repositories.denuncia_repository import DenunciaRepository
from app.models.denuncia import Denuncia


def render_denuncias():
    st.subheader("🚨 Reportar Descarte Irregular")
    usuario = st.session_state.get("usuario")
    if not usuario:
        st.warning("Faça login primeiro.")
        return

    denuncia_repo = DenunciaRepository()

    with st.form("form_denuncia"):
        descricao = st.text_area("Descreva o problema", key="den_desc")
        col1, col2 = st.columns(2)
        with col1:
            lat = st.number_input("Latitude (opcional)", value=0.0, format="%.6f", key="den_lat")
        with col2:
            lon = st.number_input("Longitude (opcional)", value=0.0, format="%.6f", key="den_lon")
        foto = st.file_uploader("Foto (opcional)", type=["jpg","jpeg","png"], key="den_foto")
        submitted = st.form_submit_button("📤 Enviar Denúncia", type="primary")

    if submitted:
        if not descricao.strip():
            st.error("A descrição é obrigatória.")
        else:
            try:
                foto_bytes = foto.read() if foto else None
                denuncia = Denuncia(
                    descricao=descricao,
                    id_usuario_autor=usuario.id_usuario,
                    foto=foto_bytes,
                    latitude=lat if lat != 0.0 else None,
                    longitude=lon if lon != 0.0 else None,
                )
                denuncia_repo.save(denuncia)
                st.success("✅ Denúncia enviada com sucesso!")
            except Exception as e:
                st.error(f"Erro ao enviar denúncia: {e}")

    st.markdown("---")
    st.subheader("📋 Minhas Denúncias")
    try:
        minhas = denuncia_repo.find_by_autor(usuario.id_usuario)
        if not minhas:
            st.info("Você ainda não fez nenhuma denúncia.")
        else:
            import pandas as pd
            df = pd.DataFrame(minhas)
            df["data"] = pd.to_datetime(df["data"]).dt.strftime("%d/%m/%Y %H:%M")
            status_emoji = {"pendente": "⏳ Pendente", "em_analise": "🔍 Em análise", "resolvida": "✅ Resolvida"}
            df["status"] = df["status"].map(lambda s: status_emoji.get(s, s))
            df = df.rename(columns={"data": "Data", "descricao": "Descrição", "status": "Status"})
            st.dataframe(df[["Data", "Descrição", "Status"]], use_container_width=True)
    except Exception as e:
        st.error(f"Erro ao carregar denúncias: {e}")
