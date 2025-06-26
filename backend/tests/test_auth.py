from unittest import TestCase
from unittest.mock import patch, MagicMock
from fastapi import Request

from utils.auth import create_token, verify_token, get_current_costumer
from utils.exceptions import APIException


class TestAuth(TestCase):

    def setUp(self):
        self.email = "test@email.com"
        self.mock_request = MagicMock(spec=Request)

    def test_create_token(self):
        token = create_token(self.email)
        self.assertTrue(verify_token(token, self.email))

    def test_verify_positive_token(self):
        token = "$2b$12$nVUO66cRC8GyKKGpQ/hmaePwaOggWlKuVQ6tyT8rf.M2vUfD9kEAm"
        self.assertTrue(verify_token(token, self.email))

    def test_verify_negative_token(self):
        token = "$2b$12$nVUO66cRC8GyKKGpQ/hmaePwaOggWlKuVQ6tyT8rf.OIAUmascbn2"
        self.assertFalse(verify_token(token, self.email))

    @patch("models.costumer.Costumers.objects")
    def test_get_current_costumer(self, mock_costumers):
        self.mock_request.headers.get.return_value = "$2b$12$nVUO66cRC8GyKKGpQ/hmaePwaOggWlKuVQ6tyT8rf.M2vUfD9kEAm"

        mock_costumer = MagicMock()
        mock_costumer.email = self.email
        mock_costumers.return_value = [mock_costumer]

        result = get_current_costumer(self.mock_request)
        self.assertEqual(result, mock_costumer)

    @patch("models.costumer.Costumers.objects")
    def test_raise_not_found_exception_get_current_costumer(self, mock_costumers):
        self.mock_request.headers.get.return_value = None
        with self.assertRaises(APIException) as cm:
            get_current_costumer(self.mock_request)

        self.assertEqual(cm.exception.message, "Authetication Token not found!")
        self.assertEqual(cm.exception.status_code, 401)

    @patch("models.costumer.Costumers.objects")
    def test_raise_invalid_token_exception_get_current_costumer(self, mock_costumers):
        self.mock_request.headers.get.return_value = "$2b$12$nVUO66cRC8GyKKGpQ/hmaePwaOggWlKuVQ6tyT8rf.OIAUmascbn2"

        mock_costumer = MagicMock()
        mock_costumer.email = self.email
        mock_costumers.return_value = [mock_costumer]

        with self.assertRaises(APIException) as cm:
            get_current_costumer(self.mock_request)

        self.assertEqual(cm.exception.message, "Authetication Token invalid")
        self.assertEqual(cm.exception.status_code, 401)
