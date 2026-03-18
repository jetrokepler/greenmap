import streamlit as st
import pandas as pd
from app.repositories.bairro_repository import BairroRepository
from app.services.gamificacao_service import GamificacaoService


def render_ranking():
    st.subheader("🏆 Ranking — Cidadão Sustentável")

    bairro_repo = BairroRepository()
    gamif_svc = GamificacaoService()
    bairros = bairro_repo.find_all()

    if not bairros:
        st.warning("Nenhum bairro cadastrado.")
        return

    bairro_opts = {b.nome: b.id_bairro for b in bairros}
    col1, col2 = st.columns([2, 1])
    with col1:
        bairro_sel = st.selectbox("Selecione o bairro", list(bairro_opts.keys()), key="rank_bairro")
    with col2:
        usar_periodo = st.toggle("Filtrar por período", key="rank_periodo")

    id_bairro = bairro_opts[bairro_sel]

    if usar_periodo:
        c1, c2 = st.columns(2)
        with c1:
            data_ini = st.date_input("Data inicial", key="rank_ini")
        with c2:
            data_fim = st.date_input("Data final", key="rank_fim")
        ranking = gamif_svc.get_ranking_periodo(
            id_bairro, str(data_ini), str(data_fim)
        )
        col_pts = "pontos_periodo"
        st.caption(f"Pontos acumulados entre {data_ini} e {data_fim}")
    else:
        ranking = gamif_svc.get_ranking(id_bairro)
        col_pts = "pontuacao_acumulada"

    if not ranking:
        st.info("Nenhum morador neste bairro ainda.")
        return

    # Pódio top 3
    medalhas = ["🥇", "🥈", "🥉"]
    cols = st.columns(min(3, len(ranking)))
    for i, (col, row) in enumerate(zip(cols, ranking[:3])):
        with col:
            st.metric(
                label=f"{medalhas[i]} {row['nome']}",
                value=f"{row[col_pts]} pts"
            )

    st.markdown("---")
    # Tabela completa
    df = pd.DataFrame(ranking)
    df.index = range(1, len(df) + 1)
    df.index.name = "Posição"
    df = df.rename(columns={"nome": "Morador", col_pts: "Pontos"})
    cols_show = [c for c in ["Morador", "Pontos"] if c in df.columns]
    st.dataframe(df[cols_show], use_container_width=True)
