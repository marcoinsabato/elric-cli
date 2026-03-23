**ELRIC FRAMEWORK**

Low-Level Design & Implementation Plan

FastAPI · LangGraph · LangChain · LangSmith · PostgreSQL · Redis

| Versione | Data       | Stato |
| :------- | :--------- | :---- |
| 1.0.0    | 2026-03-19 | Draft |

# **1\. Overview & Obiettivi**

Elric è un framework backend opinionated per Python, ispirato all'architettura di Laravel, progettato per costruire applicazioni AI-first con FastAPI, LangGraph, LangChain e LangSmith. Il framework fornisce una CLI (uv run elric) per generare automaticamente tutti i componenti dell'applicazione, mantenendo una struttura coerente e production-ready.

### **Principi guida**

- Convention over configuration — struttura predefinita, zero configurazione manuale

- AI-first — agenti, chain e tool sono cittadini di prima classe

- Production-ready da subito — Docker multi-stage, logging JSON, error handling centralizzato

- Developer experience — CLI generativa, hot-reload in dev, rules Windsurf incluse

- Async nativo — tutto I/O-bound usa async/await, nessuna operazione bloccante

### **Stack tecnologico**

| Layer       | Tecnologia          | Ruolo                                    |
| :---------- | :------------------ | :--------------------------------------- |
| HTTP        | FastAPI             | Router, middleware, dependency injection |
| AI Agents   | LangGraph           | Grafi stateful per agenti multi-step     |
| AI Chains   | LangChain           | Chain, tools, prompt templates           |
| Tracing     | LangSmith           | Monitoring e debug delle run AI          |
| ORM         | SQLModel            | Modelli Pydantic \+ SQLAlchemy           |
| Migrations  | Alembic             | Versioning schema database               |
| Database    | PostgreSQL          | Database relazionale principale          |
| Cache/Queue | Redis               | Cache, rate limiting, job queue          |
| Auth        | API Key (X-API-Key) | Header-based, validazione via middleware |
| Logging     | structlog           | Log JSON strutturati con trace_id        |
| CLI         | Typer               | Generazione componenti stile Artisan     |
| Pkg Manager | uv                  | Dipendenze, virtualenv, scripts          |
| Container   | Docker              | Dev hot-reload \+ prod multi-stage       |

# **2\. Struttura delle Cartelle**

La struttura segue il pattern MVC di Laravel adattato al mondo AI. Ogni cartella ha una responsabilità singola e ben definita.

elric-app/

├── elric \# CLI entry point (chmod \+x)

├── pyproject.toml \# uv config, dipendenze, scripts

├── .env.example \# template variabili d'ambiente

├── .env \# variabili locali (gitignored)

│

├── .windsurf/ \# Windsurf AI rules & skills

│ ├── rules/

│ │ ├── 01-python-fastapi.md

│ │ ├── 02-agents-langchain.md

│ │ ├── 03-database-sqlmodel.md

│ │ ├── 04-docker-uv.md

│ │ └── 05-elric-conventions.md

│ └── skills/

│ ├── make-agent.md

│ ├── make-chain.md

│ ├── make-route.md

│ └── debug-langsmith.md

│

├── app/ \# Core applicativo

│ ├── \_\_init\_\_.py

│ ├── agents/ \# LangGraph agents

│ │ ├── \_\_init\_\_.py

│ │ └── base_agent.py \# Classe base astratta

│ ├── chains/ \# LangChain chains

│ │ ├── \_\_init\_\_.py

│ │ └── base_chain.py

│ ├── tools/ \# LangChain tools

│ │ ├── \_\_init\_\_.py

│ │ └── base_tool.py

│ ├── routes/ \# FastAPI routers

│ │ ├── \_\_init\_\_.py

│ │ └── health.py \# /health endpoint

│ ├── controllers/ \# Request handlers

│ │ └── \_\_init\_\_.py

│ ├── middleware/ \# FastAPI middleware

