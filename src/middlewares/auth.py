from fastapi import Request, HTTPException, status
from functools import wraps
from src.utils.jwt import decode_token
from typing import Callable, Any

def protected_route(func: Callable) -> Callable:
    @wraps(func)
    async def wrapper(request: Request, *args, **kwargs) -> Any:
        print("Running the Middleware")
        print(f"Request: {request.method} {request.url}")

        auth_header = request.headers.get("Authorization")
        if not auth_header:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Not authenticated"
            )
        
        if not auth_header.startswith("Bearer "):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authorization header format"
            )
        
        token = auth_header.split(" ")[1]
        data, status_code = decode_token(token)
        
        if status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token"
            )
        
        email = data.get("email")
        print(f"Authenticated user: {email} using the route {request.url.path}")
        
        # Await the async function
        return await func(request, *args, **kwargs)
    
    return wrapper