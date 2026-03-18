import streamlit as st
from app.views.gestor.widget_validacoes import render_validacoes
from app.views.gestor.widget_relatorios import render_relatorios
from app.views.gestor.widget_ecopontos import render_ecopontos
from app.views.gestor.widget_denuncias_mgmt import render_denuncias_mgmt


def render_dashboard_gestor():
    usuario = st.session_state.get("usuario")
    gestor = st.session_state.get("gestor")

    with st.sidebar:
        st.markdown(f"### 🏛️ {usuario.nome}")
        st.markdown(f"*Gestor* — Depto: {gestor.departamento}")
        st.markdown("---")
        pagina = st.radio(
            "Navegação",
            ["✅ Validar Descartes", "📊 Relatórios",
             "📍 Ecopontos", "🚨 Denúncias"],
            key="nav_gestor"
        )
        st.markdown("---")
        if st.button("🚪 Sair"):
            for k in list(st.session_state.keys()):
                del st.session_state[k]
            st.rerun()

    if pagina == "✅ Validar Descartes":
        render_validacoes()
    elif pagina == "📊 Relatórios":
        render_relatorios()
    elif pagina == "📍 Ecopontos":
        render_ecopontos()
    elif pagina == "🚨 Denúncias":
        render_denuncias_mgmt()
