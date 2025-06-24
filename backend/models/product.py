from mongoengine import Document, StringField

from utils.exceptions import ProductException


class Products(Document):

    meta = {"collection": "products"}

    product_id = StringField(required=True, unique=True)

    def to_dict(self):
        return {
            "id": self.product_id
        }

def get_product(product_id: str):
    print(product_id)
    product = Products.objects(product_id=product_id).first()
    if not product:
        raise ProductException("Product not found!")
    return product.to_dict()