from fastapi import Request
from passlib.context import CryptContext

from utils.exceptions import APIException
from models.costumer import Costumers

context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_token(email: str):
    return context.hash(email)

def verify_token(token: str, test_email: str):
    return context.verify(test_email, token)
    
def get_current_costumer(request: Request):
    token = request.headers.get("Token")
    if not token:
        raise APIException("Authetication Token not found!", 401)
    try:
        for costumer in Costumers.objects():
            if verify_token(token, costumer.email): return costumer
        raise APIException("Authetication Token invalid", 401)
    except:
        raise APIException("Authetication Token invalid", 401)