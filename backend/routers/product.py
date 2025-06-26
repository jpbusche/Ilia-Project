from fastapi import APIRouter

from models.product import get_product, get_products

products = APIRouter()


@products.get('/{product_id}')
def get_product_by_id(product_id: str):
    product = get_product(product_id)
    return {"success": True, "product": product}
    
@products.get('/')
def get_all_products():
    products = get_products()
    return {"success": True, "products": products}
