from mongoengine import Document, StringField, ListField, FloatField, DateTimeField
from datetime import datetime
from uuid import uuid4

from utils.schemas import Product, Order
from utils.exceptions import APIException
from models.product import Products


class Orders(Document):

    meta = {"collection": "orders"}

    order_id = StringField(required=True, unique=True)
    status = StringField(default="open")
    owner = StringField(required=True)
    products = ListField(default={})
    total_price = FloatField(default=0.0)
    created_at = DateTimeField(default=datetime.now())

    def to_dict(self):
        return {
            "id": self.order_id,
            "products": self.products,
            "total_price": self.total_price,
            "order_date": self.created_at
        }
    
def add_product(product: Product, owner: str):
    prod = Products.objects(product_id=product.id).first()
    if not prod:
        raise APIException("Product to add not found!", 404)
    if product.quantity > prod.quantity:
        raise APIException("Not enough product in store!", 400)
    
    order = Orders.objects(owner=owner, status="open").first()
    if order:
        _update_order(order, prod, product.quantity)
    else:
        order = _create_order(prod, product.quantity, owner)

def remove_product(product: Product, owner: str):
    prod = Products.objects(product_id=product.id).first()
    if not prod:
        raise APIException("Product to remove not found!", 404)
    
    order = Orders.objects(owner=owner, status="open").first()
    if not order:
        raise APIException("This costumer don't have open order!", 400)
    
    order_product = None
    for _product in order.products:
        if _product["name"] == prod.name:
            order_product = _product
            break
    if not order_product:
        raise APIException("Product not found in order!", 404)
    
    order.products = [_product for _product in order.products if _product["name"] != prod.name]
    if not order.products:
        order.delete()
    else:
        order.total_price -= order_product["quantity"] * prod.price
        order.save()
    prod.quantity += order_product["quantity"]
    prod.save()

def submit(order: Order, owner: str):
    _order = Orders.objects(order_id=order.id, owner=owner).first()
    if not _order:
        raise APIException("Order not found!", 404)
    if _order.status == "closed":
        raise APIException("Order already submitted!", 400)
    
    _order.status = "closed"
    _order.save()

def get_order(owner: str):
    order = Orders.objects(owner=owner, status="open").first()
    if not order:
        raise APIException("Order not found!", 404)
    return order.to_dict()

def history(owner: str):
    return [order.to_dict() for order in Orders.objects(owner=owner, status="closed")]

def _create_order(prod, quantity: int, owner: str):
    products = []
    products.append({"name": prod.name, "quantity": quantity, "price": prod.price, "id": prod.product_id})
    order = Orders(
        order_id=uuid4().hex,
        owner=owner,
        products=products,
        total_price=quantity * prod.price
    )
    prod.quantity -= quantity
    prod.save()
    order.save()
    return order

def _update_order(order, prod, quantity: int):
    products = order.products
    products.append({"name": prod.name, "quantity": quantity, "price": prod.price, "id": prod.product_id})
    order.total_price += quantity * prod.price
    order.save()
    prod.quantity -= quantity
    prod.save()
