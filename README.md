# 🚀 mars-probe-simulator

A production-grade backend API built with **FastAPI**, designed to demonstrate how I structure scalable, maintainable, and testable systems in a real-world engineering environment.

This repository is intentionally organized to show:
- clean architectural separation,
- async-first business logic,
- infrastructure-ready persistence,
- rigorous test coverage,
- and developer-friendly local workflows.

[![Mars Probe Simulator API home](https://raw.githubusercontent.com/barbaraport/mars-probe-simulator/refs/heads/main/files/api_home.png)](https://raw.githubusercontent.com/barbaraport/mars-probe-simulator/refs/heads/main/files/api_home.png)

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

### 🐳 Docker & Deployment Ready

This repository includes Docker Compose configuration for both development and test workflows.

- `docker/docker-compose.yml` — core application, Postgres, and Adminer
- `docker/dev/docker-compose.yml` — development-specific build and runtime configuration
- `docker/prod/docker-compose.yml` — production-style compose manifest

`make dev` launches the local stack, while `make test` executes the suite in a reproducible test environment.

### 🧰 Code Quality and Developer Experience

This repo includes quality controls that reflect engineering discipline:

- **Husky** for Git hooks
- **Commitlint** for conventional commit enforcement
- **`make check`** for linting and static checks
- environment-specific runtime configuration
- modular and testable dependency wiring

#### 📦 Database Access (Adminer)

Adminer is included as a lightweight tool for inspecting the database during local development.

It enables:

- browsing tables and records
- running raw SQL queries
- inspecting schema design
- validating persisted data quickly

This accelerates development without requiring an external database client.

[![Mars probe simulator tables on Adminer](https://raw.githubusercontent.com/barbaraport/mars-probe-simulator/refs/heads/main/files/adminer-1.png)](https://raw.githubusercontent.com/barbaraport/mars-probe-simulator/refs/heads/main/files/adminer-1.png)

### ⛳ Local commands

- `make setup` — install dependencies, enable Git hooks, and migrate the database
- `make dev` — start the local development Docker stack
- `make test` — run the test suite inside the test Compose environment
- `make check` — run lint, formatting, and static analysis
- `make db-upgrade` — apply database migrations
- `make migration name="<message>"` — create a new Alembic migration

---

## 🏗 Architecture Overview

This service uses a layered backend architecture to minimize coupling and reduce risk when shipping changes.

<div align="center">
<pre>
HTTP Layer
(FastAPI routes)
↓
Service Layer
(business orchestration)
↓
Domain Layer
(probe/grid rules)
↓
Repository Layer
(data access)
↓
Database
(PostgreSQL)
</pre>
</div>

Each layer is intentionally responsible for only one concern:

- **Routes** → translate HTTP requests into application input/output
- **Services** → orchestrate business rules, validation, and workflows
- **Domain** → encapsulate core probe/grid logic and invariants
- **Repositories** → isolate persistence specifics from domain behavior
- **Schemas/Models** → enforce contracts and data integrity

## 📁 Project Structure

```text
app/
├── api/            # HTTP entrypoints, routers, dependency wiring
├── core/           # configuration, database setup, environment bootstrapping
├── domain/         # business rules, entities, command handling
├── models/         # SQLAlchemy ORM models and schema mapping
├── schemas/        # Pydantic request/response models and validation
├── services/       # application business logic and use-case orchestration
├── repositories/   # database persistence abstractions
└── main.py         # application startup and router mounting
```

This layout is designed to support team development, safe refactoring, and incremental feature growth.

---

## 🧪 Test Strategy

This repository follows a disciplined test pyramid with clearly defined test boundaries.

To run the test suite, use the provided make commands. `make setup` initializes the development environment and installs dependencies, while `make test` executes all tests across the pyramid. These commands streamline the setup and test execution process, ensuring consistency across the development team.

```bash
make setup
make test
```

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

```text
tests/
├── unit/               # isolated business logic tests
│   ├── test_services/       # service orchestration
│   ├── test_domain/         # domain rules and entities
│   └── test_validation/     # input validation and parsing
├── integration/        # database persistence tests
│   └── test_repositories/   # repository contracts and queries
└── e2e/               # HTTP endpoint tests
    └── test_api/            # route contracts and workflows
```

> This approach yields confidence for both safe refactoring and production-quality delivery.

[![Tests execution](https://raw.githubusercontent.com/barbaraport/mars-probe-simulator/refs/heads/main/files/tests.png)](https://raw.githubusercontent.com/barbaraport/mars-probe-simulator/refs/heads/main/files/tests.png)

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

## ✅ Prerequisites

- Python `3.12` or higher
- `uv` for dependency and environment management
- `Docker` and `Docker Compose` for local development and testing
- `Node.js` / `npm` for package management and git hooks
- `.env` and `.env.test` for environment configuration

### 🧾 Environment files

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

## 🚀 Getting Started

Run both commands in sequence to prepare and launch the application:

```bash
make setup
make dev
```

1. Run `make setup` to install dependencies, enable Git hooks, and migrate the database.
2. Run `make dev` to start the app and its local Docker stack.
3. Open `http://localhost:8000/docs` to explore the automatically generated OpenAPI UI.

---

## 🚧 API Endpoints

All endpoints are exposed under `/api/v1`.

- `POST /api/v1/setup`
  - initialize a Mars probe on a grid
  - accepts `x`, `y`, and `direction`
  - returns the created probe state

[![Probe/Grid setup router](https://raw.githubusercontent.com/barbaraport/mars-probe-simulator/refs/heads/main/files/setup-1.png)](https://raw.githubusercontent.com/barbaraport/mars-probe-simulator/refs/heads/main/files/setup-1.png)
[![Probe/Grid setup router response](https://raw.githubusercontent.com/barbaraport/mars-probe-simulator/refs/heads/main/files/setup-2.png)](https://raw.githubusercontent.com/barbaraport/mars-probe-simulator/refs/heads/main/files/setup-2.png)

- `PATCH /api/v1/move`
  - execute movement commands against an existing probe
  - valid commands: `L`, `R`, `M`
  - prevents invalid grid moves and invalid commands

[![Grid movement router](https://raw.githubusercontent.com/barbaraport/mars-probe-simulator/refs/heads/main/files/move-1.png)](https://raw.githubusercontent.com/barbaraport/mars-probe-simulator/refs/heads/main/files/move-1.png)
[![Probe/Grid move response](https://raw.githubusercontent.com/barbaraport/mars-probe-simulator/refs/heads/main/files/move-2.png)](https://raw.githubusercontent.com/barbaraport/mars-probe-simulator/refs/heads/main/files/move-2.png)
[![Probe/Grid move error for non existent command](https://raw.githubusercontent.com/barbaraport/mars-probe-simulator/refs/heads/main/files/move-3.png)](https://raw.githubusercontent.com/barbaraport/mars-probe-simulator/refs/heads/main/files/move-3.png)
[![Probe/Grid move error for command with invalid result](https://raw.githubusercontent.com/barbaraport/mars-probe-simulator/refs/heads/main/files/move-4.png)](https://raw.githubusercontent.com/barbaraport/mars-probe-simulator/refs/heads/main/files/move-4.png)

- `GET /api/v1/check`
  - returns current probe coordinates and orientation

[![Available probes list](https://raw.githubusercontent.com/barbaraport/mars-probe-simulator/refs/heads/main/files/check-1.png)](https://raw.githubusercontent.com/barbaraport/mars-probe-simulator/refs/heads/main/files/check-1.png)
[![Available probes after fetching](https://raw.githubusercontent.com/barbaraport/mars-probe-simulator/refs/heads/main/files/check-2.png)](https://raw.githubusercontent.com/barbaraport/mars-probe-simulator/refs/heads/main/files/check-2.png)

> OpenAPI docs are available at `/docs` when the app is running.

---

## 📌 What this project demonstrates
This repository demonstrates how I approach backend engineering with senior-level discipline:

- scalable backend architecture with clear service and domain boundaries
- async-first implementation aligned with modern Python best practices
- practical testing discipline across unit, integration, and E2E levels
- clean, modular code organization built for team collaboration
- production-minded infrastructure and deployment readiness
- strong focus on maintainability, validation, and long-term operability

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

## 🧠 Closing Note
This project was intentionally structured beyond the minimum requirements to reflect real-world backend engineering practices, including maintainability, scalability, and test strategy design.

<p align="center">
  <img src="https://ForTheBadge.com/images/badges/built-with-love.svg">
</p>