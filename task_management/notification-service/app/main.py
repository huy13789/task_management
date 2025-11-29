from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_noti():
    return {"Đây là dịch vụ gửi thông báo (Notification Service)"}
