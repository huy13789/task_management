# 🚀 Task Management Microservice System

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white)
![Traefik](https://img.shields.io/badge/Traefik-24a1c1?style=flat&logo=traefik&logoColor=white)
![uv](https://img.shields.io/badge/uv-package_manager-purple)
![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python&logoColor=white)

**Hệ thống quản lý tác vụ (Task Management)** được xây dựng theo kiến trúc **Microservices**, sử dụng **FastAPI**, **Docker** và **Traefik Gateway**. Dự án được tối ưu hóa cho hiệu suất cao với trình quản lý gói `uv`.

---

## 🛠 Hướng Dẫn Cài Đặt (Installation)

### 1. Cài đặt
  ### Docker, Postgrel

## 2. Khởi Chạy Dự Án (Running)
  ```bash
  docker-compose up -d --build
  ```
## 4. Dừng hệ thống
  ```bash
  docker-compose down # hoặc là Crl + C cho nhanh rồi xóa Image
  ```

## 💬 Khắc Phục Lỗi (Troubleshooting)

  ### 🔴 Lỗi 1: Bind for 0.0.0.0:80 failed
  ```
    Nguyên nhân: Cổng 80 thường bị chiếm bởi Windows System (IIS) hoặc Skype.

    Giải pháp: Dự án này đã được cấu hình chuyển sang cổng 8080. Hãy truy cập localhost:8080. 
  ```
  ### 🔴 Lỗi 2: OS Error 5 / Access Denied
  ```
      Nguyên nhân: Windows khóa quyền truy cập thư mục .venv khi map volume từ máy thật vào Docker.

      Giải pháp: Xóa thư mục ảo và build lại
      docker-compose down
      # Xóa thủ công thư mục task_management/account-service/.venv
      docker-compose up -d --build
  ```
  ### 🔴 Lỗi 3: Frontend bị lỗi CORS
  ```
  Giải pháp: Kiểm tra file app/main.py, đảm bảo URL của Frontend (ví dụ http://localhost:3000) đã được thêm vào biến allow_origins.
  ```

## 🧰 Project Structure
```
root/
├── docker-compose.yml              # 🎼 Nhạc trưởng điều phối (Orchestration)
├── .env                            # 🔑 Biến môi trường (DB, Secret Key)
├── task_management/                # 📂 Thư mục chứa các Microservices
│   └── account-service/            # 👤 Service Tài Khoản
│       ├── app/                    # Source code chính
│       │   ├── api/                # Định nghĩa Routes
│       │   ├── core/               # Configs
│       │   └── main.py             # Entry point
│       ├── Dockerfile              # Cấu hình Build Docker
│       ├── pyproject.toml          # Danh sách thư viện
│       └── uv.lock                 # Khóa phiên bản thư viện
└── README.md
```

## 🌐 Cổng Truy Cập (Port Mapping)

Hệ thống sử dụng **Traefik** làm Gateway chính điều hướng request.

| Service       | URL / Host               | Mô tả                                                        |
|---------------|--------------------------|--------------------------------------------------------------|
| API Gateway   | [http://localhost:8080](http://localhost:8080)   | Cổng chính (Frontend gọi vào đây)    |
| Swagger UI    | [http://localhost:8080/docs](http://localhost:8080/docs) | Tài liệu API & Test tool     |
| Traefik Dash  | [http://localhost:8081](http://localhost:8081)   | Dashboard quản lý Gateway            |
| Direct API    | [http://localhost:8000](http://localhost:8000)   | Truy cập trực tiếp (Chỉ dùng Debug)  |

## ✅ Tổng Hợp Lệnh Nhanh

| Hành động   | Lệnh                                    | Mô tả                                |
|-------------|-----------------------------------------|--------------------------------------|
| Khởi chạy   | `docker-compose up `                  | Chạy project          |
| Khởi chạy   | `docker-compose up -d` ❌                 | Chạy ngầm (Background mode)          |
| Rebuild     | `docker-compose up -d --build` 👍         | Chạy lại khi có thay đổi config/lib  |
| Dừng        | `docker-compose down`                   | Tắt và xóa containers                |
| Xem Log     | `docker-compose logs -f`                | Theo dõi log thời gian thực          |
| Vào Shell   | `docker-compose exec account-service bash` | SSH vào trong container           |