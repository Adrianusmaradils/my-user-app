from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import models, schemas
from database import engine, get_db
from hashing import Hash

# Membuat tabel database secara otomatis jika belum ada
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="My User App",
    description="Aplikasi manajemen pengguna dengan FastAPI dan SQLAlchemy",
    version="1.0.0"
)

# 1. Endpoint Root / Beranda
@app.get("/")
def read_root():
    return {"message": "Selamat datang di My User App dengan Database SQLAlchemy!"}

# 2. Endpoint POST untuk Registrasi Pengguna Baru (dengan Hashing Password)
@app.post("/users/register", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user_email = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user_email:
        raise HTTPException(status_code=400, detail="Email sudah terdaftar!")
    
    db_user_name = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user_name:
        raise HTTPException(status_code=400, detail="Username sudah digunakan!")

    hashed_password_str = Hash.encrypt(user.password)

    new_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password_str,
        age=user.age
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

# 3. Endpoint GET untuk Mengambil Seluruh Pengguna
@app.get("/users", response_model=list[schemas.UserResponse])
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users

# 4. Endpoint GET untuk Mencari Pengguna Berdasarkan ID
@app.get("/users/{user_id}", response_model=schemas.UserResponse)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pengguna dengan ID {user_id} tidak ditemukan"
        )
    return user

# 5. Endpoint PUT untuk Memperbarui Data Pengguna Berdasarkan ID
@app.put("/users/{user_id}", response_model=schemas.UserResponse)
def update_user(user_id: int, user_update: schemas.UserUpdate, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pengguna dengan ID {user_id} tidak ditemukan"
        )
    
    if user_update.username is not None:
        user.username = user_update.username
    if user_update.email is not None:
        user.email = user_update.email
    if user_update.age is not None:
        user.age = user_update.age
    if user_update.password is not None:
        user.hashed_password = Hash.encrypt(user_update.password)

    db.commit()
    db.refresh(user)

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

# 7. Endpoint POST untuk Login & Autentikasi Pengguna
@app.post("/users/login")
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username atau password salah",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not Hash.verify(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username atau password salah",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return {
        "message": "Login berhasil!",
        "username": user.username,
        "email": user.email
    }
