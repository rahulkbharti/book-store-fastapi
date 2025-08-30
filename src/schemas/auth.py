from pydantic import BaseModel, EmailStr

class Auth(BaseModel):
    email : EmailStr

class OTPVerify(BaseModel):
    email : EmailStr
    otp : str

class RefreshToken(BaseModel):
    refresh_token: str