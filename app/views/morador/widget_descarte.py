import streamlit as st
from app.repositories.ponto_repository import PontoDeColetaRepository
from app.repositories.tipo_residuo_repository import TipoResiduoRepository
from app.repositories.registro_repository import RegistroDescarteRepository
from app.models.registro_descarte import RegistroDescarte
from app.services.validacao_service import ValidacaoService
from app.services.gamificacao_service import GamificacaoService


def render_descarte():
    st.subheader("♻️ Registrar Descarte")
    usuario = st.session_state.get("usuario")
    if not usuario:
        st.warning("Faça login primeiro.")
        return

    ponto_repo = PontoDeColetaRepository()
    tipo_repo = TipoResiduoRepository()
    val_svc = ValidacaoService()
    gamif_svc = GamificacaoService()

    pontos_ativos = ponto_repo.find_ativos()
    tipos = tipo_repo.find_all()

    if not pontos_ativos:
        st.warning("Nenhum ecoponto ativo disponível no momento.")
        return

    col1, col2 = st.columns(2)
    with col1:
        ponto_opts = {p["nome_local"]: p["id_ponto"] for p in pontos_ativos}
        ponto_sel = st.selectbox("Ecoponto", list(ponto_opts.keys()), key="desc_ponto")
    with col2:
        tipo_opts = {t.nome_categoria: t for t in tipos}
        tipo_sel = st.selectbox("Tipo de resíduo", list(tipo_opts.keys()), key="desc_tipo")

    tipo_obj = tipo_opts[tipo_sel]
    peso = st.number_input("Peso estimado (kg)", min_value=0.1, step=0.1, key="desc_peso")

    if peso > 0:
        pontos_previstos = gamif_svc.calcular_pontos(peso, tipo_obj.id_tipo)
        st.info(f"🏆 Pontos previstos: **{pontos_previstos}** pts ({tipo_obj.pontos_por_kg} pts/kg)")

    foto = st.file_uploader("Foto de evidência (opcional)", type=["jpg","jpeg","png"], key="desc_foto")

    if st.button("📤 Registrar Descarte", type="primary", key="btn_descarte"):
        if not val_svc.validar_peso(peso):
            st.error("Peso deve ser maior que zero.")
            return
        try:
            foto_bytes = foto.read() if foto else None
            registro = RegistroDescarte(
                id_usuario_morador=usuario.id_usuario,
                id_ponto=ponto_opts[ponto_sel],
                id_tipo=tipo_obj.id_tipo,
                peso_estimado=peso,
                foto_evidencia=foto_bytes
            )
            reg_repo = RegistroDescarteRepository()
            reg_repo.save(registro)
            st.success("✅ Descarte registrado! Aguardando validação da cooperativa.")
        except Exception as e:
            st.error(f"Erro ao registrar: {e}")

    st.markdown("---")
    st.subheader("📋 Histórico de Descartes")
    try:
        reg_repo = RegistroDescarteRepository()
        historico = reg_repo.find_by_morador(usuario.id_usuario)
        if not historico:
            st.info("Nenhum descarte registrado ainda.")
        else:
            import pandas as pd
            df = pd.DataFrame(historico)
            df["data"] = pd.to_datetime(df["data"]).dt.strftime("%d/%m/%Y %H:%M")
            df = df.rename(columns={
                "data": "Data", "nome_categoria": "Tipo", "nome_local": "Ecoponto",
                "peso_estimado": "Peso (kg)", "status_validacao": "Status",
                "pontos_concedidos": "Pontos"
            })
            status_emoji = {"pendente": "⏳", "aprovado": "✅", "rejeitado": "❌"}
            df["Status"] = df["Status"].map(lambda s: f"{status_emoji.get(s,'')} {s}")
            st.dataframe(df, use_container_width=True)
    except Exception as e:
        st.error(f"Erro ao carregar histórico: {e}")
