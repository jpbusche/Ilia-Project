from mongoengine import Document, StringField, ListField, FloatField, DateTimeField
from datetime import datetime
from uuid import uuid4

from utils.schemas import Product
from utils.exceptions import OrderException
from models.product import Products


class Orders(Document):

    meta = {"collection": "orders"}

    order_id = StringField(required=True, unique=True, default=uuid4().hex)
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
            "order_date": self.create_at
        }
    
def add_product(product: Product, owner: str):
    prod = Products.objects(product_id=product.id).first()
    if not prod:
        raise OrderException("Product to add not found!")
    if product.quantity > prod.quantity:
        raise OrderException("Not enough product in store!")
    
    order = Orders.objects(owner=owner).first()
    if order:
        _update_order(order, prod, product.quantity)
    else:
        order = _create_order(prod, product.quantity, owner)
    return order.order_id

def _create_order(prod, quantity: int, owner: str):
    products = []
    products.append({"name": prod.name, "quantity": quantity, "price": prod.price})
    order = Orders(
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
    products.append({"name": prod.name, "quantity": quantity, "price": prod.price})
    order.total_price += quantity * prod.price
    order.save()
    prod.quantity -= quantity
    prod.save()
