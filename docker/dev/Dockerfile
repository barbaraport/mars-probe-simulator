FROM python:3.12-slim
RUN groupadd --gid 1000 appuser \
    && useradd --uid 1000 --gid appuser --shell /bin/bash --create-home appuser
WORKDIR /app
RUN pip install --no-cache-dir uv && chown -R appuser:appuser /app
USER appuser
COPY --chown=appuser:appuser pyproject.toml uv.lock ./
RUN ls -ld /app && whoami && RUN touch /app/testfile && RUN uv sync --frozen --dev
COPY --chown=appuser:appuser . .
CMD ["uv", "run", "fastapi", "dev", "app/main.py", "--host", "0.0.0.0"]