│ │ ├── \_\_init\_\_.py

│ │ ├── api_key.py \# Validazione X-API-Key

│ │ ├── rate_limit.py \# Rate limiting Redis-based

│ │ └── logging.py \# Request/response logging

│ ├── schemas/ \# Pydantic request/response

│ │ └── \_\_init\_\_.py

│ ├── providers/ \# Service providers

│ │ ├── \_\_init\_\_.py

│ │ ├── database.py \# SQLModel engine \+ session

│ │ ├── redis.py \# Redis client

│ │ └── langsmith.py \# LangSmith config

│ ├── exceptions/ \# Custom exceptions

│ │ ├── \_\_init\_\_.py

│ │ └── base.py \# ElricException base class

│ ├── jobs/ \# Background jobs

│ │ └── \_\_init\_\_.py

│ └── events/ \# Events & listeners

│ └── \_\_init\_\_.py

│

├── config/ \# Configurazione per ambiente

│ ├── \_\_init\_\_.py

│ └── settings.py \# Pydantic Settings

│

├── database/ \# Database layer

│ ├── models/ \# SQLModel entities

│ │ ├── \_\_init\_\_.py

│ │ └── api_key.py \# Modello ApiKey

│ ├── migrations/ \# Alembic migrations

│ │ ├── env.py

│ │ ├── script.py.mako

│ │ └── versions/

│ └── seeders/ \# Data seeders

│ └── \_\_init\_\_.py

│

├── tests/ \# Test suite

│ ├── conftest.py

│ ├── unit/

│ ├── integration/

│ └── e2e/

│

├── stubs/ \# Template per la CLI (Jinja2)

│ ├── agent.stub.py

│ ├── chain.stub.py

│ ├── tool.stub.py

│ ├── route.stub.py

│ ├── controller.stub.py

│ ├── schema.stub.py

│ ├── model.stub.py

│ ├── migration.stub.py

│ ├── job.stub.py

│ ├── event.stub.py

│ ├── listener.stub.py

│ ├── middleware.stub.py

│ ├── exception.stub.py

│ └── test.stub.py

│

├── elric_cli/ \# Codice della CLI

│ ├── \_\_init\_\_.py

│ ├── app.py \# Typer app entry point

│ └── commands/ \# Un file per gruppo comandi

│ ├── make.py \# make:\* commands

│ ├── migrate.py \# migrate:\* commands

│ ├── serve.py \# serve command

│ ├── route.py \# route:list

│ └── apikey.py \# apikey:\* commands

│

└── docker/

    ├── Dockerfile.dev

    ├── Dockerfile.prod

    ├── nginx.conf

    ├── docker-compose.yml         \# Dev

    └── docker-compose.prod.yml    \# Production

# **3\. Componenti Core — Low-Level Design**

## **3.1 CLI — elric_cli/**

La CLI è costruita con Typer e organizzata in gruppi di comandi. L'entry point è il file elric nella root del progetto.

### **Entry point (elric)**

\#\!/usr/bin/env python

import sys

from elric_cli.app import app

if \_\_name\_\_ \== "\_\_main\_\_":

    app()

### **Architettura CLI (elric_cli/app.py)**

import typer

from elric_cli.commands import make, migrate, serve, route, apikey

app \= typer.Typer(name="elric", help="Elric Framework CLI")

app.add_typer(make.app, name="make")

app.add_typer(migrate.app, name="migrate")

app.add_typer(route.app, name="route")

app.add_typer(apikey.app, name="apikey")

app.command()(serve.serve)

### **Comandi disponibili**

