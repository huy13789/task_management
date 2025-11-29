from fastapi import FastAPI

app = FastAPI("/notification")

@app.get("/")
def read_noti():
    return {"Đây là dịch vụ gửi thông báo (Notification Service)"}
