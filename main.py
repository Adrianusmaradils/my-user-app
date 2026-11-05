from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
import models, schemas
from database import engine, get_db
from hashing import Hash # Impor modul hashing yang baru dibuat

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="My User App",
    description="Aplikasi manajemen pengguna dengan FastAPI dan SQLAlchemy",
    version="1.0.0"
)

# Endpoint POST untuk Registrasi Pengguna Baru dengan Hashing Password
@app.post("/users/register", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Cek apakah email sudah terdaftar
    db_user_email = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user_email:
        raise HTTPException(status_code=400, detail="Email sudah terdaftar!")
    
    # Cek apakah username sudah digunakan
    db_user_name = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user_name:
        raise HTTPException(status_code=400, detail="Username sudah digunakan!")

    # Enkripsi password menggunakan Passlib sebelum disimpan
    hashed_password_str = Hash.encrypt(user.password)

    # Buat objek user baru dengan password yang sudah di-hash
    new_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password_str, # Menyimpan hash, bukan password asli
        age=user.age
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
