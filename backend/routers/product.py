from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from utils.schemas import Costumers
from utils.auth import get_current_costumer
from models.product import get_product, get_products

products = APIRouter()


@products.get('/{product_id}')
def get_product_by_id(product_id: str):
    try:
        product = get_product(product_id)
        return {"success": True, "product": product}
    except Exception as e:
        return JSONResponse(status_code=401, content={"message": str(e), "success": False})
    
@products.get('/')
def get_all_products():
    products = get_products()
    return {"success": True, "products": products}
