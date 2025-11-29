from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Đây là dịch vụ quản lý công việc (Task Service)"}