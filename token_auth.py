from datetime import datetime, timedelta, timezone
import jwt

# Kunci rahasia untuk menandatangani token (Jaga kerahasiaan ini di produksi!)
SECRET_KEY = "kunci_rahasia_super_aman_buat_jwt_anda"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Masa aktif token (30 menit)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
