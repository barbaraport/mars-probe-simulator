# 🚀 mars-probe-simulator

A production-grade backend API built with **FastAPI**, designed to demonstrate how I structure scalable, maintainable, and testable systems in a real-world engineering environment.

This repository is intentionally organized to show:
- clean architectural separation,
- async-first business logic,
- infrastructure-ready persistence,
- rigorous test coverage,
- and developer-friendly local workflows.

## 🌟 Engineering Highlights

- ⚡ **Async-first architecture** using FastAPI and SQLAlchemy 2.0 async
- 🧱 **Layered domain model** with clear API / service / domain / repository boundaries
- 🧪 **Full testing pyramid**: unit, integration, and E2E coverage
- 🐘 **PostgreSQL-ready** data layer with Alembic migrations and database contract safety
- 🛠 **Quality tooling**: `ruff`, automated hooks, and environment-specific workflows
- 🧩 **Extendable design** for future features and production adoption

## ⚙️ Tech Stack

- **FastAPI** – high-performance async HTTP layer
- **uv** – dependency and environment management
- **Pydantic v2** – validation and schema contracts
- **SQLAlchemy 2.0 (async)** – async ORM and persistence
- **PostgreSQL** – production-grade relational storage
- **Alembic** – migrations and schema versioning
- **Docker / Docker Compose** – consistent local development and CI-style test environments
- **pytest** – deterministic, fast automated testing
- **ruff** – linting, formatting, and static checks

---

## 🏗 Architecture Overview

This service uses a layered backend architecture to minimize coupling and reduce risk when shipping changes.

HTTP Layer (FastAPI routes)

↓

Service Layer (business orchestration)

↓

Domain Layer (probe/grid rules)

↓

Repository Layer (data access)

↓

Database (PostgreSQL)

Each layer is intentionally responsible for only one concern:

- **Routes** → translate HTTP requests into application input/output
- **Services** → orchestrate business rules, validation, and workflows
- **Domain** → encapsulate core probe/grid logic and invariants
- **Repositories** → isolate persistence specifics from domain behavior
- **Schemas/Models** → enforce contracts and data integrity

## 📁 Project Structure

app/
├── api/            # HTTP entrypoints, routers, dependency wiring
├── core/           # configuration, database setup, environment bootstrapping
├── domain/         # business rules, entities, command handling
├── models/         # SQLAlchemy ORM models and schema mapping
├── schemas/        # Pydantic request/response models and validation
├── services/       # application business logic and use-case orchestration
├── repositories/   # database persistence abstractions
└── main.py         # application startup and router mounting

This layout is designed to support team development, safe refactoring, and incremental feature growth.

---

## 🧪 Test Strategy

This repository follows a disciplined test pyramid with clearly defined test boundaries.

### ✔ Unit tests
Validate business logic in isolation, without network or database dependencies.
- Services
- Domain rules
- Validation utilities
- Command parsing

### ✔ Integration tests
Verify persistence and repository behavior against a real database.
- SQLAlchemy queries
- repository contracts
- transactional behavior

### ✔ End-to-end tests
Validate real HTTP behavior through FastAPI endpoints.
- route contracts
- request/response validation
- business workflows

> This approach yields confidence for both safe refactoring and production-quality delivery.

---

## 🔐 Design Principles

### Service-oriented business logic
The service layer isolates orchestration and enables reuse across APIs, CLI tools, or background workers.

### Repository abstraction
Database access is decoupled from domain rules, making the core logic independent of persistence mechanism.

### Dependency injection
FastAPI dependencies are used to keep wiring explicit, replaceable, and testable.

### Async-first implementation
The app is built around async endpoints, async sessions, and non-blocking IO for modern backend performance.

### Contract-first validation
Pydantic schemas and explicit command validation ensure invalid input fails fast and clearly.

---

## 🧱 Why this repository stands out

This project was structured to demonstrate backend engineering maturity:

