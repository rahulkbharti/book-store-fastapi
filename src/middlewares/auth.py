from fastapi import Request,HTTPException
from functools import wraps
from src.utils.jwt import decode_token

def protected_route(fun):
    @wraps(fun)
    def wrapper(request:Request, *args, **kwargs):
        print("Running the Middleware")
        print(f"Request: {request.method} {request.url}")

        auth_header = request.headers.get("Authorization")
        if not auth_header:
           raise HTTPException(status_code=401, detail="Not authenticated")
        
        data,_ = decode_token(auth_header.split(" ")[1])
        email = data.get("email")
        print(f"Authenticated user: {email} using the route {request.url.path}")
        
        return fun(request, *args, **kwargs)
    return wrapper