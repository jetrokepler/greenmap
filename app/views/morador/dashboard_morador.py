import streamlit as st
from app.views.morador.widget_mapa import render_mapa
from app.views.morador.widget_descarte import render_descarte
from app.views.morador.widget_ranking import render_ranking
from app.views.morador.widget_eventos import render_eventos
from app.views.morador.widget_conquistas import render_conquistas
from app.views.morador.widget_denuncias import render_denuncias


def render_dashboard_morador():
    usuario = st.session_state.get("usuario")
    morador = st.session_state.get("morador")

    with st.sidebar:
        st.markdown(f"### 👤 {usuario.nome}")
        st.markdown(f"🏆 **{morador.pontuacao_acumulada} pts**")
        st.markdown("---")
        pagina = st.radio(
            "Navegação",
            ["🗺️ Mapa de Ecopontos", "♻️ Registrar Descarte",
             "🏆 Ranking", "📅 Eventos", "🏅 Conquistas", "🚨 Denúncias"],
            key="nav_morador"
        )
        st.markdown("---")
        if st.button("🚪 Sair"):
            for k in list(st.session_state.keys()):
                del st.session_state[k]
            st.rerun()

    if pagina == "🗺️ Mapa de Ecopontos":
        render_mapa()
    elif pagina == "♻️ Registrar Descarte":
        render_descarte()
        # recarrega pontuação após possível descarte
        from app.repositories.morador_repository import MoradorRepository
        m = MoradorRepository().find_by_id(usuario.id_usuario)
        if m:
            st.session_state["morador"] = m
    elif pagina == "🏆 Ranking":
        render_ranking()
    elif pagina == "📅 Eventos":
        render_eventos()
    elif pagina == "🏅 Conquistas":
        render_conquistas()
    elif pagina == "🚨 Denúncias":
        render_denuncias()
