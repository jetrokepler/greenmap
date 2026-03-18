import streamlit as st
import pandas as pd
from app.repositories.denuncia_repository import DenunciaRepository


def render_denuncias_mgmt():
    st.subheader("🚨 Gestão de Denúncias")

    denuncia_repo = DenunciaRepository()

    tab1, tab2 = st.tabs(["📋 Todas as Denúncias", "🔍 Buscar por Bairro/Status"])

    with tab1:
        denuncias = denuncia_repo.find_all_with_autor()
        if not denuncias:
            st.info("Nenhuma denúncia registrada.")
        else:
            for d in denuncias:
                status_cor = {"pendente": "🟡", "em_analise": "🔵", "resolvida": "🟢"}
                emoji = status_cor.get(d["status"], "⚪")
                data_str = d["data"].strftime('%d/%m/%Y %H:%M') if hasattr(d["data"],'strftime') else str(d["data"])
                with st.expander(f"{emoji} #{d['id_denuncia']} — {data_str} | {d['nome_autor']}"):
                    st.write(f"**Descrição:** {d['descricao']}")
                    st.write(f"**Status:** {d['status']}")
                    if d.get("latitude"):
                        st.write(f"**Localização:** {d['latitude']}, {d['longitude']}")
                    novo = st.selectbox(
                        "Alterar status",
                        ["pendente", "em_analise", "resolvida"],
                        index=["pendente","em_analise","resolvida"].index(d["status"]),
                        key=f"dstatus_{d['id_denuncia']}"
                    )
                    if st.button("💾 Atualizar", key=f"dupd_{d['id_denuncia']}"):
                        try:
                            denuncia_repo.update_status(d["id_denuncia"], novo)
                            st.success("Status atualizado!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Erro: {e}")

    with tab2:
        from app.repositories.bairro_repository import BairroRepository
        bairro_repo = BairroRepository()
        bairros = bairro_repo.find_all()
        bairro_opts = {b.nome: b.id_bairro for b in bairros}
        col1, col2 = st.columns(2)
        with col1:
            bairro_sel = st.selectbox("Bairro", list(bairro_opts.keys()), key="dm_bairro")
        with col2:
            status_sel = st.selectbox("Status", ["pendente", "em_analise", "resolvida"], key="dm_status")
        if st.button("🔍 Buscar", key="btn_buscar_den"):
            try:
                results = denuncia_repo.find_by_bairro_status(bairro_opts[bairro_sel], status_sel)
                if results:
                    df = pd.DataFrame(results)
                    cols_show = [c for c in ["data","descricao","status","nome_autor"] if c in df.columns]
                    st.dataframe(df[cols_show], use_container_width=True)
                else:
                    st.info("Nenhuma denúncia encontrada.")
            except Exception as e:
                st.error(f"Erro: {e}")
