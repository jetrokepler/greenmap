-- ORDEM DE CRIAÇÃO:
--   Tabelas sem FK primeiro, depois as que dependem delas.
--   Isso evita erros de "tabela referenciada não existe".
-- ============================================================

-- garante que o script pode ser rodado mais de uma vez sem erro
-- DROP TABLE IF EXISTS em ordem reversa de dependência

DROP TABLE IF EXISTS ponto_de_coleta_tipo_de_residuo CASCADE;
DROP TABLE IF EXISTS morador_evento                  CASCADE;
DROP TABLE IF EXISTS morador_conquista               CASCADE;
DROP TABLE IF EXISTS registro_descarte               CASCADE;
DROP TABLE IF EXISTS denuncia                        CASCADE;
DROP TABLE IF EXISTS evento                          CASCADE;
DROP TABLE IF EXISTS ponto_de_coleta                 CASCADE;
DROP TABLE IF EXISTS tipo_de_residuo                 CASCADE;
DROP TABLE IF EXISTS cooperativa                     CASCADE;
DROP TABLE IF EXISTS conquista                       CASCADE;
DROP TABLE IF EXISTS morador                         CASCADE;
DROP TABLE IF EXISTS gestor                          CASCADE;
DROP TABLE IF EXISTS bairro                          CASCADE;
DROP TABLE IF EXISTS usuario                         CASCADE;

-- ============================================================
-- TABELA 1: usuario
-- Superclasse da especialização Morador/Gestor.
-- Todo usuário do sistema começa aqui.
-- ============================================================
CREATE TABLE usuario (
    id_usuario    SERIAL        PRIMARY KEY,
    nome          VARCHAR(150)  NOT NULL,
    email         VARCHAR(255)  NOT NULL UNIQUE,
    senha         VARCHAR(255)  NOT NULL,
    data_cadastro TIMESTAMP     NOT NULL DEFAULT NOW()
);

-- ============================================================
-- TABELA 2: gestor
-- Subtipo de usuario. Gerencia bairros e valida descartes.
-- id_usuario é PK e FK ao mesmo tempo (padrão de herança em BD).
-- ============================================================
CREATE TABLE gestor (
    id_usuario   INTEGER      PRIMARY KEY
                              REFERENCES usuario(id_usuario) ON DELETE CASCADE,
    matricula    INTEGER      NOT NULL UNIQUE,
    departamento VARCHAR(150) NOT NULL
);

-- ============================================================
-- TABELA 3: bairro
-- Criado ANTES de morador porque morador tem FK para bairro.
-- id_usuario_gestor pode ser NULL (bairro ainda sem gestor).
-- ============================================================
CREATE TABLE bairro (
    id_bairro          SERIAL       PRIMARY KEY,
    nome               VARCHAR(100) NOT NULL,
    zona               VARCHAR(50)  NOT NULL,
    populacao_estimada INTEGER      NOT NULL CHECK (populacao_estimada > 0),
    id_usuario_gestor  INTEGER      REFERENCES gestor(id_usuario) ON DELETE SET NULL
    -- ON DELETE SET NULL: se o gestor for removido, o bairro fica sem gestor
    -- (não é deletado junto)
);

-- ============================================================
-- TABELA 4: morador
-- Subtipo de usuario. Faz descartes e acumula pontos.
-- ============================================================
CREATE TABLE morador (
    id_usuario            INTEGER      PRIMARY KEY
                                       REFERENCES usuario(id_usuario) ON DELETE CASCADE,
    cpf                   VARCHAR(14)  NOT NULL UNIQUE,
    pontuacao_acumulada   INTEGER      NOT NULL DEFAULT 0
                                       CHECK (pontuacao_acumulada >= 0),
    endereco_residencial  VARCHAR(255),
    id_bairro             INTEGER      REFERENCES bairro(id_bairro) ON DELETE SET NULL
);

