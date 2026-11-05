from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
import models, schemas
from database import engine, get_db

# 1. Inisialisasi app FastAPI harus diletakkan DI ATAS sebelum dekorator endpoint (@app...)
app = FastAPI(
    title="My User App",
    description="Aplikasi manajemen pengguna dengan FastAPI dan SQLAlchemy",
    version="1.0.0"
)

# Membuat tabel database secara otomatis jika belum ada
models.Base.metadata.create_all(bind=engine)

# 2. Endpoint Root / Beranda
@app.get("/")
def read_root():
    return {"message": "Selamat datang di My User App dengan Database SQLAlchemy!"}

# 3. Endpoint POST untuk Registrasi Pengguna Baru
@app.post("/users/register", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user_email = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user_email:
        raise HTTPException(status_code=400, detail="Email sudah terdaftar!")
    
    db_user_name = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user_name:
        raise HTTPException(status_code=400, detail="Username sudah digunakan!")

    new_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=user.password,
        age=user.age
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

# 4. Endpoint GET untuk Mengambil Seluruh Pengguna
@app.get("/users", response_model=list[schemas.UserResponse])
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users

# 5. Endpoint GET untuk Mencari Pengguna Berdasarkan ID
@app.get("/users/{user_id}", response_model=schemas.UserResponse)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pengguna dengan ID {user_id} tidak ditemukan"
        )
    return user

# 6. Endpoint DELETE untuk Menghapus Pengguna Berdasarkan ID
@app.delete("/users/{user_id}", status_code=status.HTTP_200_OK)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pengguna dengan ID {user_id} tidak ditemukan"
        )
    
    db.delete(user)
    db.commit()
    
    return {"message": f"Pengguna dengan ID {user_id} berhasil dihapus"}
