# greenmap ♻️

Sistema gamificado de gerenciamento de reciclagem e coleta de lixo.

**Stack:** Python · Streamlit · PostgreSQL · Docker  
**Disciplina:** Banco de Dados — UFCA 2026

---

## Como rodar o projeto

### Pré-requisitos

Você precisa ter instalado **apenas o Docker Desktop**.  
Baixe em: https://www.docker.com/products/docker-desktop/
---

### Passo a passo

**1. Clone o repositório**
```bash
git clone https://gitlab.com/seu-grupo/collector.git
cd collector
```

**2. Suba os contêineres**
```bash
// abra o Docker Desktop no pc, apenas para carregar

// no terminal:
docker compose up
```

Aguarde aparecer no terminal:
```
collector_app  | You can now view your Streamlit app in your browser.
collector_app  | Local URL: http://localhost:8501
```

**3. Abra no navegador**
```
http://localhost:8501
```

Pronto. A aplicação está rodando e o banco já foi criado com dados de teste.

---

### Comandos úteis do Docker

| O que fazer | Comando |
|---|---|
| Subir tudo | `docker compose up` |
| Subir em segundo plano | `docker compose up -d` |
| Ver os logs | `docker compose logs -f` |
| Parar tudo | `Ctrl+C` ou `docker compose down` |
| Resetar o banco (apaga dados) | `docker compose down -v` |
| Reconstruir após mudar requirements.txt | `docker compose up --build` |

---

### Estrutura do projeto

```
collector/
├── database/
│   ├── init.sql          # cria as tabelas (roda automático no Docker)
│   └── seed.sql          # insere dados de teste (roda automático no Docker)
├── app/
│   ├── main.py           # ponto de entrada do Streamlit
│   ├── db/
│   │   └── connection.py # conexão com o banco (Singleton)
│   ├── models/           # dataclasses — representação das tabelas
│   ├── repositories/     # SQL — acesso ao banco
│   ├── services/         # regras de negócio
│   └── views/            # interface Streamlit
│       ├── morador/      # dashboard e widgets do morador
│       └── gestor/       # dashboard e widgets do gestor
├── docker-compose.yml    # define os contêineres
├── Dockerfile            # define como montar o contêiner da app
├── requirements.txt      # dependências Python
└── .env.example          # template de variáveis de ambiente
```

---

## Decisões de Ajuste (TP1 → TP2)

> Esta seção documenta as mudanças feitas no modelo para o TP2.

### 1. Adição de `execute_returning` na DatabaseConnection
O psycopg3 precisa de tratamento explícito para `RETURNING` em INSERTs.
Adicionamos o método `execute_returning()` para capturar o `id` gerado pelo banco
após inserções em `usuario`, evitando uma segunda query de busca.

### 2. Status de Denuncia expandido
O MER original tinha apenas `pendente/resolvida`.
Adicionamos `em_analise` para representar o fluxo real de fiscalização.

### 3. CHECK constraints explícitos
O modelo lógico não especificava os valores válidos para campos `status`.
Adicionamos `CHECK (status IN (...))` em `ponto_de_coleta`, `registro_descarte`
e `denuncia` para garantir integridade no nível do banco.

### 4. Índices adicionais
Adicionamos índices em colunas frequentemente filtradas
(`id_bairro`, `status_validacao`, `id_usuario_morador`) para
melhorar performance das consultas de ranking e relatórios.

---

## Integrantes

| Nome | Responsabilidade principal |
|---|---|
| Jetro | Sprint 0 · setup · repos de Evento/Denuncia/Conquista |
| David | Models (dataclasses) |
| Carlos | Repos de Morador/Bairro/Gestor/Usuario · Services |
| Ângelo | Repos de Ponto/Registro/Tipo/Cooperativa |
| Luiz | UI · Dashboards Morador e Gestor |
