from fastapi import FastAPI
from starlette.responses import JSONResponse

app = FastAPI(title="Task Service", root_path="/task")

@app.get("/")
def read_root():
    return {"Đây là dịch vụ quản lý công việc (Task Service)"}

@app.get("/health", tags=["System"])
def health_check():
    return JSONResponse(content={"status":"ok", "service": "task-service"}, status_code=200)
