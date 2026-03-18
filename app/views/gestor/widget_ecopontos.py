import streamlit as st
from app.repositories.ponto_repository import PontoDeColetaRepository
from app.repositories.bairro_repository import BairroRepository
from app.repositories.tipo_residuo_repository import TipoResiduoRepository
from app.models.ponto_de_coleta import PontoDeColeta


def render_ecopontos():
    st.subheader("📍 Gerenciar Ecopontos")

    ponto_repo = PontoDeColetaRepository()
    bairro_repo = BairroRepository()
    tipo_repo = TipoResiduoRepository()

    tab1, tab2 = st.tabs(["📋 Lista de Ecopontos", "➕ Adicionar Ecoponto"])

    with tab1:
        pontos = ponto_repo.find_all()
        if not pontos:
            st.info("Nenhum ecoponto cadastrado.")
        else:
            for p in pontos:
                status_cor = {"ativo": "🟢", "manutencao": "🟡", "inativo": "🔴"}
                emoji = status_cor.get(p["status"], "⚪")
                with st.expander(f"{emoji} {p['nome_local']} — {p.get('nome_bairro','')}"):
                    st.write(f"**Status atual:** {p['status']}")
                    st.write(f"**Endereço:** {p['endereco']}")
                    novo_status = st.selectbox(
                        "Alterar status",
                        ["ativo", "manutencao", "inativo"],
                        index=["ativo","manutencao","inativo"].index(p["status"]),
                        key=f"est_{p['id_ponto']}"
                    )
                    if st.button("💾 Salvar status", key=f"sav_{p['id_ponto']}"):
                        try:
                            ponto_repo.update_status(p["id_ponto"], novo_status)
                            st.success("Status atualizado!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Erro: {e}")

    with tab2:
        st.markdown("#### Cadastrar novo ecoponto")
        with st.form("form_ponto"):
            nome = st.text_input("Nome do local")
            endereco = st.text_input("Endereço")
            col1, col2 = st.columns(2)
            with col1:
                lat = st.number_input("Latitude", value=-7.2160, format="%.6f")
            with col2:
                lon = st.number_input("Longitude", value=-39.3153, format="%.6f")
            status_novo = st.selectbox("Status", ["ativo", "manutencao", "inativo"])
            bairros = bairro_repo.find_all()
            bairro_opts = {b.nome: b.id_bairro for b in bairros}
            bairro_sel = st.selectbox("Bairro", list(bairro_opts.keys()))
            tipos = tipo_repo.find_all()
            tipos_sel = st.multiselect("Tipos de resíduo aceitos", [t.nome_categoria for t in tipos])
            submitted = st.form_submit_button("➕ Cadastrar", type="primary")

        if submitted:
            if not nome:
                st.error("Nome obrigatório.")
            else:
                try:
                    ponto = PontoDeColeta(
                        nome_local=nome, latitude=lat, longitude=lon,
                        status=status_novo, endereco=endereco,
                        id_bairro=bairro_opts[bairro_sel]
                    )
                    id_ponto = ponto_repo.save(ponto)
                    tipos_map = {t.nome_categoria: t.id_tipo for t in tipos}
                    for nome_tipo in tipos_sel:
                        ponto_repo.add_tipo(id_ponto, tipos_map[nome_tipo])
                    st.success(f"✅ Ecoponto '{nome}' cadastrado!")
                except Exception as e:
                    st.error(f"Erro: {e}")
