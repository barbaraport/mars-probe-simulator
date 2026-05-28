.PHONY: uv-setup uv-uninstall clean setup deps dev check format

uv-setup:
	@curl -LsSf https://astral.sh/uv/install.sh | sh
	@uv self update

uv-uninstall:
	@uv cache clean
	@rm -rf "$(uv python dir)"
	@rm -rf "$(uv tool dir)"
	@rm -f ~/.local/bin/uv ~/.local/bin/uvx

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf node_modules
	rm -rf .ruff_cache
	rm -rf .mypy_cache
	rm -rf .venv

setup:
	${MAKE} uv-setup
	${MAKE} deps
	@npx husky init
	@chmod +x .husky/commit-msg

deps:
	@uv sync
	@npm ci

dev:
	uv run fastapi dev app/main.py

check:
	uv run ruff check .
	uv run ruff format --check .
	uv run mypy .

format:
	uv run ruff format .