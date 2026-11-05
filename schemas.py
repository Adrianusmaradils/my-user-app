from pydantic import BaseModel, EmailStr
from typing import Optional

# Skema untuk validasi data saat update user (semua opsional)
class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    age: Optional[int] = None
