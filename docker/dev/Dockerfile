FROM python:3.12-slim

WORKDIR /app

RUN pip install uv

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --dev

COPY . .

CMD ["uv", "run", "fastapi", "dev", "app/main.py"]