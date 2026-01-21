# Desafio MBA Engenharia de Software com IA - Full Cycle

Sistema RAG (Retrieval-Augmented Generation) para ingestao de PDF e busca semantica com LangChain.

## Pre-requisitos

- Docker e Docker Compose
- Python 3.10+
- API Key da OpenAI

## Configuracao

### 1. Clonar repositorio

```bash
git clone <seu-repo>
cd mba-ia-desafio-ingestao-busca
```

### 2. Criar ambiente virtual

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variaveis de ambiente

Copie `.env.example` para `.env` e preencha sua API key:

```bash
cp .env.example .env
```

Edite o `.env`:

```
OPENAI_API_KEY=sk-...
OPENAI_MODEL=text-embedding-3-small
PGVECTOR_URL=postgresql+psycopg://postgres:postgres@localhost:5432/rag
PGVECTOR_COLLECTION=document_collection
PDF_PATH=document.pdf
```

### 5. Subir banco de dados

```bash
docker compose up -d
```

## Execucao

### 1. Ingestao do PDF (executar 1 vez)

```bash
python src/ingest.py
```

### 2. Chat interativo

```bash
python src/chat.py
```

## Exemplo de Uso

```
Faca sua pergunta: Qual o faturamento da empresa?
PERGUNTA: Qual o faturamento da empresa?
RESPOSTA: O faturamento foi de 10 milhoes de reais.

Faca sua pergunta: Quantos clientes temos em 2024?
PERGUNTA: Quantos clientes temos em 2024?
RESPOSTA: Nao tenho informacoes necessarias para responder sua pergunta.
```

## Estrutura do Projeto

```
├── docker-compose.yml
├── requirements.txt
├── .env
├── src/
│   ├── ingest.py    # Ingestao do PDF
│   ├── search.py    # Funcao de busca (RetrievalQA Chain)
│   └── chat.py      # CLI interativo
├── document.pdf
└── README.md
```

## Tecnologias

- Python 3.10+
- LangChain (RetrievalQA Chain)
- OpenAI (text-embedding-3-small, gpt-4o-mini)
- PostgreSQL + pgVector
- Docker
