.PHONY: help uv-setup uv-uninstall clean setup deps dev check format test prod migration db-upgrade ci

COMPOSE=docker-compose --env-file ./.env -f docker/docker-compose.yml
TEST_COMPOSE=docker-compose --env-file ./.env.test -f docker/docker-compose.yml -f docker/dev/docker-compose.yml
CI_COMPOSE=docker compose --env-file ./.env.test -f docker/docker-compose.yml -f docker/ci/docker-compose.yml 

help:
	@printf "Available commands:\n"
	@printf " make help                      Show this help message\n"
	@printf " make setup                     Install dependencies, enable git hooks, and migrate the DB\n"
	@printf " make dev                       Start the local development environment\n"
	@printf " make test                      Run the test suite in the test compose environment\n"
	@printf " make check                     Run lint, format checks, and mypy\n"
	@printf " make db-upgrade                Apply Alembic migrations to the development DB\n"
	@printf " make migration name=\"<msg>\"    Create a new Alembic migration and apply upgrades\n"
	@printf " make clean                     Remove build artifacts and stop Docker containers\n"

uv-setup:
	@curl -LsSf https://astral.sh/uv/install.sh | sh
	@uv self update

uv-uninstall:
	@uv cache clean
	@rm -rf "$$(uv python dir)"
	@rm -rf "$$(uv tool dir)"
	@rm -f ~/.local/bin/uv ~/.local/bin/uvx

clean:
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@rm -rf node_modules
	@rm -rf .ruff_cache
	@rm -rf .mypy_cache
	@rm -rf .venv
	@rm -f .coverage
	@rm -rf .pytest_cache
	@$(COMPOSE) -f docker/dev/docker-compose.yml down --remove-orphans -v

setup:
	@${MAKE} uv-setup
	@${MAKE} deps
	@npx husky init
	@echo "make check" > .husky/pre-commit
	@chmod +x .husky/commit-msg
	@chmod +x .husky/pre-commit
	@${MAKE} db-upgrade

deps:
	@uv sync --quiet
	@npm ci --silent

check:
	@uv run ruff check .
	@uv run ruff format --check .
	@uv run mypy .

format:
	@uv run ruff check --fix .
	@uv run ruff format .

dev:
	@$(COMPOSE) -f docker/dev/docker-compose.yml up --build

prod:
	@$(COMPOSE) -f docker/prod/docker-compose.yml up --build

test:
	@$(TEST_COMPOSE) run --rm mars-probe-simulator-app uv run pytest --cov
	@$(TEST_COMPOSE) down

db-upgrade:
	@$(COMPOSE) -f docker/dev/docker-compose.yml run --rm mars-probe-simulator-app uv run alembic upgrade head
	@$(COMPOSE) -f docker/dev/docker-compose.yml down

migration:
	@if [ -z "$(name)" ]; then echo "Error: name parameter required. Usage: make migration name='description'"; exit 1; fi
	@${MAKE} db-upgrade
	@$(COMPOSE) -f docker/dev/docker-compose.yml run --rm mars-probe-simulator-app uv run alembic revision --autogenerate -m "$(name)"
	@$(COMPOSE) -f docker/dev/docker-compose.yml run --rm mars-probe-simulator-app uv run alembic upgrade head

ci:
	@$(CI_COMPOSE) run --rm mars-probe-simulator-app sh -c "uv run --no-venv pytest --cov"
	@$(CI_COMPOSE) down