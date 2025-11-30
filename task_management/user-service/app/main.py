from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

app = FastAPI(title="User Service", root_path="/user")

# CORS
origins = [
    "http://localhost:3000",
    "*"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Trang chủ Backend"}

@app.get("/items")
def read_items():
    return [{"id": 1, "name": "Item 1"}]

@app.get("/health", tags=["System"])
def health_check():
    return JSONResponse(content={"status": "ok", "service": "user-service"}, status_code=200)