-- ============================================================
-- TABELA 5: tipo_de_residuo
-- Tabela de referência: categorias de resíduo e pontos por kg.
-- ============================================================
CREATE TABLE tipo_de_residuo (
    id_tipo        SERIAL       PRIMARY KEY,
    nome_categoria VARCHAR(100) NOT NULL UNIQUE,
    descricao      TEXT,
    pontos_por_kg  INTEGER      NOT NULL CHECK (pontos_por_kg > 0)
);

-- ============================================================
-- TABELA 6: cooperativa
-- Entidade que valida os registros de descarte.
-- ============================================================
CREATE TABLE cooperativa (
    id_cooperativa INTEGER      GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nome           VARCHAR(150) NOT NULL,
    cnpj           VARCHAR(18)  NOT NULL UNIQUE,
    area_atuacao   VARCHAR(150)
);

-- ============================================================
-- TABELA 7: conquista
-- Badges de gamificação. Existem antes de qualquer morador
-- desbloquear — por isso não têm FK para morador aqui.
-- ============================================================
CREATE TABLE conquista (
    id_conquista INTEGER      GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nome_badge   VARCHAR(100) NOT NULL UNIQUE,
    criterio     TEXT         NOT NULL,
    icone_url    VARCHAR(500)
);

-- ============================================================
-- TABELA 8: ponto_de_coleta
-- Ecopontos físicos georreferenciados.
-- ============================================================
CREATE TABLE ponto_de_coleta (
    id_ponto   SERIAL       PRIMARY KEY,
    nome_local VARCHAR(150) NOT NULL,
    latitude   DECIMAL(10,7) NOT NULL,
    longitude  DECIMAL(10,7) NOT NULL,
    status     VARCHAR(20)  NOT NULL DEFAULT 'ativo'
               CHECK (status IN ('ativo', 'manutencao', 'inativo')),
    endereco   VARCHAR(255),
    id_bairro  INTEGER      NOT NULL REFERENCES bairro(id_bairro) ON DELETE CASCADE
);

-- ============================================================
-- TABELA 9: evento
-- Mutirões de limpeza organizados por bairro.
-- ============================================================
CREATE TABLE evento (
    id_evento  SERIAL       PRIMARY KEY,
    titulo     VARCHAR(150) NOT NULL,
    data       TIMESTAMP    NOT NULL,
    descricao  TEXT,
    vagas      INTEGER      NOT NULL CHECK (vagas > 0),
    id_bairro  INTEGER      NOT NULL REFERENCES bairro(id_bairro) ON DELETE CASCADE
);

-- ============================================================
-- TABELA 10: registro_descarte
-- Entidade central: une Morador, PontoDeColeta, Tipo e Cooperativa.
-- ============================================================
CREATE TABLE registro_descarte (
    id_registro          SERIAL         PRIMARY KEY,
    pontos_concedidos    INTEGER        NOT NULL DEFAULT 0
                                        CHECK (pontos_concedidos >= 0),
    data                 TIMESTAMP      NOT NULL DEFAULT NOW(),
    peso_estimado        DECIMAL(8,2)   NOT NULL CHECK (peso_estimado > 0),
    status_validacao     VARCHAR(20)    NOT NULL DEFAULT 'pendente'
                                        CHECK (status_validacao IN ('pendente', 'aprovado', 'rejeitado')),
    foto_evidencia       BYTEA,
    data_validacao       TIMESTAMP,

    -- chaves estrangeiras
    id_usuario_morador   INTEGER        NOT NULL
                                        REFERENCES morador(id_usuario) ON DELETE CASCADE,
    id_ponto             INTEGER        NOT NULL
                                        REFERENCES ponto_de_coleta(id_ponto) ON DELETE CASCADE,
    id_tipo              INTEGER        NOT NULL
                                        REFERENCES tipo_de_residuo(id_tipo),
    id_cooperativa       INTEGER        REFERENCES cooperativa(id_cooperativa) ON DELETE SET NULL
    -- ON DELETE SET NULL: se a cooperativa for removida, o registro
    -- fica com id_cooperativa NULL (não é deletado)
);

