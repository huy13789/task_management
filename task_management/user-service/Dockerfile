# 1. Chọn base image
FROM python:3.12-slim

# 2. Cài đặt uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# 3. Thiết lập biến môi trường
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# QUAN TRỌNG: Thêm đường dẫn .venv vào PATH
# Khi uv sync chạy, nó sẽ tạo .venv. Ta thêm dòng này để hệ thống tự nhận diện python trong đó.
ENV PATH="/app/.venv/bin:$PATH"

WORKDIR /app

# 4. Copy file quản lý thư viện
COPY pyproject.toml uv.lock ./

# 5. Cài đặt thư viện
RUN uv sync --frozen

# 6. Copy code nguồn
COPY . .

# 7. Chạy server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]