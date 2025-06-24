from fastapi import APIRouter, HTTPException, Response

from routers.schemas.costumer_schemas import CostumerCreate, CostumerLogin
from models.costumer import save_costumer, validate_user
from utils.auth import create_token
from settings import EXPIRE_TIME

costumers = APIRouter()


@costumers.post('/register')
def create_costumer(costumer: CostumerCreate):
    try:
        save_costumer(costumer)
        return {"success": True}
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))

@costumers.post('/login')
def login_user(login: CostumerLogin, response: Response):
    try:
        validate_user(login)
        token = create_token(data={"email": login.email})
        response.set_cookie(key="Token", value=token, httponly=True, max_age= 60 * EXPIRE_TIME)
        return {"success": True}
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))