- predictable service boundaries
- clear domain ownership
- robust validation and error handling
- environment-specific configuration
- containerized local development
- repeatable migration workflows
- quality gates through automated tooling

---

## ✅ Prerequisites

- Python `3.12` or higher
- `uv` for dependency and environment management
- Docker and Docker Compose for local development and testing
- Node.js / npm for package management and git hooks
- `.env` and `.env.test` for environment configuration

## 🧾 Environment files

The app loads configuration from `.env` in development. `.env.test` is used for the test environment.

Example `.env`:

```env
APP_PORT=8000
ADMINER_PORT=8080
DB_HOST=mars-probe-simulator-db
DB_PORT=5432
DB_USER=myappuser
DB_PASSWORD=password
DB_NAME=mydb
ENV=dev
```

Example `.env.test`:

```env
APP_PORT=8000
ADMINER_PORT=8080
DB_HOST=mars-probe-simulator-db
DB_PORT=5433
DB_USER=test
DB_PASSWORD=test
DB_NAME=test
ENV=test
```

### ⛳ Local commands

- `make setup` — install dependencies, enable Git hooks, and migrate the database
- `make dev` — start the local development Docker stack
- `make test` — run the test suite inside the test Compose environment
- `make check` — run lint, formatting, and static analysis
- `make db-upgrade` — apply database migrations
- `make migration name="<message>"` — create a new Alembic migration

---

## 🚀 Getting Started

1. Run `make setup` to install dependencies and prepare the environment.
2. Run `make dev` to start the app with the local Docker stack.
3. Open `http://localhost:8000/docs` to explore the automatically generated OpenAPI UI.

---

## 🧰 Code Quality and Developer Experience

This repo includes quality controls that reflect engineering discipline:

- **Husky** for Git hooks
- **Commitlint** for conventional commit enforcement
- **`make check`** for linting and static checks
- environment-specific runtime configuration
- modular and testable dependency wiring

---

## 🚧 API Endpoints

All endpoints are exposed under `/api/v1`.

- `POST /api/v1/setup`
  - initialize a Mars probe on a grid
  - accepts `x`, `y`, and `direction`
  - returns the created probe state
- `PATCH /api/v1/move`
  - execute movement commands against an existing probe
  - valid commands: `L`, `R`, `M`
  - prevents invalid grid moves and invalid commands
- `GET /api/v1/check`
  - returns current probe coordinates and orientation

> OpenAPI docs are available at `/docs` when the app is running.

---

## 🐳 Docker & Deployment Ready

This repository includes Docker Compose configuration for both development and test workflows.

- `docker/docker-compose.yml` — core application, Postgres, and Adminer
- `docker/dev/docker-compose.yml` — development-specific build and runtime configuration
- `docker/prod/docker-compose.yml` — production-style compose manifest

`make dev` launches the local stack, while `make test` executes the suite in a reproducible test environment.

---

## 📦 Database Access (Adminer)

Adminer is included as a lightweight tool for inspecting the database during local development.

It enables:

- browsing tables and records
- running raw SQL queries
- inspecting schema design
- validating persisted data quickly

This accelerates development without requiring an external database client.

---

## 📌 What this demonstrates

This project demonstrates how I build backend systems with:

- clear ownership of responsibilities,
- engineering rigor in design and testing,
- production-minded infrastructure,
- and a strong focus on maintainability and team collaboration.


```bash
make setup
make dev
```

Open the FastAPI docs at `http://localhost:8000/docs`

## 🧪 Running Tests

```bash
make setup
make test
```

---

## 📌 What This Project Demonstrates
This assessment was used to demonstrate:
- Ability to design scalable backend architectures
- Strong understanding of Python async systems
- Practical testing discipline (not just unit tests, but full pyramid coverage)
- Clean code organization suitable for team environments
- Production-level thinking (not just “works locally” implementations)

## 🧠 Closing Note
This project was intentionally structured beyond the minimum requirements to reflect real-world backend engineering practices, including maintainability, scalability, and test strategy design.