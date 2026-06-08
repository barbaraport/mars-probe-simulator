# 🚀 mars-probe-simulator
![CodeRabbit Pull Request Reviews](https://img.shields.io/coderabbit/prs/github/barbaraport/mars-probe-simulator?utm_source=oss&utm_medium=github&utm_campaign=barbaraport%2Fmars-probe-simulator&labelColor=171717&color=FF570A&link=https%3A%2F%2Fcoderabbit.ai&label=CodeRabbit+Reviews)

A production-grade backend API built with **FastAPI**, designed to demonstrate how I structure scalable, maintainable, and testable systems in a real-world engineering environment.

This repository is intentionally organized to show:
- clean architectural separation,
- async-first business logic,
- infrastructure-ready persistence,
- rigorous test coverage,
- and developer-friendly local workflows.

> ✅ Test coverage results are deployed automatically on merges to `main`.
> View the deployed coverage report here: [https://barbaraport.github.io/mars-probe-simulator/](https://barbaraport.github.io/mars-probe-simulator/)

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

### 🐳 Docker & Environment Strategy

This project uses environment-specific Docker configurations to reflect real-world deployment workflows.

Each environment has different operational goals and therefore different build/runtime requirements:

| Environment | Purpose |
|------------|----------|
| Development | Developer productivity, hot reload, debugging, and local tooling |
| Test | Deterministic execution of automated test suites |
| Production | Lean runtime image with only the dependencies required to run the application |

This separation helps prevent development-only tooling from leaking into production images while keeping local workflows fast and reproducible.

```text
docker/
├── prometheus.yml            # prometheus configuration
├── docker-compose.yml        # shared/base services
├── dev/
│   ├── Dockerfile
│   └── docker-compose.yml
├── test/
│   ├── Dockerfile
│   └── docker-compose.yml
└── prod/
    ├── Dockerfile
    └── docker-compose.yml
```

Key benefits:

- isolated environment concerns
- predictable builds
- production-safe container images
- reproducible development and testing workflows
- reduced operational risk

## 📊 Observability

This application includes production-oriented observability capabilities based on modern telemetry standards.

### Signals

The service emits the three fundamental observability signals:

- **Logs** (structured JSON logging)
- **Metrics** (Prometheus)
- **Traces** (OpenTelemetry)

### Structured Logging

All application logs are emitted as structured JSON and include request correlation metadata.

Grid setup example:
```json
mars-probe-simulator-app-1  | {"status": "started", "grid_id": "75cf11e0-f5d5-4dd7-b895-22e7e3d66fa8", "grid_x": 10, "grid_y": 10, "probe_id": "fc5e8297-4b08-4c44-b830-f1924589fa7c", "probe_x": 0, "probe_y": 0, "probe_direction": "NORTH", "event": "PROBE_CREATED", "correlation_id": "31bef03e-4f3d-4c59-a7bb-612049c6018a", "timestamp": "2026-06-08T01:08:47.138437Z", "level": "info"}
mars-probe-simulator-app-1  | {"operation": "increment", "new_value": 1.0, "event": "PROBE_CREATED_TOTAL", "correlation_id": "31bef03e-4f3d-4c59-a7bb-612049c6018a", "timestamp": "2026-06-08T01:08:47.138494Z", "level": "info"}

mars-probe-simulator-app-1  | {"status": "finished", "grid_id": "75cf11e0-f5d5-4dd7-b895-22e7e3d66fa8", "grid_x": 10, "grid_y": 10, "probe_id": "fc5e8297-4b08-4c44-b830-f1924589fa7c", "probe_x": 0, "probe_y": 0, "probe_direction": "NORTH", "event": "PROBE_CREATED", "correlation_id": "31bef03e-4f3d-4c59-a7bb-612049c6018a", "timestamp": "2026-06-08T01:08:47.138512Z", "level": "info"}

mars-probe-simulator-app-1  | {"method": "POST", "path": "/api/v1/setup", "status_code": 200, "duration_ms": 65.18, "event": "COMPLETED_REQUEST", "correlation_id": "31bef03e-4f3d-4c59-a7bb-612049c6018a", "timestamp": "2026-06-08T01:08:47.138988Z", "level": "info"}
```

Command example:
```json
mars-probe-simulator-app-1  | {"status": "started", "probe_id": "fc5e8297-4b08-4c44-b830-f1924589fa7c", "command": "MMMRMMM", "from_x": 0, "from_y": 0, "from_direction": "NORTH", "to_x": 3, "to_y": 3, "to_direction": "EAST", "event": "PROBE_COMMAND_SENT", "correlation_id": "32dcb6f3-f5ee-4cc0-a841-cae6f6ae026e", "timestamp": "2026-06-08T01:09:42.239671Z", "level": "info"}

mars-probe-simulator-app-1  | {"operation": "increment", "new_value": 1.0, "event": "PROBE_COMMANDS_TOTAL", "correlation_id": "32dcb6f3-f5ee-4cc0-a841-cae6f6ae026e", "timestamp": "2026-06-08T01:09:42.239719Z", "level": "info"}

mars-probe-simulator-app-1  | {"status": "finished", "probe_id": "fc5e8297-4b08-4c44-b830-f1924589fa7c", "command": "MMMRMMM", "from_x": 0, "from_y": 0, "from_direction": "NORTH", "to_x": 3, "to_y": 3, "to_direction": "EAST", "event": "PROBE_COMMAND_SENT", "correlation_id": "32dcb6f3-f5ee-4cc0-a841-cae6f6ae026e", "timestamp": "2026-06-08T01:09:42.239736Z", "level": "info"}

mars-probe-simulator-app-1  | {"method": "PATCH", "path": "/api/v1/move", "status_code": 200, "duration_ms": 9.49, "event": "COMPLETED_REQUEST", "correlation_id": "32dcb6f3-f5ee-4cc0-a841-cae6f6ae026e", "timestamp": "2026-06-08T01:09:42.239865Z", "level": "info"}
```

### Health Endpoints

Operational endpoints are available for runtime monitoring.

| Endpoint | Purpose |
|-----------|----------|
| `/ready` | Readiness check, including database connectivity |
| `/metrics` | Prometheus metrics endpoint |

### Metrics

Metrics are exposed using Prometheus-compatible format.

Collected metrics include:

- request count
- request duration
- in-flight requests
- error rates
- endpoint-specific statistics
- domain usage statistics (grid/probe)

### Distributed Tracing

The application is instrumented with OpenTelemetry and automatically generates traces for:

- FastAPI requests
- service execution
- repository operations
- SQLAlchemy database interactions

[![Mars probe simulator Jaeger tracing for a probe movement](https://raw.githubusercontent.com/barbaraport/mars-probe-simulator/refs/heads/main/files/jaeger.png)](https://raw.githubusercontent.com/barbaraport/mars-probe-simulator/refs/heads/main/files/jaeger.png)

### Local Observability Stack

Development environments include a complete local observability stack.

| Service | URL |
|----------|------|
| FastAPI Docs | http://localhost:8000/docs |
| Prometheus | http://localhost:9090 |
| Grafana | http://localhost:3000 |
| Jaeger | http://localhost:16686 |
| Adminer | http://localhost:8080 |

### Tooling

[!NOTE]
> The application is instrumented through OpenTelemetry and can export telemetry to any OTLP-compatible observability backend.

- **OpenTelemetry**: Vendor-neutral telemetry standard used to generate traces and metrics.
- **Prometheus**: Metrics collection and time-series database.
- **Grafana**: Dashboarding and metrics visualization.
- **Jaeger**: Distributed tracing backend used to inspect request execution flows.

[![Mars probe simulator Grafana dashboard](https://raw.githubusercontent.com/barbaraport/mars-probe-simulator/refs/heads/main/files/grafana.mov)](https://raw.githubusercontent.com/barbaraport/mars-probe-simulator/refs/heads/main/files/grafana.mov)

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

To run the test suite, use the provided make commands. `make setup` initializes the development environment and installs dependencies, while `make test` executes all tests across the pyramid.

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
├── unit/                    # isolated business logic tests
│   ├── services/            # service orchestration
│   ├── domain/              # domain rules and entities
├── integration/             # database persistence tests
│   └── repositories/        # repository contracts and queries
└── e2e/                     # HTTP endpoint tests, route contracts and workflows
```

> This approach yields confidence for both safe refactoring and production-quality delivery.

[![Tests execution](https://raw.githubusercontent.com/barbaraport/mars-probe-simulator/refs/heads/main/files/tests.png)](https://raw.githubusercontent.com/barbaraport/mars-probe-simulator/refs/heads/main/files/tests.png)

> 🧪✅ Coverage results are deployed automatically on merges to `main`; inspect the latest report here: [https://barbaraport.github.io/mars-probe-simulator/](https://barbaraport.github.io/mars-probe-simulator/)

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

The app loads configuration from `.env` in development. `.env.test` is used for the test environment, while `.env.prod` is used for the production app.

Example `.env`:

```env
APP_PORT=8000
ADMINER_PORT=8080
DB_HOST=mars-probe-simulator-db
DB_PORT=5432
DB_USER=myappuser
DB_PASSWORD=password
DB_NAME=mydb
ENV=dev # dev, test, prod
GRAFANA_ADMIN_USER=admin
GRAFANA_ADMIN_USER_PASSWORD=admin
```

[!WARNING]
> Each `.env` file is used for a specific purpose (development, testing, or production).
> For a complete experience, you should create `.env`, `.env.test`, and `.env.prod`.
> All must contain the same variables.
> You should change the values for each environment, avoiding conflicts.

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
