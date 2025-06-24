from fastapi import APIRouter
from fastapi.responses import JSONResponse

from utils.schemas import Costumers, Login
from models.costumer import save_costumer, validate_user
from utils.auth import create_token

costumers = APIRouter()


@costumers.post('/register')
def create_costumer(costumer: Costumers):
    try:
        save_costumer(costumer)
        return {"success": True}
    except Exception as e:
        return JSONResponse(status_code=401, content={"message": str(e), "success": False})

@costumers.post('/login')
def login_user(login: Login):
    try:
        validate_user(login)
        token = create_token(login.email)
        return {"success": True, "token": token}
    except Exception as e:
        return JSONResponse(status_code=401, content={"message": str(e), "success": False})
