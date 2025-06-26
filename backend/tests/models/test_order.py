from unittest import TestCase
from unittest.mock import patch
from pydantic import BaseModel

from utils.exceptions import APIException
from models.order import add_product, remove_product, submit, get_order, history
from tests.models.test_product import ProductTest
from utils.schemas import Product, Order

class OrderTest(BaseModel):
    id: str
    status: str
    total_price: float
    owner: str
    products: list
    created_at: str

    def to_dict(self):
        return self.model_dump()
    
    def save(self):
        pass


class TestOrderModel(TestCase):

    def setUp(self):
        self.product = ProductTest(product_id="id", name="Product Test", price=12.3, quantity=5, rarity="Raridade", collection="Teste", image_link="http://link_image.png")
        self.open_order = OrderTest(id="id", status="open", total_price=36.9, owner="test@email.com", created_at="26-06-2025T13:41:23", 
                                    products=[{"name": self.product.name, "quantity": 2, "price": self.product.price, "id": self.product.product_id},
                                              {"name": self.product.name + " 1", "quantity": 1, "price": self.product.price, "id": self.product.product_id + "1"}])
        self.closed_order = OrderTest(id="id", status="closed", total_price=36.9, owner="test@email.com", created_at="26-06-2025T13:41:23", 
                                      products=[{"name": self.product.name, "quantity": 2, "price": self.product.price, "id": self.product.product_id}])

    @patch("models.order.Orders.objects")
    @patch("models.product.Products.objects")
    @patch("models.order.Orders.save")
    def test_add_product_in_order(self, mock_order_save, mock_product_objects, mock_order_objects):
        mock_product_objects.return_value.first.return_value = self.product
        mock_order_objects.return_value.first.return_value = None
        add_product(Product(id="id", quantity=2), "test@email.com")
        mock_order_save.assert_called_once()

    @patch("models.product.Products.objects")
    def test_raise_not_found_add_product_in_order(self, mock_product_objects):
        mock_product_objects.return_value.first.return_value = None
        with self.assertRaises(APIException) as cm:
            add_product(Product(id="id", quantity=2), "test@email.com")

        self.assertEqual(cm.exception.message, "Product to add not found!")
        self.assertEqual(cm.exception.status_code, 404)

    @patch("models.product.Products.objects")
    def test_raise_not_enough_add_product_in_order(self, mock_product_objects):
        mock_product_objects.return_value.first.return_value = self.product
        with self.assertRaises(APIException) as cm:
            add_product(Product(id="id", quantity=6), "test@email.com")

        self.assertEqual(cm.exception.message, "Not enough product in store!")
        self.assertEqual(cm.exception.status_code, 400)

    @patch("models.order.Orders.objects")
    @patch("models.product.Products.objects")
    def test_remove_product(self, mock_product_objects, mock_order_objects):
        mock_product_objects.return_value.first.return_value = self.product
        mock_order_objects.return_value.first.return_value = self.open_order
        remove_product(Product(id="id"), "test@email.com")

    @patch("models.product.Products.objects")
    def test_raise_not_found_remove_product(self, mock_product_objects):
        mock_product_objects.return_value.first.return_value = None
        with self.assertRaises(APIException) as cm:
            remove_product(Product(id="id"), "test@email.com")

        self.assertEqual(cm.exception.message, "Product to remove not found!")
        self.assertEqual(cm.exception.status_code, 404)

    @patch("models.order.Orders.objects")
    @patch("models.product.Products.objects")
    def test_raise_not_open_remove_product(self, mock_product_objects, mock_order_objects):
        mock_product_objects.return_value.first.return_value = self.product
        mock_order_objects.return_value.first.return_value = None
        with self.assertRaises(APIException) as cm:
            remove_product(Product(id="id"), "test@email.com")

        self.assertEqual(cm.exception.message, "This costumer don't have open order!")
        self.assertEqual(cm.exception.status_code, 400)

    @patch("models.order.Orders.objects")
    @patch("models.product.Products.objects")
    def test_raise_not_product_remove_product(self, mock_product_objects, mock_order_objects):
        mock_product_objects.return_value.first.return_value = ProductTest(product_id="id", name="Other Name", price=12.3, quantity=5, rarity="Raridade", collection="Teste", image_link="http://link_image.png")
        mock_order_objects.return_value.first.return_value = self.open_order
        with self.assertRaises(APIException) as cm:
            remove_product(Product(id="id"), "test@email.com")

        self.assertEqual(cm.exception.message, "Product not found in order!")
        self.assertEqual(cm.exception.status_code, 404)

    @patch("models.order.Orders.objects")
    def test_submit(self, mock_order_objects):
        mock_order_objects.return_value.first.return_value = self.open_order
        submit(Order(id="id"), "test@email.com")

    @patch("models.order.Orders.objects")
    def test_raise_not_found_submit(self, mock_order_objects):
        mock_order_objects.return_value.first.return_value = None
        with self.assertRaises(APIException) as cm:
            submit(Order(id="id"), "test@email.com")

        self.assertEqual(cm.exception.message, "Order not found!")
        self.assertEqual(cm.exception.status_code, 404)
    
    @patch("models.order.Orders.objects")
    def test_raise_closed_submit(self, mock_order_objects):
        mock_order_objects.return_value.first.return_value = self.closed_order
        with self.assertRaises(APIException) as cm:
            submit(Order(id="id"), "test@email.com")

        self.assertEqual(cm.exception.message, "Order already submitted!")
        self.assertEqual(cm.exception.status_code, 400)

    @patch("models.order.Orders.objects")
    def test_get_order(self, mock_order_objects):
        mock_order_objects.return_value.first.return_value = self.open_order
        result = get_order("test@email.com")
        self.assertTrue(result, self.open_order.model_dump())

    @patch("models.order.Orders.objects")
    def test_raise_not_found_get_order(self, mock_order_objects):
        mock_order_objects.return_value.first.return_value = None
        with self.assertRaises(APIException) as cm:
            get_order("test@email.com")

        self.assertEqual(cm.exception.message, "Order not found!")
        self.assertEqual(cm.exception.status_code, 404)

    @patch("models.order.Orders.objects")
    def test_history(self, mock_order_objects):
        mock_order_objects.return_value = [self.open_order]
        result = history("test@email.com")
        self.assertEqual(result, [self.open_order.model_dump()])
