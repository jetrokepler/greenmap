-- Contém dados suficientes para demonstrar TODAS as consultas.


-- ────────────────────────────────────────
-- TIPOS DE RESÍDUO (referência)
-- ────────────────────────────────────────
INSERT INTO tipo_de_residuo (nome_categoria, descricao, pontos_por_kg) VALUES
    ('Reciclável',  'Papel, plástico, metal e vidro limpos', 10),
    ('Eletrônico',  'Celulares, computadores, pilhas e baterias', 25),
    ('Orgânico',    'Restos de alimentos e materiais biodegradáveis', 5),
    ('Perigoso',    'Tintas, solventes, produtos químicos domésticos', 30);

-- ────────────────────────────────────────
-- COOPERATIVAS
-- ────────────────────────────────────────
INSERT INTO cooperativa (nome, cnpj, area_atuacao) VALUES
    ('EcoVerde Cooperativa', '12.345.678/0001-90', 'Juazeiro do Norte - CE'),
    ('ReciclaJuá',           '98.765.432/0001-10', 'Região do Cariri - CE');

-- ────────────────────────────────────────
-- CONQUISTAS (badges de gamificação)
-- ────────────────────────────────────────
INSERT INTO conquista (nome_badge, criterio, icone_url) VALUES
    ('Primeiro Passo',   'Realize seu primeiro descarte', '/icons/primeiro_passo.png'),
    ('Coletor Prata',    'Acumule 500 pontos',            '/icons/prata.png'),
    ('Coletor Ouro',     'Acumule 1000 pontos',           '/icons/ouro.png'),
    ('Eco Guerreiro',    'Realize 10 descartes aprovados','/icons/guerreiro.png'),
    ('Denunciante Ativo','Envie 3 denúncias',             '/icons/denuncia.png');

-- ────────────────────────────────────────
-- USUÁRIOS — gestores (inserir usuario primeiro, depois gestor)
-- ────────────────────────────────────────
INSERT INTO usuario (nome, email, senha) VALUES
    ('David Alves',   'david@collector.com',  'hash_david_123'),
    ('Angelo Lima',   'angelo@collector.com', 'hash_angelo_123');
-- senhas são hashes — nunca salvar em texto puro
-- em produção: hashlib.sha256 ou bcrypt

INSERT INTO gestor (id_usuario, matricula, departamento) VALUES
    (1, 10421, 'Secretaria de Meio Ambiente'),
    (2, 20815, 'Secretaria de Infraestrutura');

-- ────────────────────────────────────────
-- BAIRROS (precisam de gestores criados acima)
-- ────────────────────────────────────────
INSERT INTO bairro (nome, zona, populacao_estimada, id_usuario_gestor) VALUES
    ('Centro',        'Central', 25000, 1),
    ('Pirajá',        'Norte',   18000, 1),
    ('João Cabral',   'Sul',     12000, 2),
    ('Lagoa Seca',    'Leste',   9500,  2),
    ('Tiradentes',    'Oeste',   7200,  NULL);
-- Tiradentes sem gestor — testa o caso de id_usuario_gestor NULL

-- ────────────────────────────────────────
-- USUÁRIOS — moradores
-- ────────────────────────────────────────
INSERT INTO usuario (nome, email, senha) VALUES
    ('Jetro Cavalcante', 'jetro@email.com',   'hash_jetro'),
    ('Carlos Rocha',     'carlos@email.com',  'hash_carlos'),
    ('Luiz Henrique',    'luiz@email.com',    'hash_luiz'),
    ('Ana Lima',         'ana@email.com',     'hash_ana'),
    ('Maria Santos',     'maria@email.com',   'hash_maria'),
    ('Pedro Ferreira',   'pedro@email.com',   'hash_pedro'),
    ('Júlia Oliveira',   'julia@email.com',   'hash_julia'),
    ('Rafael Costa',     'rafael@email.com',  'hash_rafael');
-- IDs gerados: 3 ao 10 (usuários 1 e 2 são os gestores)

