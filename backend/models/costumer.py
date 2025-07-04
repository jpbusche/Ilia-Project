from mongoengine import Document, StringField
from passlib.context import CryptContext

from utils.schemas import Costumers, Login
from utils.exceptions import APIException

context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Costumers(Document):

    meta = {"collection": "costumers"}

    name = StringField(required=True)
    email = StringField(required=True, unique=True)
    password = StringField(required=True)

def save_costumer(costumer_data: Costumers):
    if Costumers.objects(email=costumer_data.email):
        raise APIException("Costumer with this email already exists!", 400)
    costumer = Costumers(
        name=costumer_data.name,
        email=costumer_data.email,
        password=_crypt_password(costumer_data.password)
    )
    costumer.save()

def validate_user(login: Login):
    user = Costumers.objects(email=login.email).first()
    if not user:
        raise APIException("Costumer not found!", 404)
    if not _verify_password(login.password, user.password):
        raise APIException("Invalid password!", 400)

def _crypt_password(password: str) -> str:
    return context.hash(password)

def _verify_password(login_password: str, user_password: str):
    return context.verify(login_password, user_password) 
