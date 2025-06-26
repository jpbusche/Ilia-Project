from unittest import TestCase
from unittest.mock import patch
from pydantic import BaseModel

from utils.exceptions import APIException
from models.product import get_product, get_products

class ProductTest(BaseModel):
    product_id: str
    name: str
    price: float
    quantity: int
    rarity: str
    collection: str
    image_link: str

    def to_dict(self):
        return self.model_dump()
    
    def save(self):
        pass


class TestProductModel(TestCase):

    def setUp(self):
        self.product = ProductTest(product_id="id", name="Product Test", price=12.3, quantity=5, rarity="Raridade", collection="Teste", image_link="http://link_image.png")

    @patch("models.product.Products.objects")
    def test_get_product(self, mock_objects):
        mock_objects.return_value.first.return_value = self.product
        result = get_product("id")
        self.assertEqual(result, self.product.model_dump())
    
    @patch("models.product.Products.objects")
    def test_raise_not_found_get_product(self, mock_objects):
        mock_objects.return_value.first.return_value = None
        with self.assertRaises(APIException) as cm:
            get_product("id")

        self.assertEqual(cm.exception.message, "Product not found!")
        self.assertEqual(cm.exception.status_code, 404)

    @patch("models.product.Products.objects")
    def test_get_product(self, mock_objects):
        mock_objects.return_value = [self.product, self.product, self.product]
        result = get_products()
        self.assertEqual(result, [self.product.model_dump(), self.product.model_dump(), self.product.model_dump()])
