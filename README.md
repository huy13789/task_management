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
  ### Docker, Postgrel, Setup uv

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
app/
├── api/                        # 🛡️ TẦNG GIAO TIẾP & PHỤ THUỘC (Dependencies)
│   ├── __init__.py
│   └── deps.py                 # "Keo dán" của hệ thống.
│                               # - Chứa các hàm `Depends(...)`.
│                               # - Lấy Header/Token từ Request.
│                               # - Gọi `auth` để giải mã Token.
│                               # - Gọi `db` để lấy kết nối.
│                               # - Trả về `current_user` hoặc `db_session` cho Router dùng.
│
├── auth/                       # 🔐 TẦNG BẢO MẬT THUẦN TÚY (Pure Security)
│   ├── jwt.py                  # - Chỉ chứa logic: Encode & Decode Token (PyJWT).
│   │                           # - Không biết DB là gì, không biết Request là gì.
│   └── security.py             # - Chỉ chứa logic: Hash Password & Verify Password (Argon2).
│
├── core/                       # ⚙️ TẦNG CẤU HÌNH (Configuration)
│   ├── config.py               # - Load biến môi trường (.env).
│   │                           # - Cung cấp settings (DATABASE_URL, SECRET_KEY) cho toàn app.
│   └── logger.py (nếu có)      # - Cấu hình định dạng log.
│
├── db/                         # 🔌 TẦNG KẾT NỐI (Database Connection)
│   └── __init__.py             # - Khởi tạo `Engine` và `SessionLocal`.
│                               # - Quản lý việc đóng/mở kết nối tới PostgreSQL.
│
├── models/                     # 🗄️ TẦNG DỮ LIỆU (Data Layer / ORM)
│   ├── __init__.py             # - Base class của SQLAlchemy.
│   └── user.py                 # - Định nghĩa cấu trúc Bảng `users` trong SQL (Cột, Kiểu dữ liệu).
│
├── schemas/                    # 📝 TẦNG CHUYỂN ĐỔI DỮ LIỆU (DTO / Pydantic)
│   └── user.py                 # - Định dạng dữ liệu Đầu vào (UserCreate, UserLogin).
│                               # - Định dạng dữ liệu Đầu ra (UserResponse).
│                               # - Validate dữ liệu (Email đúng chuẩn, Pass đủ dài...).
│
├── services/                   # 🧠 TẦNG NGHIỆP VỤ (Business Logic Layer)
│   ├── auth_service.py         # - Logic Đăng nhập (Gọi DB tìm user -> Gọi Auth check pass -> Trả Token).
│   └── user_service.py         # - Logic User (Tạo user, Check trùng email, Update, Delete...).
│                               # - Đây là nơi "thông minh" nhất của ứng dụng.
│
├── routers/                    # 🌐 TẦNG ĐIỀU PHỐI (Controller / Interface)
│   ├── login.py                # - Endpoint: POST /login.
│   └── users.py                # - Endpoint: POST /users/, GET /me...
│                               # - Nhiệm vụ: Nhận Request -> Gọi Service -> Trả Response.
│                               # - Code ở đây phải cực kỳ ngắn gọn.
│
└── main.py                     # 🟢 ĐIỂM KHỞI CHẠY (Entry Point)
                                # - Khởi tạo FastAPI App.
                                # - Gắn Middleware (CORS, Gzip).
                                # - Gắn (Include) các Routers vào App.
```

## 🌐 Cổng Truy Cập (Port Mapping)

Hệ thống sử dụng **Traefik** làm Gateway chính điều hướng request.

| Service       | URL / Host               | Mô tả                                                        |
|---------------|--------------------------|--------------------------------------------------------------|
| API Gateway   | [http://localhost:8080](http://localhost:8080)   | Cổng chính (Frontend gọi vào đây)    |
| Swagger UI    | [http://localhost:8080/docs](http://localhost:8080/docs) | Tài liệu API & Test tool     |
| Traefik Dash  | [http://localhost:8081](http://localhost:8081)   | Dashboard quản lý Gateway            |
| User Service    | [http://localhost:8080/user](http://localhost:8080/user)   | Truy cập User service qua Gateway  |
| Task Service    | [http://localhost:8080/task](http://localhost:8080/task)   | Truy cập User service qua Gateway  |
| Notification Service    | [http://localhost:8080/notification](http://localhost:8080/notification)   | Truy cập Notification service qua Gateway  |
| Dev Direct API (User, Task, Notification)    | [http://localhost:8010, 8020, 8030]()   | Truy cập trực tiếp container (chỉ dev/debug)  |

## ✅ Tổng Hợp Lệnh Nhanh

| Hành động   | Lệnh                                    | Mô tả                                |
|-------------|-----------------------------------------|--------------------------------------|
| Khởi chạy   | `docker-compose up `                  | Chạy project          |
| Khởi chạy   | `docker-compose up -d` ❌                 | Chạy ngầm (Background mode)          |
| Rebuild     | `docker-compose up -d --build` 👍         | Chạy lại khi có thay đổi config/lib  |
| Dừng        | `docker-compose down -v`                   | Tắt và xóa containers                |
| Xem Log     | `docker-compose logs -f`                | Theo dõi log thời gian thực          |
| Vào Shell   | `docker-compose exec account-service bash` | SSH vào trong container           |