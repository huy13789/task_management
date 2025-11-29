# 1. Chọn base image
FROM python:3.12-slim

# 2. Cài đặt uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# 3. Thiết lập biến môi trường
# Quan trọng: Đặt luôn đường dẫn venv vào PATH để không cần gõ 'uv run' nữa
ENV PATH="/app/.venv/bin:$PATH"
# Để python không tạo file .pyc rác
ENV PYTHONDONTWRITEBYTECODE=1
# Để log hiện ra ngay lập tức
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# 4. Copy file quản lý thư viện và cài đặt
COPY pyproject.toml uv.lock ./

# --frozen: Dùng đúng phiên bản trong lock file
#cài thư viện
RUN uv sync --frozen
 
# 5. Copy toàn bộ code nguồn
COPY . .

# 6. Chạy server
# Vì code đã nằm trong thư mục 'app', ta gọi app.main:app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8010"]