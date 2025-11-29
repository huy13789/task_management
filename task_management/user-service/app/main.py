from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Giữ nguyên CORS để FE gọi được
origins = [
    "http://localhost:3000",      # React/Next.js
    "*"                           # HOẶC: Chấp nhận tất cả (Chỉ dùng lúc Dev)
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,        
    allow_credentials=True,
    allow_methods=["*"],          # Cho phép mọi phương thức (GET, POST, PUT, DELETE)
    allow_headers=["*"],          # Cho phép mọi loại dữ liệu gửi lên
)

@app.get("/")
def read_root():
    return {"message": "Trang chủ Backend"}

@app.get("/items")
def read_items():
    return [{"id": 1, "name": "Item 1"}]
