from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    otp: Optional[str] = None

class UserCreate(UserBase):
    pass

class UserUpdate(UserBase):
    email: Optional[EmailStr] = None
    
class UserResponse(UserBase):
    id: int
