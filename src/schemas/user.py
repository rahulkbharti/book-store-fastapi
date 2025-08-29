from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    otp: str

class UserResponse(UserBase):
    id: int
    email: Optional[EmailStr] = None
    otp: Optional[str] = None
    
    class ConfigDict:
        from_attributes = True