from mongoengine import Document, StringField
from passlib.context import CryptContext

from routers.schemas.costumer_schemas import CostumerCreate
from settings import CreateException

context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Costumers(Document):

    meta = {"collection": "costumers"}

    name = StringField(required=True)
    email = StringField(required=True)
    password = StringField(required=True)

def save_costumer(costumer_data: CostumerCreate):
    if Costumers.objects(email=costumer_data.email):
        raise CreateException("Costumer with this email already exists!")
    costumer = Costumers(
        name=costumer_data.name,
        email=costumer_data.email,
        password=_crypt_password(costumer_data.password)
    )
    costumer.save()

def _crypt_password(password: str) -> str:
    return context.hash(password)