INSERT INTO morador (id_usuario, cpf, pontuacao_acumulada, endereco_residencial, id_bairro) VALUES
    (3,  '111.222.333-44', 340,  'Rua das Flores, 10',    1), -- Centro
    (4,  '222.333.444-55', 180,  'Av. Principal, 55',     1), -- Centro
    (5,  '333.444.555-66', 520,  'Rua do Sol, 22',        2), -- Pirajá
    (6,  '444.555.666-77', 820,  'Rua Nova, 88',          2), -- Pirajá
    (7,  '555.666.777-88', 210,  'Av. Sul, 14',           3), -- João Cabral
    (8,  '666.777.888-99', 90,   'Rua Leste, 33',         4), -- Lagoa Seca
    (9,  '777.888.999-00', 450,  'Rua Oeste, 7',          4), -- Lagoa Seca
    (10, '888.999.000-11', 60,   'Av. Tiradentes, 100',   5); -- Tiradentes

-- ────────────────────────────────────────
-- PONTOS DE COLETA
-- ────────────────────────────────────────
INSERT INTO ponto_de_coleta (nome_local, latitude, longitude, status, endereco, id_bairro) VALUES
    ('Ecoponto Centro',      -7.2160, -39.3153, 'ativo',      'Praça do Centro, s/n',        1),
    ('Ecoponto Pirajá',      -7.2089, -39.3201, 'ativo',      'Rua do Pirajá, 200',          2),
    ('Ecoponto João Cabral', -7.2240, -39.3100, 'manutencao', 'Av. Sul, 500',                3),
    ('Ecoponto Lagoa Seca',  -7.2300, -39.3050, 'ativo',      'Rua da Lagoa, 45',            4),
    ('Ecoponto Tiradentes',  -7.2050, -39.3280, 'ativo',      'Av. Tiradentes, km 2',        5),
    ('Ecoponto Norte',       -7.2010, -39.3210, 'inativo',    'Rua Norte, 10',               2);
-- temos 1 em manutenção e 1 inativo para testar filtros de status

-- ────────────────────────────────────────
-- QUAIS TIPOS CADA PONTO ACEITA (N:N)
-- ────────────────────────────────────────
-- Ecoponto Centro (id=1): aceita reciclável e orgânico
INSERT INTO ponto_de_coleta_tipo_de_residuo VALUES (1, 1), (1, 3);

-- Ecoponto Pirajá (id=2): aceita tudo
INSERT INTO ponto_de_coleta_tipo_de_residuo VALUES (2, 1), (2, 2), (2, 3), (2, 4);

-- Ecoponto João Cabral (id=3): reciclável
INSERT INTO ponto_de_coleta_tipo_de_residuo VALUES (3, 1);

-- Ecoponto Lagoa Seca (id=4): eletrônico e perigoso
INSERT INTO ponto_de_coleta_tipo_de_residuo VALUES (4, 2), (4, 4);

-- Ecoponto Tiradentes (id=5): reciclável e eletrônico
INSERT INTO ponto_de_coleta_tipo_de_residuo VALUES (5, 1), (5, 2);

-- Ecoponto Norte (id=6): reciclável
INSERT INTO ponto_de_coleta_tipo_de_residuo VALUES (6, 1);

-- ────────────────────────────────────────
-- EVENTOS (mutirões de limpeza)
-- ────────────────────────────────────────
INSERT INTO evento (titulo, data, descricao, vagas, id_bairro) VALUES
    ('Mutirão Pirajá',    '2026-03-15 08:00:00', 'Limpeza coletiva no bairro Pirajá. Traga luvas!',       10, 2),
    ('Coleta Centro',     '2026-03-22 09:00:00', 'Coleta especial de eletrônicos no Centro.',              20, 1),
    ('Eco Lagoa Seca',    '2026-04-05 07:30:00', 'Mutirão de limpeza da margem da lagoa.',                15, 4),
    ('Evento Lotado',     '2026-04-10 08:00:00', 'Evento para testar validação de vagas — lotado.',        2, 3);

-- ────────────────────────────────────────
-- INSCRIÇÕES EM EVENTOS (N:N)
-- ────────────────────────────────────────
-- Mutirão Pirajá (id=1): Jetro(3), Carlos(4), Luiz(5)
INSERT INTO morador_evento (id_usuario, id_evento, presenca_confirmada) VALUES
    (3, 1, TRUE),   -- Jetro — já confirmado
    (4, 1, FALSE),
    (5, 1, FALSE);

-- Coleta Centro (id=2): Ana(6), Maria(7)
INSERT INTO morador_evento (id_usuario, id_evento) VALUES
    (6, 2),
    (7, 2);

-- Evento Lotado (id=4): 2 inscrições — igual ao limite de vagas
INSERT INTO morador_evento (id_usuario, id_evento) VALUES
    (8, 4),
    (9, 4);
