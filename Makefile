.PHONY: uv-setup uv-uninstall clean setup deps dev check format test prod migration

COMPOSE= docker-compose --env-file ./.env -f docker/docker-compose.yml

uv-setup:
	@curl -LsSf https://astral.sh/uv/install.sh | sh
	@uv self update

uv-uninstall:
	@uv cache clean
	@rm -rf "$(uv python dir)"
	@rm -rf "$(uv tool dir)"
	@rm -f ~/.local/bin/uv ~/.local/bin/uvx

clean:
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@rm -rf node_modules
	@rm -rf .ruff_cache
	@rm -rf .mypy_cache
	@rm -rf .venv
	@rm -f .coverage
	@rm -rf .pytest_cache

setup:
	@${MAKE} uv-setup
	@${MAKE} deps
	@npx husky init
	@echo "make check" > .husky/pre-commit
	@chmod +x .husky/commit-msg
	@chmod +x .husky/pre-commit

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
	@$(COMPOSE) -f docker/dev/docker-compose.yml run --rm mars-probe-simulator-app uv run pytest --cov

migration:
	@$(COMPOSE) -f docker/dev/docker-compose.yml run --rm mars-probe-simulator-app uv run alembic revision --autogenerate -m "$(name)"
	@$(COMPOSE) -f docker/dev/docker-compose.yml run --rm mars-probe-simulator-app uv run alembic upgrade head