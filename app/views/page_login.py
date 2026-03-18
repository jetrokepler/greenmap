import streamlit as st
from app.repositories.usuario_repository import UsuarioRepository
from app.repositories.morador_repository import MoradorRepository
from app.repositories.gestor_repository import GestorRepository


def render_login():
    st.title("♻️ GreenMap — Sistema de Reciclagem")
    st.markdown("---")

    tab_login, tab_cadastro = st.tabs(["🔑 Entrar", "📝 Cadastrar-se"])

    with tab_login:
        _form_login()

    with tab_cadastro:
        _form_cadastro()


def _form_login():
    st.subheader("Acesse sua conta")
    email = st.text_input("E-mail", key="login_email")
    senha = st.text_input("Senha", type="password", key="login_senha")

    if st.button("Entrar", key="btn_login", type="primary"):
        if not email or not senha:
            st.error("Preencha e-mail e senha.")
            return
        try:
            usuario_repo = UsuarioRepository()
            morador_repo = MoradorRepository()
            gestor_repo = GestorRepository()

            usuario = usuario_repo.find_by_email(email)
            if not usuario or usuario.senha != senha:
                st.error("E-mail ou senha incorretos.")
                return

            morador = morador_repo.find_by_id(usuario.id_usuario)
            gestor = gestor_repo.find_by_id(usuario.id_usuario)

            st.session_state["usuario"] = usuario
            if morador:
                st.session_state["tipo"] = "morador"
                st.session_state["morador"] = morador
            elif gestor:
                st.session_state["tipo"] = "gestor"
                st.session_state["gestor"] = gestor
            else:
                st.error("Usuário sem perfil definido.")
                return
            st.rerun()
        except Exception as e:
            st.error(f"Erro ao conectar ao banco: {e}")


def _form_cadastro():
    from app.services.validacao_service import ValidacaoService
    from app.models.usuario import Usuario
    from app.models.morador import Morador
    from app.repositories.bairro_repository import BairroRepository

    st.subheader("Criar conta de Morador")
    nome = st.text_input("Nome completo", key="cad_nome")
    email = st.text_input("E-mail", key="cad_email")
    senha = st.text_input("Senha", type="password", key="cad_senha")
    cpf = st.text_input("CPF (somente números)", key="cad_cpf")
    endereco = st.text_input("Endereço residencial", key="cad_endereco")

    bairro_repo = BairroRepository()
    bairros = bairro_repo.find_all()
    bairro_opts = {b.nome: b.id_bairro for b in bairros}
    bairro_nome = st.selectbox("Bairro", list(bairro_opts.keys()), key="cad_bairro")

    if st.button("Cadastrar", key="btn_cadastrar", type="primary"):
        val = ValidacaoService()
        erros = []
        if not nome: erros.append("Nome obrigatório.")
        if not email: erros.append("E-mail obrigatório.")
        if not senha: erros.append("Senha obrigatória.")
        if email and not val.is_email_livre(email): erros.append("E-mail já cadastrado.")
        if not val.validar_cpf(cpf): erros.append("CPF inválido.")
        if erros:
            for e in erros:
                st.error(e)
            return
        try:
            usuario_repo = UsuarioRepository()
            morador_repo = MoradorRepository()
            usuario = Usuario(nome=nome, email=email, senha=senha)
            id_usuario = usuario_repo.save(usuario)
            morador = Morador(
                id_usuario=id_usuario, cpf=cpf,
                endereco_residencial=endereco,
                id_bairro=bairro_opts[bairro_nome]
            )
            morador_repo.save(morador)
            st.success("✅ Conta criada! Faça login.")
        except Exception as e:
            st.error(f"Erro ao cadastrar: {e}")
