from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from utils.schemas import Product, Costumers, Order
from utils.auth import get_current_costumer
from models.order import add_product, remove_product, submit, get_order

orders = APIRouter()


@orders.post('/add')
def add_product_in_order(product: Product, current_costumer: Costumers = Depends(get_current_costumer)):
    try:
        order_id = add_product(product, current_costumer.email)
        return {"success": True, "order_id": order_id}
    except Exception as e:
        return JSONResponse(status_code=401, content={"message": str(e), "success": False})

@orders.post('/remove')
def remove_product_in_order(product: Product, current_costumer: Costumers = Depends(get_current_costumer)):
    try:
        remove_product(product, current_costumer.email)
        return {"success": True}
    except Exception as e:
        return JSONResponse(status_code=401, content={"message": str(e), "success": False})
    
@orders.post('/submit')
def submit_order(order: Order, current_costumer: Costumers = Depends(get_current_costumer)):
    try:
        submit(order, current_costumer.email)
        return {"success": True}
    except Exception as e:
        return JSONResponse(status_code=401, content={"message": str(e), "success": False})
    
@orders.get('/{order_id}')
def get_order_by_id(order_id: str, current_costumer: Costumers = Depends(get_current_costumer)):
    try:
        order = get_order(order_id, current_costumer.email)
        return {"success": True, "order": order}
    except Exception as e:
        return JSONResponse(status_code=401, content={"message": str(e), "success": False})