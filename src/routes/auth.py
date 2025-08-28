from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from src.utils.jwt import create_access_token, create_refresh_token, decode_token
from src.database.db import get_db
from src.models.user import User
from src.schemas.user import UserCreate, UserResponse
from src.schemas.auth import Auth, OTPVerify

router = APIRouter(tags=["auth"])

@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.post("/request-otp",response_model=dict)
def request_otp(auth:Auth = None, db :Session = Depends(get_db)):
    user = db.query(User).filter(User.email == auth.email).first()
    print(auth.email)
    if not user:
        return {"message": "Email not found"}
    
    user.otp = "123456"
    db.commit()
    return {"message": "OTP Sent Successfully"}

@router.post("/verify-otp",response_model=dict)
def verify_otp(auth: OTPVerify, db :Session = Depends(get_db)):
    user = db.query(User).filter(User.email == auth.email).first()
    if not user:
        return {"message": "Email not found"}
    if user.otp != auth.otp:
        return {"message": "Invalid OTP"}
    
    user.otp = None
    db.commit()
    access_token= create_access_token({"email": auth.email})
    refresh_token = create_refresh_token({"email": auth.email})
    return {"message": "OTP verified successfully", "access_token": access_token, "refresh_token": refresh_token}


@router.post("/refresh-token", response_model=dict)
def refresh_token(request : Request):
    auth_header = request.headers.get("Authorization")
    print(auth_header.split(" ")[1])
    data,status = decode_token(auth_header.split(" ")[1])
    email = data.get("email")
    access_token = create_access_token({"email": email})
    return {"message": "Token refreshed", "access_token": access_token}


