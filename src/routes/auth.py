from fastapi import APIRouter, Depends, Request, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timedelta, timezone

from src.utils.jwt import create_access_token, create_refresh_token, decode_token_access_token, decode_token_refresh_token
from src.database.database import get_async_db
from src.models.user import User
from src.schemas.user import UserCreate, UserResponse
from src.schemas.auth import Auth, OTPVerify, RefreshToken
import os
from dotenv import load_dotenv
load_dotenv()

OTP_EXPIRE_MINUTES = int(os.getenv("OTP_EXPIRE_MINUTES", 10))

router = APIRouter()
otpStore = {}

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user: UserCreate, db: AsyncSession = Depends(get_async_db)):
    # Check if user already exists
    result = await db.execute(select(User).where(User.email == user.email))
    existing_user = result.scalar_one_or_none()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    db_user = User(**user.model_dump())
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

@router.post("/request-otp", response_model=dict,status_code=status.HTTP_200_OK)
async def request_otp(auth: Auth, db: AsyncSession = Depends(get_async_db)):
    result = await db.execute(select(User).where(User.email == auth.email))
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Email not found"
        )
    
    user.otp = "123456"
    await db.commit()
    expire = datetime.now(timezone.utc) + timedelta(minutes=OTP_EXPIRE_MINUTES)
    otpStore[auth.email] = {"otp":"123456","exp":expire}
    return {"message": "OTP Sent Successfully"}

@router.post("/verify-otp", response_model=dict,status_code=status.HTTP_200_OK)
async def verify_otp(auth: OTPVerify, db: AsyncSession = Depends(get_async_db)):
    result = await db.execute(select(User).where(User.email == auth.email))
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Email not found"
        )
    
    if otpStore[auth.email]["exp"] < datetime.now(timezone.utc):
        del otpStore[auth.email]
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="OTP Expired"
        )
    if otpStore[auth.email]["otp"] != auth.otp:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid OTP"
        )
    
    user.otp = None
    await db.commit()
    
    access_token,expire = create_access_token({"email": auth.email})
    refresh_token,_ = create_refresh_token({"email": auth.email})
    
    return {
        "email": auth.email, 
        "access_token": access_token, 
        "refresh_token": refresh_token,
        "exp": expire
    }

@router.post("/refresh-token", response_model=dict,status_code=status.HTTP_200_OK)
async def refresh_token(token: RefreshToken):
    print("Getting Refresh Token:", token.refresh_token)
    data, status_code = decode_token_refresh_token(token.refresh_token)

    if status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token"
        )
    
    email = data.get("email")
    if not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload"
        )
    
    access_token,expire = create_access_token({"email": email})
    return {"message": "Token refreshed", "access_token": access_token, "exp": expire}