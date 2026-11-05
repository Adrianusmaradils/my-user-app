from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    age: int | None = None

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    age: int | None = None

    class Config:
        from_attributes = True