| Comando                  | Output                        | Descrizione              |
| :----------------------- | :---------------------------- | :----------------------- |
| make:agent NomeAgent     | app/agents/nome_agent.py      | LangGraph agent da stub  |
| make:chain NomeChain     | app/chains/nome_chain.py      | LangChain chain da stub  |
| make:tool NomeTool       | app/tools/nome_tool.py        | LangChain tool da stub   |
| make:route NomeRoute     | app/routes/nome_route.py      | FastAPI router da stub   |
| make:controller NomeCtrl | app/controllers/nome_ctrl.py  | Controller da stub       |
| make:schema NomeSchema   | app/schemas/nome_schema.py    | Pydantic schema da stub  |
| make:model NomeModel     | database/models/nome_model.py | SQLModel entity da stub  |
| make:migration desc      | database/migrations/versions/ | Alembic migration        |
| make:job NomeJob         | app/jobs/nome_job.py          | Background job da stub   |
| make:exception NomeEx    | app/exceptions/nome_ex.py     | Custom exception da stub |
| make:test NomeTest       | tests/unit/test_nome.py       | Test file da stub        |
| migrate                  | —                             | alembic upgrade head     |
| migrate:rollback         | —                             | alembic downgrade \-1    |
| migrate:fresh            | —                             | Drop tutto \+ re-migra   |
| migrate:status           | —                             | alembic current          |
| serve                    | —                             | uvicorn con hot-reload   |
| route:list               | —                             | Lista tutte le routes    |
| apikey:create            | elk_live_xxxxx                | Genera nuova API key     |
| apikey:list              | —                             | Lista key attive         |
| apikey:revoke \<id\>     | —                             | Revoca una key           |

### **Meccanismo di generazione da stub**

Ogni comando make:\* legge lo stub corrispondente in stubs/, sostituisce i placeholder con Jinja2 e scrive il file nella cartella target. I placeholder standard sono:

- {{ class\_name }} — nome della classe in PascalCase (es. ChatAgent)

- {{ snake\_name }} — nome in snake_case (es. chat_agent)

- {{ kebab\_name }} — nome in kebab-case (es. chat-agent)

- {{ timestamp }} — timestamp per le migration

## **3.2 Configurazione — config/settings.py**

Tutta la configurazione è centralizzata in un unico file Pydantic Settings. Ogni variabile ha un valore default e può essere sovrascritta da .env.

from pydantic_settings import BaseSettings

from functools import lru_cache

class Settings(BaseSettings):

    \# App

    APP\_NAME: str \= "elric-app"

    APP\_ENV: str \= "development"          \# development | production

    APP\_DEBUG: bool \= True

    APP\_PORT: int \= 8000

    APP\_HOST: str \= "0.0.0.0"



    \# Database

    DATABASE\_URL: str                      \# postgresql+asyncpg://user:pass@host/db

    DATABASE\_POOL\_SIZE: int \= 10

    DATABASE\_MAX\_OVERFLOW: int \= 20



    \# Redis

    REDIS\_URL: str \= "redis://localhost:6379/0"



    \# Auth

    API\_KEY\_HEADER: str \= "X-API-Key"

    API\_KEY\_PREFIX: str \= "elk\_live\_"



    \# Rate limiting

    RATE\_LIMIT\_REQUESTS: int \= 100         \# richieste per finestra

    RATE\_LIMIT\_WINDOW: int \= 60            \# secondi



    \# LangSmith

    LANGCHAIN\_TRACING\_V2: bool \= False

    LANGCHAIN\_API\_KEY: str \= ""

    LANGCHAIN\_PROJECT: str \= "elric-app"



    \# Logging

    LOG\_LEVEL: str \= "INFO"

    LOG\_JSON: bool \= True                  \# False in dev per leggibilità



    model\_config \= SettingsConfigDict(env\_file=".env", extra="ignore")

@lru_cache

def get_settings() \-\> Settings:

    return Settings()

## **3.3 FastAPI App — app/\_\_init\_\_.py**

L'applicazione FastAPI usa il pattern lifespan per gestire startup/shutdown. Tutti i router vengono inclusi automaticamente.

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.middleware.api_key import ApiKeyMiddleware

from app.middleware.rate_limit import RateLimitMiddleware

from app.middleware.logging import LoggingMiddleware

