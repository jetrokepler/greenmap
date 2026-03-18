"""
app/main.py — Ponto de entrada da aplicação GreenMap ♻️

Para rodar:
    Com Docker:    docker compose up
    Sem Docker:    streamlit run app/main.py
"""
import streamlit as st


def main():
    st.set_page_config(
        page_title="GreenMap ♻️",
        page_icon="♻️",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Injeta CSS customizado
    st.markdown("""
    <style>
    .stMetric { border: 1px solid #e0e0e0; border-radius: 8px; padding: 8px; }
    </style>
    """, unsafe_allow_html=True)

    if "usuario" not in st.session_state:
        from app.views.page_login import render_login
        render_login()
        return

    tipo = st.session_state.get("tipo")
    if tipo == "morador":
        from app.views.morador.dashboard_morador import render_dashboard_morador
        render_dashboard_morador()
    elif tipo == "gestor":
        from app.views.gestor.dashboard_gestor import render_dashboard_gestor
        render_dashboard_gestor()
    else:
        st.error("Perfil de usuário não reconhecido.")
        if st.button("Voltar ao login"):
            for k in list(st.session_state.keys()):
                del st.session_state[k]
            st.rerun()


if __name__ == "__main__":
    main()
