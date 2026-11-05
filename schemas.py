from pydantic import BaseModel, EmailStr
from typing import Optional

# Skema untuk input saat registrasi user baru
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    age: Optional[int] = None

# Skema untuk update data user (semua opsional)
class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    age: Optional[int] = None

# Skema untuk ubah password user yang sedang login
class ChangePassword(BaseModel):
    old_password: str
    new_password: str

# Skema untuk respons data user yang dikembalikan ke klien (TANPA menampilkan password asli/hash)
class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    age: Optional[int] = None

    class Config:
        from_attributes = True