from app.providers.database import init_db

from app.providers.redis import init_redis

from app.providers.langsmith import init_langsmith

from app.exceptions.handler import global_exception_handler

from app.routes import health

@asynccontextmanager

async def lifespan(app: FastAPI):

    await init\_db()

    await init\_redis()

    init\_langsmith()

    yield

    \# cleanup on shutdown

def create_app() \-\> FastAPI:

    app \= FastAPI(

        title="Elric App",

        lifespan=lifespan,

        docs\_url="/docs" if settings.APP\_DEBUG else None,

    )

    app.add\_middleware(LoggingMiddleware)

    app.add\_middleware(RateLimitMiddleware)

    app.add\_middleware(ApiKeyMiddleware)

    app.add\_exception\_handler(Exception, global\_exception\_handler)

    app.include\_router(health.router)

    return app

## **3.4 Auth — API Key Middleware**

Ogni richiesta deve includere l'header X-API-Key. Il middleware valida la key in due step: prima controlla la cache Redis, poi il database PostgreSQL.

\# Flusso di validazione

Request ricevuta

└─\> Estrai header X-API-Key

      ├─\> Mancante → 401 Unauthorized

      └─\> Presente

          ├─\> Check Redis cache (key: "apikey:{hash}")

          │   ├─\> HIT  → key valida, procedi

          │   └─\> MISS → query PostgreSQL

          │           ├─\> Non trovata → 401

          │           ├─\> Disattiva → 401

          │           ├─\> Scaduta   → 401

          │           └─\> Valida → salva in Redis (TTL 300s) \+ procedi

          └─\> Inietta api\_key\_id in request.state

### **Modello API Key (database/models/api_key.py)**

from sqlmodel import SQLModel, Field

from datetime import datetime

from typing import Optional

import uuid

class ApiKey(SQLModel, table=True):

    \_\_tablename\_\_ \= "api\_keys"



    id: uuid.UUID \= Field(default\_factory=uuid.uuid4, primary\_key=True)

    name: str \= Field(index=True)           \# nome descrittivo

    key\_hash: str \= Field(unique=True)       \# sha256 della key

    prefix: str                              \# primi 12 char (elk\_live\_xxxx)

    is\_active: bool \= Field(default=True)

    expires\_at: Optional\[datetime\] \= None

    last\_used\_at: Optional\[datetime\] \= None

    created\_at: datetime \= Field(default\_factory=datetime.utcnow)

## **3.5 Rate Limiting — Redis**

Il rate limiting usa il pattern sliding window counter su Redis. Ogni key API ha un contatore separato.

\# Pattern: sliding window counter

Redis key: "ratelimit:{api_key_id}:{window}"

\# Per ogni richiesta:

1\. window \= int(time.time() / RATE_LIMIT_WINDOW)

2\. key \= f"ratelimit:{api_key_id}:{window}"

3\. count \= INCR key

4\. if count \== 1: EXPIRE key RATE_LIMIT_WINDOW

5\. if count \> RATE_LIMIT_REQUESTS: return 429

## **3.6 Logging — structlog**

Tutti i log sono in formato JSON con trace_id propagato da ogni request attraverso tutto lo stack (middleware → controller → agent → tool).

\# Struttura log standard

{

"timestamp": "2026-03-19T10:23:41Z",

"level": "info",

"event": "agent.run.completed",

"trace_id": "uuid-v4-per-request",

"api_key_id": "uuid-della-key",

"agent": "ChatAgent",

"duration_ms": 342,

"tokens_used": 1240,

"http_method": "POST",

"http_path": "/api/v1/chat",

"http_status": 200

}

Il trace_id viene generato nel LoggingMiddleware e iniettato nel contesto structlog via contextvars, rendendolo disponibile ovunque senza doverlo passare esplicitamente.

## **3.7 Error Handling — GlobalExceptionHandler**

