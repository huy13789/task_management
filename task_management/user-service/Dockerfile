
FROM python:3.12-slim


COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/


ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

ENV PATH="/app/.venv/bin:$PATH"

WORKDIR /app

COPY pyproject.toml uv.lock ./
COPY requirements.txt .
RUN uv pip install --system --no-cache -r requirements.txt
RUN uv sync --frozen

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]