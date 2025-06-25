from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from utils.schemas import Product, Costumers
from utils.auth import get_current_costumer
from models.order import add_product

orders = APIRouter()


@orders.post('/add')
def add_product_in_order(product: Product, current_costumer: Costumers = Depends(get_current_costumer)):
    try:
        order_id = add_product(product, current_costumer.email)
        return {"success": True, "order_id": order_id}
    except Exception as e:
        return JSONResponse(status_code=401, content={"message": str(e), "success": False})