-- ============================================================
-- TABELA 11: denuncia
-- Relatos de descarte irregular feitos por moradores.
-- ============================================================
CREATE TABLE denuncia (
    id_denuncia      SERIAL        PRIMARY KEY,
    data             TIMESTAMP     NOT NULL DEFAULT NOW(),
    descricao        TEXT          NOT NULL,
    foto             BYTEA,
    latitude         DECIMAL(10,7),
    longitude        DECIMAL(10,7),
    status           VARCHAR(20)   NOT NULL DEFAULT 'pendente'
                                   CHECK (status IN ('pendente', 'em_analise', 'resolvida')),
    id_usuario_autor INTEGER       NOT NULL
                                   REFERENCES usuario(id_usuario) ON DELETE CASCADE
);

-- ============================================================
-- TABELA 12 (N:N): morador_conquista
-- PK composta garante que um morador não desbloqueie
-- a mesma conquista duas vezes.
-- ============================================================
CREATE TABLE morador_conquista (
    id_usuario    INTEGER   NOT NULL REFERENCES morador(id_usuario) ON DELETE CASCADE,
    id_conquista  INTEGER   NOT NULL REFERENCES conquista(id_conquista) ON DELETE CASCADE,
    data_conquista TIMESTAMP NOT NULL DEFAULT NOW(),

    PRIMARY KEY (id_usuario, id_conquista)
    -- PK composta: a combinação (morador, conquista) é única
);

-- ============================================================
-- TABELA 13 (N:N): morador_evento
-- Inscrições de moradores em eventos.
-- presenca_confirmada é atualizado pelo gestor após o evento.
-- ============================================================
CREATE TABLE morador_evento (
    id_usuario          INTEGER   NOT NULL REFERENCES morador(id_usuario) ON DELETE CASCADE,
    id_evento           INTEGER   NOT NULL REFERENCES evento(id_evento) ON DELETE CASCADE,
    presenca_confirmada BOOLEAN   NOT NULL DEFAULT FALSE,
    data_inscricao      TIMESTAMP NOT NULL DEFAULT NOW(),

    PRIMARY KEY (id_usuario, id_evento)
);

-- ============================================================
-- TABELA 14 (N:N): ponto_de_coleta_tipo_de_residuo
-- Define quais tipos de resíduo cada ponto aceita.
-- ============================================================
CREATE TABLE ponto_de_coleta_tipo_de_residuo (
    id_ponto  INTEGER NOT NULL REFERENCES ponto_de_coleta(id_ponto) ON DELETE CASCADE,
    id_tipo   INTEGER NOT NULL REFERENCES tipo_de_residuo(id_tipo) ON DELETE CASCADE,

    PRIMARY KEY (id_ponto, id_tipo)
);

-- ============================================================
-- ÍNDICES (opcional mas recomendado para performance)
-- O banco já cria índices para PKs e UNIQUEs automaticamente.
-- Estes são para colunas muito consultadas que não são PK/UNIQUE.
-- ============================================================
CREATE INDEX idx_morador_bairro        ON morador(id_bairro);
CREATE INDEX idx_ponto_bairro          ON ponto_de_coleta(id_bairro);
CREATE INDEX idx_registro_morador      ON registro_descarte(id_usuario_morador);
CREATE INDEX idx_registro_status       ON registro_descarte(status_validacao);
CREATE INDEX idx_denuncia_status       ON denuncia(status);
CREATE INDEX idx_evento_bairro         ON evento(id_bairro);

-- ============================================================
-- FIM DO SCRIPT
-- ============================================================
-- Para verificar as tabelas criadas (rodar no psql ou DBeaver):
--   \dt                    → lista as tabelas
--   \d nome_da_tabela      → mostra colunas e constraints
-- ============================================================
