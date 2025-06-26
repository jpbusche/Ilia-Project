from fastapi import APIRouter

from utils.schemas import Costumers, Login
from models.costumer import save_costumer, validate_user
from utils.auth import create_token

costumers = APIRouter()


@costumers.post('/register')
def create_costumer(costumer: Costumers):
    save_costumer(costumer)
    return {"success": True}

@costumers.post('/login')
def login_user(login: Login):
    validate_user(login)
    token = create_token(login.email)
    return {"success": True, "token": token}
