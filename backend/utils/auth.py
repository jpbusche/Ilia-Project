from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi import Request, HTTPException

from settings import SECRET_KEY, EXPIRE_TIME


def create_token(data: dict):
    token_data = data | {"exp": datetime.now() + timedelta(minutes=EXPIRE_TIME)}
    return jwt.encode(token_data, SECRET_KEY, "HS256")

def verify_token(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, "HS256")
    except JWTError:
        return None