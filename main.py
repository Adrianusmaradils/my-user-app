from fastapi import FastAPI

app = FastAPI(
    title="My User App",
    description="Aplikasi manajemen pengguna yang dibangun dengan FastAPI",
    version="1.0.0"
)

@app.get("/")
def read_root():
    return {"message": "Selamat datang di My User App!"}

@app.get("/users/{user_id}")
def read_user(user_id: int, q: str | None = None):
    return {"user_id": user_id, "query": q}
