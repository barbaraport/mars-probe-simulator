FROM python:3.12-slim
RUN groupadd --gid 1000 appuser \
    && useradd --uid 1000 --gid appuser --shell /bin/bash --create-home appuser
WORKDIR /app
RUN mkdir -p /tmp/coverage /tmp/htmlcov \
    && chown -R appuser:appuser /tmp/coverage /tmp/htmlcov \
    && chmod -R 775 /tmp/coverage /tmp/htmlcov \
    && pip install --no-cache-dir uv \
    && chown -R appuser:appuser /app
USER appuser
ENV UV_PROJECT_ENVIRONMENT=/home/appuser/.venv
COPY --chown=appuser:appuser pyproject.toml uv.lock ./
RUN uv sync --frozen --dev
COPY --chown=appuser:appuser . .
CMD ["uv", "run", "fastapi", "dev", "app/main.py", "--host", "0.0.0.0"]