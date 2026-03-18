import streamlit as st
from app.repositories.ponto_repository import PontoDeColetaRepository
from app.repositories.bairro_repository import BairroRepository
from app.repositories.tipo_residuo_repository import TipoResiduoRepository


def render_mapa():
    st.subheader("🗺️ Mapa de Ecopontos")

    ponto_repo = PontoDeColetaRepository()
    bairro_repo = BairroRepository()
    tipo_repo = TipoResiduoRepository()

    bairros = bairro_repo.find_all()
    tipos = tipo_repo.find_all()

    col1, col2 = st.columns(2)
    with col1:
        bairro_opts = {"Todos os bairros": None} | {b.nome: b.id_bairro for b in bairros}
        bairro_sel = st.selectbox("Filtrar por bairro", list(bairro_opts.keys()), key="mapa_bairro")
    with col2:
        tipo_opts = {"Todos os tipos": None} | {t.nome_categoria: t.id_tipo for t in tipos}
        tipo_sel = st.selectbox("Filtrar por tipo de resíduo", list(tipo_opts.keys()), key="mapa_tipo")

    id_bairro = bairro_opts[bairro_sel]
    id_tipo = tipo_opts[tipo_sel]

    if id_bairro and id_tipo:
        pontos = ponto_repo.find_by_bairro_tipo(id_bairro, id_tipo)
        st.caption(f"Ecopontos ativos em **{bairro_sel}** que aceitam **{tipo_sel}**")
    elif id_bairro:
        todos = ponto_repo.find_all()
        pontos = [p for p in todos if p["id_bairro"] == id_bairro]
    elif id_tipo:
        pontos = ponto_repo.find_by_tipo(id_tipo)
    else:
        pontos = ponto_repo.find_ativos()

    if not pontos:
        st.info("Nenhum ecoponto encontrado com os filtros selecionados.")
        return

    import pandas as pd
    df = pd.DataFrame(pontos)

    # Mapa
    if "latitude" in df.columns:
        map_df = df[["latitude", "longitude"]].rename(
            columns={"latitude": "lat", "longitude": "lon"}
        )
        map_df["lat"] = map_df["lat"].astype(float)
        map_df["lon"] = map_df["lon"].astype(float)
        st.map(map_df)

    # Tabela detalhada
    cols_show = [c for c in ["nome_local", "endereco", "status", "nome_bairro"] if c in df.columns]
    st.dataframe(df[cols_show] if cols_show else df, use_container_width=True)