Tutte le eccezioni vengono catturate da un unico handler. I controller non gestiscono mai le eccezioni direttamente.

\# Gerarchia delle eccezioni

ElricException (base)

├── ValidationException → 422

├── AuthException → 401

├── ForbiddenException → 403

├── NotFoundException → 404

├── RateLimitException → 429

├── AgentException → 500

├── DatabaseException → 503

└── ExternalServiceException → 502

\# Response JSON uniforme per tutti gli errori

{

"error": "agent_failed",

"message": "Descrizione human-readable",

"trace_id": "uuid-per-debug",

"code": 500

}

## **3.8 Agents — LangGraph**

Ogni agent estende BaseAgent che fornisce: logging automatico, tracing LangSmith, gestione errori e interfaccia comune.

\# app/agents/base_agent.py

from abc import ABC, abstractmethod

from langgraph.graph import StateGraph

class BaseAgent(ABC):

    name: str \= "base\_agent"



    @abstractmethod

    def build\_graph(self) \-\> StateGraph:

        """Costruisce e restituisce il grafo LangGraph."""

        ...



    async def run(self, input: dict) \-\> dict:

        """Esegue l'agent con logging e tracing automatici."""

        graph \= self.build\_graph().compile()

        return await graph.ainvoke(input)

\# Stub generato da: uv run elric make:agent ChatAgent

class ChatAgent(BaseAgent):

    name \= "chat\_agent"



    def build\_graph(self) \-\> StateGraph:

        graph \= StateGraph(dict)

        graph.add\_node("process", self.\_process)

        graph.set\_entry\_point("process")

        return graph



    async def \_process(self, state: dict) \-\> dict:

        \# TODO: implementa la logica

        return state

## **3.9 Health Check — /health**

L'endpoint /health verifica lo stato di tutti i servizi e risponde con un oggetto dettagliato. Usato da Docker e load balancer.

GET /health

Response 200:

{

"status": "healthy",

"version": "1.0.0",

"services": {

    "database": "ok",

    "redis": "ok",

    "langsmith": "ok"

}

}

Response 503 (se un servizio è down):

{

"status": "degraded",

"services": { "database": "error", "redis": "ok", "langsmith": "ok" }

}

# **4\. Database Layer**

## **4.1 Provider — app/providers/database.py**

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from sqlalchemy.orm import sessionmaker

from sqlmodel import SQLModel

from config.settings import get_settings

settings \= get_settings()

engine \= create_async_engine(

    settings.DATABASE\_URL,

    pool\_size=settings.DATABASE\_POOL\_SIZE,

    max\_overflow=settings.DATABASE\_MAX\_OVERFLOW,

    echo=settings.APP\_DEBUG,

)

AsyncSessionLocal \= sessionmaker(engine, class\_=AsyncSession, expire_on_commit=False)

async def init_db():

    async with engine.begin() as conn:

        await conn.run\_sync(SQLModel.metadata.create\_all)

async def get_session() \-\> AsyncSession:

    async with AsyncSessionLocal() as session:

        yield session

## **4.2 Convenzioni SQLModel**

- Tutti i modelli in database/models/, un file per entità

- Ogni modello ha id UUID come primary key

- created_at e updated_at automatici su ogni tabella

- Relazioni definite con Relationship di SQLModel

- Migration generate con: uv run elric make:migration \<descrizione\>

\# Struttura standard di ogni modello

class NomeModello(SQLModel, table=True):

    \_\_tablename\_\_ \= "nome\_tabella"



    id: uuid.UUID \= Field(default\_factory=uuid.uuid4, primary\_key=True)

    \# ... campi ...

    created\_at: datetime \= Field(default\_factory=datetime.utcnow)

    updated\_at: datetime \= Field(default\_factory=datetime.utcnow)

# **5\. Docker Setup**

## **5.1 Development — docker-compose.yml**

In sviluppo il codice è montato come volume e uvicorn gira con \--reload. Il database e Redis sono servizi separati.

services:

