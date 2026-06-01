# 🚀 mars-probe-simulator

A production-style backend API built with **FastAPI**, designed to demonstrate clean architecture, testability, and real-world engineering practices using modern Python tooling.

This project was developed as a technical assessment and reflects how I structure, scale, and maintain backend systems in production environments.

---

## 📌 Key Highlights

- ⚡ Modern **Python** stack using `uv` for dependency and environment management
- 🧱 Clean layered architecture (API / Service / Repository separation)
- 🧪 Comprehensive testing strategy (unit, integration, E2E)
- 🐘 **PostgreSQL-ready** with migration support with ***Alembic*
- 🔁 Async-first design throughout the stack
- 🧩 Modular structure designed for scalability and team collaboration
- 🧼 Strict separation of concerns and dependency injection patterns

---

## 🏗 Architecture Overview

The project follows a layered architecture designed for maintainability and scalability:
HTTP Layer (FastAPI Routes)
↓
Service Layer (Business Logic)
↓
Domain Layer (Core Business Logic)
↓
Repository Layer (Data Access)
↓
Database (PostgreSQL)

Each layer has a clearly defined responsibility:

- **Routes** → request/response handling only
- **Services** → app business rules and orchestration
- **Domain** → core probe and grid business rules
- **Repositories** → database abstraction
- **Models/Schemas** → data integrity and validation

---

## 📁 Project Structure
app/
├── api/ # HTTP layer (routers, dependencies, middleware)
├── core/ # Config, security, logging, database setup
├── domain/ # Core probe and grid logic
├── models/ # SQLAlchemy ORM models
├── schemas/ # Pydantic DTOs (request/response models)
├── services/ # Business logic layer
├── repositories/ # Database access layer
└── main.py # Application entry point

This structure is designed to remain stable as the codebase grows, avoiding tight coupling between layers.

---

## � Prerequisites
- `uv` for Python dependency and environment management
- Docker and Docker Compose for local development and testing
- Node.js / npm for package management and git hooks
- Optional: `.env` file for environment configuration when running Docker Compose

## 🚀 Getting Started
1. Run `make setup` to install Python and Node dependencies, configure git hooks, and migrate the database.
2. Run `make dev` to start the development stack.
3. Open `http://localhost:8000/docs` to explore the FastAPI OpenAPI UI.

## ��� API Routes
All API endpoints are mounted under the `/api/v1` prefix and exposed through FastAPI. The key routes are:

- `POST /api/v1/setup`
  - Initialize a Mars probe on a grid
  - Accepts `x`, `y`, and `direction`
  - Returns the created probe state
- `PATCH /api/v1/move`
  - Move an existing probe using a command string
  - Valid commands are `L`, `R`, and `M`
  - Validates the command and prevents invalid grid movement
- `GET /api/v1/check`
  - Retrieve current coordinates and orientation for all probes

You can also explore the automatically generated OpenAPI documentation at `/docs` when the app is running.

---

## ⚙️ Tech Stack

- **FastAPI** – High-performance async API framework
- **uv** – Fast dependency and environment management
- **Pydantic v2** – Data validation and serialization
- **SQLAlchemy 2.0 (async)** – ORM layer
- **PostgreSQL** – Primary database
- **Alembic** – Database migrations
- **Docker / Docker Compose** – Local development, database, and test environment orchestration
- **pytest** – Testing framework
- **ruff** – Linting and formatting

## 🐳 Docker Usage
This project includes Docker Compose configuration for local development and testing.

- `docker/docker-compose.yml` defines the application, Postgres database, and Adminer services.
- `docker/dev/docker-compose.yml` provides development-specific build configuration.
- `make dev` starts the local development stack using Docker Compose.
- `make test` runs pytest inside the test Compose environment.
- `make db-upgrade` applies Alembic migrations in the development Docker environment.

Use a `.env` and `.env.test` files to configure service ports and database credentials for local runs.

## 🧾 Environment files
The app loads configuration from `.env` by default in development. The `.env.test` file is used when running tests.

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

## 📦 Database Access (Adminer)

I’ve included **Adminer** as an optional database management tool to simplify database inspection during local development and evaluation.

Adminer provides a lightweight web interface that allows you to:

- Browse database tables and records
- Execute raw SQL queries
- Inspect schema structure
- Debug and validate persisted data

This helps streamline development by removing the need for external database clients while still giving full visibility into the database layer when needed.

---

## 🧪 Testing Strategy

Testing is structured according to a **test pyramid model**:

### ✔ Unit Tests
Focus on business logic in isolation.

- Services
- Validators
- Utility functions
- Core business logic

No database or HTTP dependencies.

---

### ✔ Integration Tests
Validate interaction with real infrastructure.

- Database queries (PostgreSQL)
- Repository layer behavior

---

### ✔ End-to-End Tests
Validate full system behavior via HTTP.

- API endpoints

These tests ensure the system behaves correctly from a client perspective.

---

## 🔐 Design Decisions

### 1. Service-Oriented Business Logic
Business rules are isolated in services to ensure:
- Reusability across interfaces (API, workers, scripts)
- Easier unit testing
- Clear separation from transport layer

---

### 2. Repository Pattern
Database logic is abstracted into repositories to:
- Decouple persistence from business logic
- Improve testability
- Allow future database flexibility

---

### 3. Dependency Injection (FastAPI)
FastAPI’s dependency system is used to:
- Improve modularity
- Enable clean overrides in testing
- Reduce tight coupling between components

---

### 4. Async-First Design
The entire stack is designed around async execution:
- FastAPI async endpoints
- Async SQLAlchemy sessions
- Non-blocking I/O operations

---

## 🧱 Why This Architecture

This structure was chosen to reflect how I would build and maintain a production backend system:

- Easy to scale across teams
- Clear ownership of components
- High testability at every layer
- Minimal coupling between domain and infrastructure
- Ready for real-world deployment patterns

---

## 🚀 Running the Project

```make setup```
```make dev```

Open the FastAPI docs at `http://localhost:8000/docs`

### ⛳ Local commands
- `make setup` — install dependencies, enable husky hooks, and migrate the database
- `make dev` — start the local development Docker stack
- `make test` — run the test suite inside the test Compose environment
- `make check` — run lint, format checks, and static type analysis
- `make db-upgrade` — apply migrations to the local development database
- `make migration name="<message>"` — create a new Alembic migration after database changes

🧪 Running Tests

```make test```

📌 What This Project Demonstrates
This assessment was used to demonstrate:
- Ability to design scalable backend architectures
- Strong understanding of Python async systems
- Practical testing discipline (not just unit tests, but full pyramid coverage)
- Clean code organization suitable for team environments
- Production-level thinking (not just “works locally” implementations)

🧠 Closing Note
This project was intentionally structured beyond the minimum requirements to reflect real-world backend engineering practices, including maintainability, scalability, and test strategy design.