from unittest import TestCase
from unittest.mock import patch, MagicMock

from utils.schemas import Costumers, Login
from utils.exceptions import APIException
from models.costumer import save_costumer, validate_user, _crypt_password, _verify_password


class TestCostumerModel(TestCase):

    def setUp(self):
        self.costumer = Costumers(name="Test Name", email="test@email.com", password="password")
        self.crypted_costumer = Costumers(name="Test Name", email="test@email.com", password=_crypt_password("password"))

    @patch("models.costumer.Costumers.objects")
    @patch("models.costumer.Costumers.save")
    def test_save_costumer(self, mock_save, mock_objects):
        mock_objects.return_value = None
        save_costumer(self.costumer)
        mock_save.assert_called_once()

    @patch("models.costumer.Costumers.objects")
    def test_raise_already_exist_save_costumer(self, mock_objects):
        mock_costumer = MagicMock()
        mock_costumer.email = self.costumer.email
        mock_objects.return_value = mock_costumer
        with self.assertRaises(APIException) as cm:
            save_costumer(self.costumer)

        self.assertEqual(cm.exception.message, "Costumer with this email already exists!")
        self.assertEqual(cm.exception.status_code, 400)

    @patch("models.costumer.Costumers.objects")
    def test_validate_user(self, mock_objects):
        login = Login(email="test@email.com", password="password")
        mock_objects.return_value.first.return_value = self.crypted_costumer
        validate_user(login)

    @patch("models.costumer.Costumers.objects")
    def test_raise_not_found_validate_user(self, mock_objects):
        login = Login(email="test@email.com", password="password")
        mock_objects.return_value.first.return_value = None
        with self.assertRaises(APIException) as cm:
            validate_user(login)

        self.assertEqual(cm.exception.message, "Costumer not found!")
        self.assertEqual(cm.exception.status_code, 404)

    @patch("models.costumer.Costumers.objects")
    def test_raise_wrong_password_validate_user(self, mock_objects):
        login = Login(email="test@email.com", password="wrong password")
        mock_objects.return_value.first.return_value =self.crypted_costumer
        with self.assertRaises(APIException) as cm:
            validate_user(login)

        self.assertEqual(cm.exception.message, "Invalid password!")
        self.assertEqual(cm.exception.status_code, 400)