-- este evento tem vagas=2 e já tem 2 inscritos
-- ValidacaoService.verificar_vagas() deve retornar False

-- ────────────────────────────────────────
-- REGISTROS DE DESCARTE
-- ────────────────────────────────────────
INSERT INTO registro_descarte
    (id_usuario_morador, id_ponto, id_tipo, peso_estimado,
     status_validacao, pontos_concedidos, id_cooperativa, data_validacao)
VALUES
    -- aprovados (têm pontos e cooperativa)
    (3,  1, 1, 2.5,  'aprovado',  25,  1, NOW() - INTERVAL '5 days'),
    (3,  2, 2, 1.0,  'aprovado',  25,  1, NOW() - INTERVAL '4 days'),
    (4,  1, 1, 3.0,  'aprovado',  30,  2, NOW() - INTERVAL '6 days'),
    (5,  2, 3, 5.0,  'aprovado',  25,  1, NOW() - INTERVAL '3 days'),
    (6,  2, 1, 8.5,  'aprovado',  85,  1, NOW() - INTERVAL '10 days'),
    (6,  2, 2, 2.0,  'aprovado',  50,  2, NOW() - INTERVAL '7 days'),
    (7,  4, 4, 0.5,  'aprovado',  15,  2, NOW() - INTERVAL '2 days'),
    (8,  4, 2, 1.5,  'aprovado',  37,  1, NOW() - INTERVAL '8 days'),
    (9,  5, 1, 4.0,  'aprovado',  40,  1, NOW() - INTERVAL '1 day'),
    (10, 5, 1, 1.0,  'aprovado',  10,  2, NOW() - INTERVAL '9 days'),

    -- pendentes (aguardando validação — sem cooperativa ainda)
    (3,  1, 3, 2.0,  'pendente',  0,   NULL, NULL),
    (5,  2, 1, 3.5,  'pendente',  0,   NULL, NULL),
    (6,  2, 4, 0.8,  'pendente',  0,   NULL, NULL),

    -- rejeitado (foto inadequada)
    (7,  3, 1, 1.0,  'rejeitado', 0,   1,    NOW() - INTERVAL '3 days');

-- ────────────────────────────────────────
-- DENÚNCIAS
-- ────────────────────────────────────────
INSERT INTO denuncia (descricao, latitude, longitude, status, id_usuario_autor) VALUES
    ('Lixo acumulado no terreno baldio da Rua das Flores', -7.2165, -39.3148, 'pendente',    3),
    ('Descarte irregular de entulho na calçada',           -7.2092, -39.3205, 'em_analise',  5),
    ('Lixão clandestino perto da lagoa',                   -7.2298, -39.3055, 'resolvida',   9),
    ('Móveis velhos descartados na via pública',           -7.2055, -39.3275, 'pendente',    10),
    ('Resíduos químicos em terreno próximo à escola',      -7.2170, -39.3130, 'pendente',    3);

-- ────────────────────────────────────────
-- CONQUISTAS DESBLOQUEADAS (N:N)
-- ────────────────────────────────────────
-- "Primeiro Passo" para quem tem ao menos 1 descarte
INSERT INTO morador_conquista (id_usuario, id_conquista) VALUES
    (3, 1), -- Jetro desbloqueou "Primeiro Passo"
    (4, 1), -- Carlos
    (5, 1), -- Luiz
    (6, 1), -- Ana
    (7, 1), -- Maria
    (8, 1), -- Pedro
    (9, 1), -- Júlia
    (10,1); -- Rafael

-- "Coletor Prata" para quem tem >= 500 pontos
INSERT INTO morador_conquista (id_usuario, id_conquista) VALUES
    (5, 2), -- Luiz (520 pts)
    (6, 2); -- Ana  (820 pts)

-- "Coletor Ouro" para quem tem >= 1000 pontos
-- ninguém ainda

-- ────────────────────────────────────────
-- VERIFICAÇÃO RÁPIDA (comentado — rodar manualmente se quiser)
-- ────────────────────────────────────────
-- SELECT COUNT(*) FROM usuario;              -- deve retornar 10
-- SELECT COUNT(*) FROM morador;             -- deve retornar 8
-- SELECT COUNT(*) FROM gestor;              -- deve retornar 2
-- SELECT COUNT(*) FROM registro_descarte;   -- deve retornar 14
-- SELECT COUNT(*) FROM morador_evento;      -- deve retornar 7

-- ============================================================
-- FIM DO SEED
-- ============================================================
