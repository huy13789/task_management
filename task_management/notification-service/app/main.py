from fastapi import FastAPI
from starlette.responses import JSONResponse

app = FastAPI(title="Notification Service", root_path="/notification")

@app.get("/")
def read_noti():
    return {"Đây là dịch vụ gửi thông báo (Notification Service)"}

@app.get("/health", tags=["System"])
def health_check():
    return JSONResponse(content={"status":"ok", "service": "notification-service"}, status_code=200)
