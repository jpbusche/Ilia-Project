from mongoengine import Document, StringField, FloatField, IntField

from utils.exceptions import ProductException


class Products(Document):

    meta = {"collection": "products"}

    product_id = StringField(required=True, unique=True)
    name = StringField(required=True)
    price = FloatField(required=True)
    quantity = IntField(required=True)
    rarity = StringField(required=True)
    collection = StringField(required=True)
    image_link = StringField()

    def to_dict(self):
        return {
            "id": self.product_id,
            "name": self.name,
            "price": self.price,
            "quantity": self.quantity,
            "rarity": self.rarity,
            "collection": self.collection,
            "image_link": self.image_link
        }

def get_product(product_id: str):
    product = Products.objects(product_id=product_id).first()
    if not product:
        raise ProductException("Product not found!")
    return product.to_dict()

def get_products():
    return [product.to_dict() for product in Products.objects()]