app:

    build:

      context: .

      dockerfile: docker/Dockerfile.dev

    volumes:

      \- .:/app                         \# hot-reload del codice

    ports:

      \- "8000:8000"

    env\_file: .env

    depends\_on:

      db:    { condition: service\_healthy }

      redis: { condition: service\_healthy }

    command: uv run uvicorn app:create\_app \--factory \--reload \--host 0.0.0.0

db:

    image: postgres:16-alpine

    environment:

      POSTGRES\_DB: elric\_dev

      POSTGRES\_USER: elric

      POSTGRES\_PASSWORD: secret

    volumes:

      \- postgres\_data:/var/lib/postgresql/data

    healthcheck:

      test: \["CMD-SHELL", "pg\_isready \-U elric"\]

      interval: 5s

redis:

    image: redis:7-alpine

    healthcheck:

      test: \["CMD", "redis-cli", "ping"\]

      interval: 5s

## **5.2 Production — Dockerfile.prod (multi-stage)**

\# Stage 1: builder

FROM python:3.12-slim AS builder

COPY \--from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN uv sync \--frozen \--no-dev

\# Stage 2: production

FROM python:3.12-slim AS production

WORKDIR /app

COPY \--from=builder /app/.venv ./.venv

COPY . .

ENV PATH="/app/.venv/bin:$PATH"

ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1

RUN adduser \--disabled-password \--no-create-home appuser

USER appuser

EXPOSE 8000

CMD \["gunicorn", "app:create_app", "--factory",

     "--worker-class", "uvicorn.workers.UvicornWorker",

     "--workers", "4", "--bind", "0.0.0.0:8000"\]

# **6\. Windsurf Rules & Skills**

I file .windsurf/rules/ istruiscono l'AI di Windsurf su come generare codice coerente con le convenzioni del progetto. Ogni file ha un trigger (glob pattern) per essere applicato solo nei contesti rilevanti.

## **6.1 Contenuto di ogni rule file**

| File                    | Glob trigger                                   | Contenuto principale                                                         |
| :---------------------- | :--------------------------------------------- | :--------------------------------------------------------------------------- |
| 01-python-fastapi.md    | app/\*\*/\*.py                                 | Stile Python, async/await, type hints, RORO pattern, HTTPException, lifespan |
| 02-agents-langchain.md  | app/agents/\*\*,app/chains/\*\*,app/tools/\*\* | BaseAgent pattern, StateGraph setup, LangSmith tracing, async ainvoke        |
| 03-database-sqlmodel.md | database/\*\*/\*.py                            | SQLModel conventions, UUID pk, async session, migration naming               |
| 04-docker-uv.md         | docker/\*\*,Dockerfile\*,pyproject.toml        | Multi-stage build, uv sync, non-root user, healthcheck pattern               |
| 05-elric-conventions.md | \*\*/\*.py                                     | Naming snake_case, struttura file, import order, stub conventions, CLI usage |

## **6.2 Struttura di ogni rule file**

\---

description: "Regole per FastAPI e Python nel progetto Elric"

globs: \["app/\*\*/\*.py", "elric_cli/\*\*/\*.py"\]

alwaysApply: false

\---

\# Titolo della rule

\#\# Principi

\- Usa async def per tutte le operazioni I/O-bound

\- ...

\#\# Pattern obbligatori

...

\#\# Esempi

