import streamlit as st
from app.repositories.conquista_repository import ConquistaRepository


def render_conquistas():
    st.subheader("🏅 Minhas Conquistas")
    usuario = st.session_state.get("usuario")
    if not usuario:
        st.warning("Faça login primeiro.")
        return

    conquista_repo = ConquistaRepository()
    todas = conquista_repo.find_all()
    minhas = conquista_repo.find_by_morador(usuario.id_usuario)
    ids_desbloqueadas = {c["id_conquista"] for c in minhas}

    cols = st.columns(3)
    for i, conquista in enumerate(todas):
        with cols[i % 3]:
            desbloqueada = conquista.id_conquista in ids_desbloqueadas
            if desbloqueada:
                st.success(f"🏅 **{conquista.nome_badge}**\n\n{conquista.criterio}")
            else:
                st.info(f"🔒 **{conquista.nome_badge}**\n\n{conquista.criterio}")
