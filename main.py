from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr

app = FastAPI(
    title="My User App",
    description="Aplikasi manajemen pengguna dengan FastAPI",
    version="1.0.0"
)

# 1. Definisikan Model Pydantic untuk data registrasi
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    age: int | None = None

# Endpoint GET dasar
@app.get("/")
def read_root():
    return {"message": "Selamat datang di My User App!"}

# 2. Definisikan Endpoint POST untuk registrasi pengguna
@app.post("/users/register", status_code=201)
def register_user(user: UserCreate):
    # Di sini Anda biasanya akan mengenkripsi password dan menyimpannya ke database
    return {
        "message": "Registrasi pengguna berhasil!",
        "data": {
            "username": user.username,
            "email": user.email,
            "age": user.age
        }
    }