\`\`\`python

\# CORRETTO

async def get_user(user_id: uuid.UUID, session: AsyncSession) \-\> UserResponse:

    ...

\`\`\`

## **6.3 Skills disponibili**

- make-agent.md — come strutturare un agent LangGraph completo con stati, nodi e edges

- make-chain.md — come strutturare una chain LangChain con prompt template e output parser

- make-route.md — come creare un router FastAPI con dependency injection e schema

- debug-langsmith.md — come leggere le trace LangSmith e debuggare una run fallita

# **7\. Piano di Implementazione**

Il piano è diviso in 6 fasi. Ogni fase produce un deliverable funzionante e testabile. Le fasi sono sequenziali — ogni fase dipende dalla precedente.

## **Fase 1 — Scaffolding base (Giorno 1-2)**

| Obiettivo | Progetto Python funzionante con uv, struttura cartelle, pyproject.toml configurato |
| :-------- | :--------------------------------------------------------------------------------- |

1. Inizializza progetto uv: uv init elric-app

2. Crea struttura cartelle completa (vedere sezione 2\)

3. Configura pyproject.toml con tutte le dipendenze

4. Crea .env.example con tutte le variabili necessarie

5. Configura ruff come linter/formatter

6. Crea docker/Dockerfile.dev e docker-compose.yml

7. Verifica: docker compose up funziona

### **Dipendenze pyproject.toml (principali)**

\[project\]

dependencies \= \[

    "fastapi\>=0.115",

    "uvicorn\[standard\]\>=0.30",

    "sqlmodel\>=0.0.21",

    "alembic\>=1.13",

    "asyncpg\>=0.29",

    "redis\[asyncio\]\>=5.0",

    "langchain\>=0.3",

    "langgraph\>=0.2",

    "langsmith\>=0.1",

    "pydantic-settings\>=2.0",

    "structlog\>=24.0",

    "typer\>=0.12",

    "jinja2\>=3.1",

\]

## **Fase 2 — Config \+ Provider \+ App base (Giorno 3\)**

| Obiettivo | FastAPI app che si avvia con /health endpoint funzionante |
| :-------- | :-------------------------------------------------------- |

8. Implementa config/settings.py con Pydantic Settings

9. Implementa app/providers/database.py (async engine \+ session)

10. Implementa app/providers/redis.py (async Redis client)

11. Implementa app/providers/langsmith.py (tracing setup)

12. Crea app/\_\_init\_\_.py con create_app() \+ lifespan

13. Crea app/routes/health.py con GET /health

14. Verifica: curl localhost:8000/health risponde 200

## **Fase 3 — Auth \+ Rate Limit \+ Logging (Giorno 4-5)**

| Obiettivo | Ogni richiesta validata via API Key con logging JSON e rate limiting |
| :-------- | :------------------------------------------------------------------- |

15. Crea database/models/api_key.py (SQLModel model)

16. Prima migration: uv run alembic revision \--autogenerate \-m "create_api_keys"

17. Implementa app/middleware/api_key.py

18. Implementa app/middleware/rate_limit.py

19. Implementa app/middleware/logging.py (trace_id via contextvars)

20. Configura structlog in config/logging.py

21. Registra tutti i middleware in create_app()

22. Verifica: richiesta senza key → 401, con key → 200, oltre limit → 429

## **Fase 4 — Error Handling \+ Exceptions (Giorno 6\)**

| Obiettivo | Tutti gli errori gestiti centralmente con response JSON uniforme |
| :-------- | :--------------------------------------------------------------- |

23. Crea app/exceptions/base.py con ElricException e sottoclassi

24. Crea app/exceptions/handler.py con global_exception_handler

25. Registra l'handler in create_app()

26. Verifica: ogni tipo di eccezione produce la response JSON corretta con trace_id

## **Fase 5 — CLI Elric (Giorno 7-9)**

| Obiettivo | uv run elric make:agent NomeAgent genera file corretto |
| :-------- | :----------------------------------------------------- |

27. Crea tutti i file stub in stubs/ (14 stub)

28. Implementa elric_cli/app.py con Typer

29. Implementa elric_cli/commands/make.py (tutti i make:\* commands)

30. Implementa elric_cli/commands/migrate.py (wrappa alembic)

31. Implementa elric_cli/commands/serve.py (wrappa uvicorn)

32. Implementa elric_cli/commands/route.py (route:list)

33. Implementa elric_cli/commands/apikey.py (create, list, revoke)

34. Configura script in pyproject.toml: \[project.scripts\] elric \= "elric_cli.app:app"

35. Verifica: uv run elric \--help mostra tutti i comandi

## **Fase 6 — Agents Base \+ Windsurf Rules (Giorno 10-11)**

| Obiettivo | BaseAgent funzionante, esempio completo, rules Windsurf configurate |
| :-------- | :------------------------------------------------------------------ |

36. Implementa app/agents/base_agent.py con logging \+ tracing integrati

37. Implementa app/chains/base_chain.py

38. Implementa app/tools/base_tool.py

39. Genera un agent di esempio con la CLI: uv run elric make:agent ExampleAgent

40. Crea tutti i file .windsurf/rules/ (5 file)

41. Crea tutti i file .windsurf/skills/ (4 file)

42. Crea docker/Dockerfile.prod (multi-stage)

43. Crea docker/docker-compose.prod.yml

44. Verifica: build prod funziona, test suite base passa

# **8\. .env.example — Variabili d'Ambiente**

\# ── App ──────────────────────────────────────────────

APP_NAME=elric-app

APP_ENV=development \# development | production

APP_DEBUG=true

APP_PORT=8000

APP_HOST=0.0.0.0

\# ── Database ─────────────────────────────────────────

DATABASE_URL=postgresql+asyncpg://elric:secret@localhost:5432/elric_dev

DATABASE_POOL_SIZE=10

DATABASE_MAX_OVERFLOW=20

\# ── Redis ────────────────────────────────────────────

REDIS_URL=redis://localhost:6379/0

\# ── Auth ─────────────────────────────────────────────

API_KEY_HEADER=X-API-Key

API_KEY_PREFIX=elk_live\_

\# ── Rate Limiting ────────────────────────────────────

RATE_LIMIT_REQUESTS=100 \# richieste per finestra

RATE_LIMIT_WINDOW=60 \# secondi

\# ── LangSmith ────────────────────────────────────────

LANGCHAIN_TRACING_V2=false

LANGCHAIN_API_KEY=ls\_\_xxxxxxxxxx

LANGCHAIN_PROJECT=elric-app

\# ── Logging ──────────────────────────────────────────

LOG_LEVEL=INFO

LOG_JSON=false \# true in production

# **9\. Checklist di Completamento**

## **Fase 1 — Scaffolding**

- \[x\] uv init elric-app

- \[x\] Struttura cartelle creata

- \[x\] pyproject.toml configurato

- \[x\] .env.example creato

- \[x\] docker-compose.yml funzionante

## **Fase 2 — App base**

- \[x\] config/settings.py

- \[x\] app/providers/database.py

- \[x\] app/providers/redis.py

- \[x\] app/providers/langsmith.py

- \[x\] app/\_\_init\_\_.py con create_app()

- \[x\] GET /health risponde 200

## **Fase 3 — Auth \+ Middleware**

- \[x\] database/models/api_key.py

- \[x\] Migration api_keys

- \[x\] app/middleware/api_key.py

- \[x\] app/middleware/rate_limit.py

- \[x\] app/middleware/logging.py

- \[x\] structlog configurato

## **Fase 4 — Error Handling**

- \[ \] app/exceptions/base.py

- \[ \] app/exceptions/handler.py

- \[ \] Response JSON uniforme con trace_id

## **Fase 5 — CLI**

- \[ \] 14 file stub in stubs/

- \[ \] elric_cli/ implementata

- \[ \] uv run elric \--help funziona

- \[ \] make:agent genera file corretto

- \[ \] migrate:\* wrappano alembic

## **Fase 6 — Agents \+ Windsurf**

- \[ \] app/agents/base_agent.py

- \[ \] app/chains/base_chain.py

- \[ \] app/tools/base_tool.py

- \[ \] 5 file .windsurf/rules/

- \[ \] 4 file .windsurf/skills/

- \[ \] Dockerfile.prod multi-stage

- \[ \] Test suite base passa
