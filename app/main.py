"""
app/main.py — Ponto de entrada da aplicação #1 Collector

Para rodar:
    Com Docker:    docker compose up
    Sem Docker:    streamlit run app/main.py
"""

import streamlit as st


def main():
    st.set_page_config(
        page_title="#1 Collector",
        page_icon="♻️",
        layout="wide"
    )

    st.title("greenmap ♻️")
    st.caption("Sistema gamificado de reciclagem")
    st.info("Sprint 0 concluída. Banco de dados conectado e pronto.")

    # testa a conexão com o banco
    if st.button("Testar conexão com o banco"):
        try:
            from app.db.connection import DatabaseConnection
            db = DatabaseConnection.get_instance()
            rows = db.execute("SELECT COUNT(*) AS total FROM usuario")
            st.success(f"✅ Conexão OK — {rows[0]['total']} usuários no banco")
        except Exception as e:
            st.error(f"❌ Erro: {e}")


if __name__ == "__main__":
    main()
