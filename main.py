from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
import models, schemas
from database import engine, get_db
from hashing import Hash
from token_auth import create_access_token, verify_access_token

# Membuat tabel database secara otomatis jika belum ada
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="My User App",
    description="Aplikasi manajemen pengguna dengan FastAPI, SQLAlchemy, dan JWT Authentication",
    version="1.0.0"
)

# Konfigurasi skema OAuth2 untuk Swagger UI
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

# Fungsi Dependensi untuk Memverifikasi Token & Mengambil User yang Sedang Login
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    username = verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.username == username).first()
    if user is None:
        raise credentials_exception
    return user

# 1. Endpoint Root / Beranda
@app.get("/")
def read_root():
    return {"message": "Selamat datang di My User App dengan FastAPI & JWT!"}

# 2. Endpoint POST untuk Registrasi Pengguna Baru
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

# 7. Endpoint POST untuk Login & Mengembalikan JWT Access Token
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
    
    access_token = create_access_token(data={"sub": user.username})
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

# 8. Endpoint Terproteksi (Contoh: Profil User yang sedang Login)
@app.get("/users/me/profile", response_model=schemas.UserResponse)
def get_current_user_profile(current_user: models.User = Depends(get_current_user)):
    return current_user
