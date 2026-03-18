import streamlit as st
import pandas as pd
from app.services.relatorio_service import RelatorioService
from app.repositories.bairro_repository import BairroRepository
from app.repositories.denuncia_repository import DenunciaRepository


def render_relatorios():
    st.subheader("📊 Relatórios Ambientais")

    rel_svc = RelatorioService()

    tab1, tab2, tab3, tab4 = st.tabs(
        ["Por Tipo de Resíduo", "Por Bairro", "Cooperativas", "Denúncias por Bairro"]
    )

    with tab1:
        st.markdown("#### Total coletado por tipo de resíduo")
        dados = rel_svc.total_por_tipo()
        if dados:
            df = pd.DataFrame(dados)
            df.columns = ["Tipo de Resíduo", "Total (kg)"]
            st.dataframe(df, use_container_width=True)
            st.bar_chart(df.set_index("Tipo de Resíduo"))
        else:
            st.info("Nenhum dado disponível.")

    with tab2:
        st.markdown("#### Total coletado por bairro")
        dados = rel_svc.total_por_bairro()
        if dados:
            df = pd.DataFrame(dados)
            df.columns = ["Bairro", "Total (kg)", "Registros"]
            st.dataframe(df, use_container_width=True)
            st.bar_chart(df.set_index("Bairro")["Total (kg)"])
        else:
            st.info("Nenhum dado disponível.")

    with tab3:
        st.markdown("#### Ranking de cooperativas por validações")
        dados = rel_svc.ranking_cooperativas()
        if dados:
            df = pd.DataFrame(dados)
            df.columns = ["Cooperativa", "Validações", "Total (kg)"]
            st.dataframe(df, use_container_width=True)
        else:
            st.info("Nenhum dado disponível.")

    with tab4:
        st.markdown("#### Denúncias por bairro e status")
        bairro_repo = BairroRepository()
        denuncia_repo = DenunciaRepository()
        bairros = bairro_repo.find_all()
        bairro_opts = {b.nome: b.id_bairro for b in bairros}

        col1, col2 = st.columns(2)
        with col1:
            bairro_sel = st.selectbox("Bairro", list(bairro_opts.keys()), key="rel_bairro")
        with col2:
            status_sel = st.selectbox(
                "Status", ["pendente", "em_analise", "resolvida"], key="rel_status"
            )
        try:
            dados = denuncia_repo.find_by_bairro_status(bairro_opts[bairro_sel], status_sel)
            if dados:
                df = pd.DataFrame(dados)
                cols_show = [c for c in ["data", "descricao", "status", "nome_autor"] if c in df.columns]
                st.dataframe(df[cols_show], use_container_width=True)
            else:
                st.info("Nenhuma denúncia encontrada com esses filtros.")
        except Exception as e:
            st.error(f"Erro: {e}")
