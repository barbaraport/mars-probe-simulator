FROM python:3.12-slim
RUN groupadd --gid 1000 appuser \
    && useradd --uid 1000 --gid appuser --shell /bin/bash --create-home appuser
WORKDIR /app
RUN pip install --no-cache-dir uv && chown -R appuser:appuser /app
USER appuser
COPY --chown=appuser:appuser pyproject.toml uv.lock ./
USER root
RUN chmod 444 pyproject.toml uv.lock
USER appuser
RUN uv sync --frozen --no-dev
COPY --chown=appuser:appuser . .
USER root
RUN chmod -R a-w /app
USER appuser
CMD ["uv", "run", "fastapi", "run", "app/main.py", "--host", "0.0.0.0"]