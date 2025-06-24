from fastapi import APIRouter

from routers.schemas.costumer_schemas import CostumerCreate
from models.costumer import save_costumer

costumers = APIRouter()


@costumers.post('/register')
def create_costumer(costumer: CostumerCreate):
    try:
        save_costumer(costumer)
        return {"success": True}
    except Exception as e:
        return {"success": False, "message": str(e)}
